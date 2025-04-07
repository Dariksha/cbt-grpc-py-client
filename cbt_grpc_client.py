import argparse
import grpc
import ssl
from google.protobuf import descriptor_pb2
from com.nutanix.dataprotection.v4.content import content_pb2
from com.nutanix.dataprotection.v4.content import VolumeGroupRecoveryPointComputeChangedRegions_service_pb2
from com.nutanix.dataprotection.v4.content import VolumeGroupRecoveryPointComputeChangedRegions_service_pb2_grpc
from com.nutanix.dataprotection.v4.content import VMRecoveryPointComputeChangedRegions_service_pb2
from com.nutanix.dataprotection.v4.content import VMRecoveryPointComputeChangedRegions_service_pb2_grpc
import pdb
import requests

def fetch_jwt_token(pc_ip, recovery_point_ext_id, vm_recovery_point_ext_id, disk_recovery_point_ext_id):
    url = f"https://{pc_ip}:9440/api/dataprotection/v4.0/config/recovery-points/{recovery_point_ext_id}/$actions/discover-cluster"

    body = {
        "operation": "COMPUTE_CHANGED_REGIONS",
        "spec": {
            "$objectType": "dataprotection.v4.content.ComputeChangedRegionsClusterDiscoverSpec",
            "diskRecoveryPoint": {
                "$objectType": "dataprotection.v4.content.VmDiskRecoveryPointReference",
                "recoveryPointExtId": recovery_point_ext_id,
                "vmRecoveryPointExtId": vm_recovery_point_ext_id,
                "diskRecoveryPointExtId": disk_recovery_point_ext_id
            }
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Basic YWRtaW46TnV0YW5peC4xMjM="
    }

    print(f"Sending request to: {url}")
    print(f"Headers: {headers}")

    response = requests.post(url, json=body, headers=headers, verify=False)  # Disable SSL verification for now

    print(f"Response Code: {response.status_code}")
    
    if response.status_code == 200:
        response_data = response.json()
        jwt_token = response_data.get("data", {}).get("jwtToken")  # Extract jwtToken

        if jwt_token:
            print("JWT Token Retrieved Successfully!")
            return jwt_token
        else:
            raise ValueError("JWT Token Not Found in Response!")

    else:
        print(f"Response Text: {response.text}")
        raise ValueError(f"Failed to fetch JWT Token: {response.status_code}")
    

def compute_vm_changed_regions(server_address,jwt_token):
    """
    Example client to call volumeGroupRecoveryPointComputeChangedRegions gRPC service
    with dummy payload
    
    :param server_address: gRPC server address in format 'ip:port'
    """
    try:
        # Create SSL credentials without CA verification (just encryption)
        # credentials = grpc.ssl_channel_credentials()
        # Create a gRPC channel
        # channel = grpc.insecure_channel(server_address)
        # channel = grpc.secure_channel(server_address, credentials)

        # Create gRPC SSL credentials using the modified SSL context
        # credentials = grpc.ssl_channel_credentials(root_certificates=None)
        # Override gRPC options to allow insecure verification (like Go's `InsecureSkipVerify: true`)
        # Override options to bypass hostname and authority validation
        options = [
            ("grpc.ssl_target_name_override", "ignore"),
            ("grpc.default_authority", "ignore"),
        ]
        # Establish a secure channel without verifying the server certificate
        channel = grpc.secure_channel(server_address,
        grpc.ssl_channel_credentials(
            root_certificates=None,
            private_key=None,
            certificate_chain=None
        ),
        options)

        # Create a stub (client)
        stub = VMRecoveryPointComputeChangedRegions_service_pb2_grpc.VMRecoveryPointComputeChangedRegionsServiceStub(channel)
        
        # Prepare the request payload
        request = VMRecoveryPointComputeChangedRegions_service_pb2.VmRecoveryPointComputeChangedRegionsArg(
            # Dummy external identifiers 
            recovery_point_ext_id='0f173e13-cd30-4cfb-a054-7ef324f41c14',
            vm_recovery_point_ext_id='2554e45c-466d-47c6-8a01-b362681527e2',
            ext_id='12eb2a64-7c1e-4875-9087-b1254d3f59a6',
            
            # Prepare the body with compute changed regions specification
            body=content_pb2.VmRecoveryPointChangedRegionsComputeSpec(
                # Base recovery point specification
                base=content_pb2.VmDiskRecoveryPointClusterDiscoverSpec(
                    base=content_pb2.BaseRecoveryPointSpec(
                        reference_recovery_point_ext_id='2ef770ba-a517-46e6-8d3a-c82e5f76766c',
                        reference_disk_recovery_point_ext_id='a935e027-91ae-40f0-8740-7fa2ee8ac1f6'
                    ),
                    reference_vm_recovery_point_ext_id='510ca1fc-ced2-4eb1-8364-5c24983a8e6a'
                ),
                
                # Optional parameters for changed regions computation
                offset=0,  # Start from the beginning of the disk
                length=1024 * 1024,  # Compute for 1MB 
                block_size=65536  # 64KB block size
            )
        )
        
        try:
            # Send auth token in gRPC metadata
            metadata = [("authorization", f"Bearer {jwt_token}")]
            # Make the gRPC call
            response, call = stub.vmRecoveryPointComputeChangedRegions.with_call(request, metadata=metadata)
            # Process the response

            #  Print response metadata
            print("\nResponse Metadata:")
            for key, value in call.trailing_metadata():
                print(f"{key}: {value}")

            print("\nInitial Metadata:")
            for key, value in call.initial_metadata():
                print(f"{key}: {value}")

            if response.content.HasField('changed_region_array_data'):
                changed_regions = response.content.changed_region_array_data.value
                print("Changed Regions:")
                for region in changed_regions:
                    print(f"Offset: {region.offset}, Length: {region.length}, Type: {region.region_type}")
            elif response.content.HasField('error_response_data'):
                error_response = response.content.error_response_data.value
                print(f"Error: {error_response}")
            
            # # Optional: Print response headers
            # print("\nResponse Headers:")
            # for key, value in response.reserved.items():
            #     print(f"{key}: {value}")
        
        except grpc.RpcError as e:
            print(f"RPC failed: {e}")
    
    except Exception as e:
        print(f"Error connecting to server: {e}")

def compute_volume_group_changed_regions(server_address):
    """
    Example client to call volumeGroupRecoveryPointComputeChangedRegions gRPC service
    with dummy payload
    
    :param server_address: gRPC server address in format 'ip:port'
    """
    try:
        # Create SSL credentials without CA verification (just encryption)
        # credentials = grpc.ssl_channel_credentials()
        # Create a gRPC channel
        #channel = grpc.insecure_channel(server_address)
        
        # Create an SSL context that disables certificate verification
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False  # Disable hostname verification
        ssl_context.verify_mode = ssl.CERT_NONE  # Skip certificate validation
        # Create gRPC SSL credentials using the modified SSL context
        credentials = grpc.ssl_channel_credentials(root_certificates=None)
        # Override gRPC options to allow insecure verification (like Go's `InsecureSkipVerify: true`)
        # Override gRPC options to disable hostname validation
        options = [
            ("grpc.ssl_target_name_override", "ignore"),  # Bypass hostname check
            ("grpc.default_authority", "ignore"),        # Prevent authority validation
        ]
        # Establish a secure channel without verifying the server certificate
        channel = grpc.secure_channel(server_address, credentials, options)
        
        # Create a stub (client)
        stub = VolumeGroupRecoveryPointComputeChangedRegions_service_pb2_grpc.VolumeGroupRecoveryPointComputeChangedRegionsServiceStub(channel)
        
        # Prepare the request payload
        request = VolumeGroupRecoveryPointComputeChangedRegions_service_pb2.VolumeGroupRecoveryPointComputeChangedRegionsArg(
            # Dummy external identifiers 
            recovery_point_ext_id='dummy-recovery-point-ext-id',
            volume_group_recovery_point_ext_id='dummy-volume-group-recovery-point-ext-id',
            ext_id='dummy-disk-recovery-point-ext-id',
            
            # Prepare the body with compute changed regions specification
            body=content_pb2.VolumeGroupRecoveryPointChangedRegionsComputeSpec(
                # Base recovery point specification
                base=content_pb2.VolumeGroupDiskRecoveryPointClusterDiscoverSpec(
                    base=content_pb2.BaseRecoveryPointSpec(
                        reference_recovery_point_ext_id='ref-recovery-point-ext-id',
                        reference_disk_recovery_point_ext_id='ref-disk-recovery-point-ext-id'
                    ),
                    reference_volume_group_recovery_point_ext_id='ref-volume-group-recovery-point-ext-id'
                ),
                
                # Optional parameters for changed regions computation
                offset=0,  # Start from the beginning of the disk
                length=1024 * 1024,  # Compute for 1MB 
                block_size=65536  # 64KB block size
            )
        )
        
        try:
            # Make the gRPC call
            response = stub.volumeGroupRecoveryPointComputeChangedRegions(request)
            
            # Process the response
            if response.content.HasField('changed_region_array_data'):
                changed_regions = response.content.changed_region_array_data.value
                print("Changed Regions:")
                for region in changed_regions:
                    print(f"Offset: {region.offset}, Length: {region.length}, Type: {region.region_type}")
            elif response.content.HasField('error_response_data'):
                error_response = response.content.error_response_data.value
                print(f"Error: {error_response}")
            
            # Optional: Print response headers
            print("\nResponse Headers:")
            for key, value in response.reserved.items():
                print(f"{key}: {value}")
        
        except grpc.RpcError as e:
            print(f"RPC failed: {e}")
    
    except Exception as e:
        print(f"Error connecting to server: {e}")

def main():
    # Example Usage
    
    
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Nutanix Recovery Point Changed Regions gRPC Client')
    parser.add_argument('server', 
                        help='gRPC server address in format ip:port (e.g., 192.168.1.100:50051)',
                        type=str)
    parser.add_argument('function', 
                    help='Function to call: "volume_group" or "vm"',
                    type=str, choices=['volume_group', 'vm'])
    
    # Parse arguments
    args = parser.parse_args()

    pc_ip = "10.61.6.136"
    recovery_point_ext_id='0f173e13-cd30-4cfb-a054-7ef324f41c14'
    vm_recovery_point_ext_id='2554e45c-466d-47c6-8a01-b362681527e2'
    ext_id='12eb2a64-7c1e-4875-9087-b1254d3f59a6'
    #jwt_token = fetch_jwt_token(pc_ip, recovery_point_ext_id, vm_recovery_point_ext_id, ext_id)
    jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJudG54X2FwcF9kYXRhIjp7ImRpc2tfcmVjb3ZlcnlfcG9pbnRfZXh0X2lkIjpbIjEyZWIyYTY0LTdjMWUtNDg3NS05MDg3LWIxMjU0ZDNmNTlhNiJdLCJyZWNvdmVyeV9wb2ludF9leHRfaWQiOlsiMGYxNzNlMTMtY2QzMC00Y2ZiLWEwNTQtN2VmMzI0ZjQxYzE0Il0sInZtX3JlY292ZXJ5X3BvaW50X2V4dF9pZCI6WyIyNTU0ZTQ1Yy00NjZkLTQ3YzYtOGEwMS1iMzYyNjgxNTI3ZTIiXX0sInNjb3BlIjpbIi9hcGkvZGF0YXByb3RlY3Rpb24vdjQuMC9jb250ZW50Il0sInVzZXJfcHJvZmlsZSI6IntcIl9wZXJtYW5lbnRcIjogdHJ1ZSwgXCJhdXRoZW50aWNhdGVkXCI6IHRydWUsIFwiYXBwX2RhdGFcIjoge30sIFwidXNlcm5hbWVcIjogXCJhZG1pblwiLCBcImRvbWFpblwiOiBudWxsLCBcInVzZXJ0eXBlXCI6IFwibG9jYWxcIiwgXCJzZXJ2aWNlX25hbWVcIjogXCJNZXJjdXJ5U2VydmljZVwiLCBcImF1dGhfaW5mb1wiOiB7XCJ0ZW5hbnRfdXVpZFwiOiBcIjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMFwiLCBcInNlcnZpY2VfbmFtZVwiOiBcIk1lcmN1cnlTZXJ2aWNlXCIsIFwidXNlcl91dWlkXCI6IFwiMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwXCIsIFwidG9rZW5fYXVkaWVuY2VcIjogbnVsbCwgXCJ0b2tlbl9pc3N1ZXJcIjogbnVsbCwgXCJ1c2VybmFtZVwiOiBcImFkbWluXCIsIFwicmVtb3RlX2F1dGhvcml6YXRpb25cIjogbnVsbCwgXCJyZW1vdGVfYXV0aF9qc29uXCI6IG51bGwsIFwid29ya2Zsb3dfdHlwZVwiOiBudWxsLCBcInVzZXJfZ3JvdXBfdXVpZHNcIjogbnVsbH0sIFwibG9nX3V1aWRcIjogXCI3NWMxZmQyZi1lNGIzLTRlMzAtYWRjZC1iNGEzMTEyZGMxZTJcIiwgXCJvcmlnX3Rva2VuX2lzc190aW1lXCI6IDE3NDI5NzEwNzR9IiwianRpIjoiMDhmYzA2NWQtZDllYy0zZGMwLWI2YTUtYWQ2MmZjY2ZhOWQzIiwiaXNzIjoiQXRoZW5hIiwiaWF0IjoxNzQyOTcxMDc0LCJleHAiOjE3NDI5NzE5NzR9.NelZ6b67306nNBEopiv8Wn5J0sOL2_hle8sZZPQj862OysAiwzMgpQ1uD0JzD5li9ujlp3AN0-xqju7rDW6cpAyftB5O8SnVff7wdk97UgV9ynf-F3yD1E6U-NSxVz7SJtPz6mmyz-N1cqvzXCkZRinRbzebc6Q3UXfDSLTlrqiZAACZ63OIZaGarkm19dLWDdyob2wZa_-WhqaeiOPlmzcX-EmwesthM617Q26adIkkZUXFkk1bc5zTjuWSw00t7GOnpKZb0ZP-64iyHokyD2el9TyBiYdOl-rHq9rGqgKvCvhtzWXY-eXoUvDCOHa9fDZbyj5_OibmD2w-TDdMOw"
    print("JWT Token:", jwt_token)
    # Call the appropriate function based on the provided argument
    if args.function == 'volume_group':
        compute_volume_group_changed_regions(args.server)
    elif args.function == 'vm':
        compute_vm_changed_regions(args.server,jwt_token)

if __name__ == '__main__':
    main()
