import argparse
import grpc
import requests
from google.protobuf import descriptor_pb2
from com.nutanix.dataprotection.v4.content import content_pb2
from com.nutanix.dataprotection.v4.content import VolumeGroupRecoveryPointComputeChangedRegions_service_pb2
from com.nutanix.dataprotection.v4.content import VolumeGroupRecoveryPointComputeChangedRegions_service_pb2_grpc
from com.nutanix.dataprotection.v4.content import VMRecoveryPointComputeChangedRegions_service_pb2
from com.nutanix.dataprotection.v4.content import VMRecoveryPointComputeChangedRegions_service_pb2_grpc
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

PC_IP="10.33.81.74"
RECOVERY_POINT_EXT_ID="4f30f7ab-9236-4dbb-9122-aa76194a358d"
VM_RECOVERY_POINT_EXT_ID="52b90e12-5abd-4a3d-8b1e-652637e9b319"
DISK_RECOVERY_POINT_EXT_ID="b17a08ea-3344-4362-ba20-659292c836eb"

REFERENCE_RECOVERY_POINT_EXT_ID="9d5bba3c-67d8-4a15-8b55-0c6584ae7891"
REFERENCE_DISK_RECOVERY_POINT_EXT_ID="0e675252-d5b4-4ebb-8856-951ca5cf6b40"
REFERENCE_VM_RECOVERY_POINT_EXT_ID="bfef1eef-a42a-4300-9ef3-a5db041b7e10"

def fetch_jwt_token():
    url = f"https://{PC_IP}:9440/api/dataprotection/v4.0/config/recovery-points/{RECOVERY_POINT_EXT_ID}/$actions/discover-cluster"

    body = {
        "operation": "COMPUTE_CHANGED_REGIONS",
        "spec": {
            "$objectType": "dataprotection.v4.content.ComputeChangedRegionsClusterDiscoverSpec",
            "diskRecoveryPoint": {
                "$objectType": "dataprotection.v4.content.VmDiskRecoveryPointReference",
                "recoveryPointExtId": RECOVERY_POINT_EXT_ID,
                "vmRecoveryPointExtId": VM_RECOVERY_POINT_EXT_ID,
                "diskRecoveryPointExtId": DISK_RECOVERY_POINT_EXT_ID
            }
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Basic YWRtaW46TnV0YW5peC4xMjM="  # Replace with actual base64 if needed
    }

    print(f"Requesting JWT token from: {url}")
    response = requests.post(url, json=body, headers=headers, verify=False)

    if response.status_code == 200:
        jwt_token = response.json().get("data", {}).get("jwtToken")
        if jwt_token:
            print("JWT Token fetched successfully.")
            return jwt_token
        raise ValueError("JWT token not found in response.")
    else:
        raise ValueError(f"Failed to get JWT token. HTTP {response.status_code}: {response.text}")

def compute_vm_changed_regions(server_address, jwt_token):
    channel = grpc.insecure_channel(
        server_address,
        options=[
            ('grpc.max_receive_message_length', 100 * 1024 * 1024),
            ('grpc.max_send_message_length', 100 * 1024 * 1024),
        ]
    )
    stub = VMRecoveryPointComputeChangedRegions_service_pb2_grpc.VMRecoveryPointComputeChangedRegionsServiceStub(channel)

    request = VMRecoveryPointComputeChangedRegions_service_pb2.VmRecoveryPointComputeChangedRegionsArg(
        recovery_point_ext_id=RECOVERY_POINT_EXT_ID,
        vm_recovery_point_ext_id=VM_RECOVERY_POINT_EXT_ID,
        ext_id=DISK_RECOVERY_POINT_EXT_ID,
        body=content_pb2.VmRecoveryPointChangedRegionsComputeSpec(
            base=content_pb2.VmDiskRecoveryPointClusterDiscoverSpec(
                base=content_pb2.BaseRecoveryPointSpec(
                    reference_recovery_point_ext_id=REFERENCE_RECOVERY_POINT_EXT_ID,
                    reference_disk_recovery_point_ext_id=REFERENCE_DISK_RECOVERY_POINT_EXT_ID
                ),
                reference_vm_recovery_point_ext_id=REFERENCE_VM_RECOVERY_POINT_EXT_ID
            ),
            offset=0,
            length=1024 * 1024,
            block_size=65536
        )
    )

    try:
        metadata = [("authorization", f"Bearer {jwt_token}")]
        print("Initiating VM Changed Regions Streaming RPC...")
        for response in stub.vmRecoveryPointComputeChangedRegions(request, metadata=metadata):
            if response.content.HasField('changed_region_array_data'):
                print("\nReceived Changed Region Batch:")
                for region in response.content.changed_region_array_data.value:
                    print(f"Offset: {region.offset}, Length: {region.length}, Type: {region.region_type}")
            elif response.content.HasField('error_response_data'):
                print(f"\nError: {response.content.error_response_data.value}")
                break
        print("\nStreaming complete.")

    except grpc.RpcError as e:
        print(f"RPC failed: {e.code()}: {e.details()}")

def compute_volume_group_changed_regions(server_address):
    channel = grpc.insecure_channel(server_address)
    stub = VolumeGroupRecoveryPointComputeChangedRegions_service_pb2_grpc.VolumeGroupRecoveryPointComputeChangedRegionsServiceStub(channel)

    request = VolumeGroupRecoveryPointComputeChangedRegions_service_pb2.VolumeGroupRecoveryPointComputeChangedRegionsArg(
        recovery_point_ext_id='dummy-recovery-point-ext-id',
        volume_group_recovery_point_ext_id='dummy-volume-group-recovery-point-ext-id',
        ext_id='dummy-disk-recovery-point-ext-id',
        body=content_pb2.VolumeGroupRecoveryPointChangedRegionsComputeSpec(
            base=content_pb2.VolumeGroupDiskRecoveryPointClusterDiscoverSpec(
                base=content_pb2.BaseRecoveryPointSpec(
                    reference_recovery_point_ext_id='ref-recovery-point-ext-id',
                    reference_disk_recovery_point_ext_id='ref-disk-recovery-point-ext-id'
                ),
                reference_volume_group_recovery_point_ext_id='ref-volume-group-recovery-point-ext-id'
            ),
            offset=0,
            length=1024 * 1024,
            block_size=65536
        )
    )

    try:
        response = stub.volumeGroupRecoveryPointComputeChangedRegions(request)
        if response.content.HasField('changed_region_array_data'):
            print("Changed Regions:")
            for region in response.content.changed_region_array_data.value:
                print(f"Offset: {region.offset}, Length: {region.length}, Type: {region.region_type}")
        elif response.content.HasField('error_response_data'):
            print(f"Error: {response.content.error_response_data.value}")
    except grpc.RpcError as e:
        print(f"gRPC error: {e}")

def main():
    jwt_token = fetch_jwt_token()
    print("JWT Token:", jwt_token)

    parser = argparse.ArgumentParser(description='CBT Streaming gRPC Client')
    parser.add_argument('server', help='Server in ip:port format')
    parser.add_argument('function', choices=['vm', 'volume_group'], help='Which API to call')
    args = parser.parse_args()

    if args.function == 'vm':
        compute_vm_changed_regions(args.server, jwt_token)
    elif args.function == 'volume_group':
        compute_volume_group_changed_regions(args.server)

if __name__ == '__main__':
    main()
