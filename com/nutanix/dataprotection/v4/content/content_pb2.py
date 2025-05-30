# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/nutanix/dataprotection/v4/content/content.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'com/nutanix/dataprotection/v4/content/content.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.nutanix.dataprotection.v4.error import error_pb2 as com_dot_nutanix_dot_dataprotection_dot_v4_dot_error_dot_error__pb2
from com.nutanix.common.v1.response import response_pb2 as com_dot_nutanix_dot_common_dot_v1_dot_response_dot_response__pb2
from com.nutanix.common.v1.config import config_pb2 as com_dot_nutanix_dot_common_dot_v1_dot_config_dot_config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3com/nutanix/dataprotection/v4/content/content.proto\x12%com.nutanix.dataprotection.v4.content\x1a/com/nutanix/dataprotection/v4/error/error.proto\x1a-com/nutanix/common/v1/response/response.proto\x1a)com/nutanix/common/v1/config/config.proto\"p\n\x15\x42\x61seRecoveryPointSpec\x12(\n\x1freference_recovery_point_ext_id\x18\xd1\x0f \x01(\t\x12-\n$reference_disk_recovery_point_ext_id\x18\xd2\x0f \x01(\t\"\x8c\x01\n\rChangedRegion\x12\x0f\n\x06offset\x18\xd1\x0f \x01(\x03\x12\x0f\n\x06length\x18\xd2\x0f \x01(\x03\x12Y\n\x0bregion_type\x18\xd3\x0f \x01(\x0e\x32\x43.com.nutanix.dataprotection.v4.content.RegionTypeMessage.RegionType\"a\n\x19\x43hangedRegionArrayWrapper\x12\x44\n\x05value\x18\xe8\x07 \x03(\x0b\x32\x34.com.nutanix.dataprotection.v4.content.ChangedRegion\"Z\n\x14\x45rrorResponseWrapper\x12\x42\n\x05value\x18\xe8\x07 \x01(\x0b\x32\x32.com.nutanix.dataprotection.v4.error.ErrorResponse\"\xaa\x02\n\x13\x43hangedRegionsModel\x12\x66\n\x19\x63hanged_region_array_data\x18\xd3\x0f \x01(\x0b\x32@.com.nutanix.dataprotection.v4.content.ChangedRegionArrayWrapperH\x00\x12[\n\x13\x65rror_response_data\x18\x90\x03 \x01(\x0b\x32;.com.nutanix.dataprotection.v4.content.ErrorResponseWrapperH\x00\x12\x46\n\x08metadata\x18\xe9\x07 \x01(\x0b\x32\x33.com.nutanix.common.v1.response.ApiResponseMetadataB\x06\n\x04\x64\x61ta\"b\n\x0b\x43lusterInfo\x12\x14\n\x0b\x63\x65rtificate\x18\xd1\x0f \x01(\t\x12=\n\x0bredirect_ip\x18\xd2\x0f \x01(\x0b\x32\'.com.nutanix.common.v1.config.IPAddress\"W\n\x11RegionTypeMessage\"B\n\nRegionType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0c\n\x08REDACTED\x10\x01\x12\x0b\n\x06ZEROED\x10\xd1\x0f\x12\x0c\n\x07REGULAR\x10\xd2\x0f\"\xa2\x01\n&VmDiskRecoveryPointClusterDiscoverSpec\x12K\n\x04\x62\x61se\x18\xd4\x0f \x01(\x0b\x32<.com.nutanix.dataprotection.v4.content.BaseRecoveryPointSpec\x12+\n\"reference_vm_recovery_point_ext_id\x18\xd5\x0f \x01(\t\"\xbf\x01\n(VmRecoveryPointChangedRegionsComputeSpec\x12\\\n\x04\x62\x61se\x18\xd9\x0f \x01(\x0b\x32M.com.nutanix.dataprotection.v4.content.VmDiskRecoveryPointClusterDiscoverSpec\x12\x0f\n\x06offset\x18\xda\x0f \x01(\x03\x12\x0f\n\x06length\x18\xdb\x0f \x01(\x03\x12\x13\n\nblock_size\x18\xdc\x0f \x01(\x03\"\xb5\x01\n/VolumeGroupDiskRecoveryPointClusterDiscoverSpec\x12K\n\x04\x62\x61se\x18\xd4\x0f \x01(\x0b\x32<.com.nutanix.dataprotection.v4.content.BaseRecoveryPointSpec\x12\x35\n,reference_volume_group_recovery_point_ext_id\x18\xd5\x0f \x01(\t\"\xd1\x01\n1VolumeGroupRecoveryPointChangedRegionsComputeSpec\x12\x65\n\x04\x62\x61se\x18\xd9\x0f \x01(\x0b\x32V.com.nutanix.dataprotection.v4.content.VolumeGroupDiskRecoveryPointClusterDiscoverSpec\x12\x0f\n\x06offset\x18\xda\x0f \x01(\x03\x12\x0f\n\x06length\x18\xdb\x0f \x01(\x03\x12\x13\n\nblock_size\x18\xdc\x0f \x01(\x03\x42P\n%com.nutanix.dataprotection.v4.contentP\x01Z%com/nutanix/dataprotection/v4/contentb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.nutanix.dataprotection.v4.content.content_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n%com.nutanix.dataprotection.v4.contentP\001Z%com/nutanix/dataprotection/v4/content'
  _globals['_BASERECOVERYPOINTSPEC']._serialized_start=233
  _globals['_BASERECOVERYPOINTSPEC']._serialized_end=345
  _globals['_CHANGEDREGION']._serialized_start=348
  _globals['_CHANGEDREGION']._serialized_end=488
  _globals['_CHANGEDREGIONARRAYWRAPPER']._serialized_start=490
  _globals['_CHANGEDREGIONARRAYWRAPPER']._serialized_end=587
  _globals['_ERRORRESPONSEWRAPPER']._serialized_start=589
  _globals['_ERRORRESPONSEWRAPPER']._serialized_end=679
  _globals['_CHANGEDREGIONSMODEL']._serialized_start=682
  _globals['_CHANGEDREGIONSMODEL']._serialized_end=980
  _globals['_CLUSTERINFO']._serialized_start=982
  _globals['_CLUSTERINFO']._serialized_end=1080
  _globals['_REGIONTYPEMESSAGE']._serialized_start=1082
  _globals['_REGIONTYPEMESSAGE']._serialized_end=1169
  _globals['_REGIONTYPEMESSAGE_REGIONTYPE']._serialized_start=1103
  _globals['_REGIONTYPEMESSAGE_REGIONTYPE']._serialized_end=1169
  _globals['_VMDISKRECOVERYPOINTCLUSTERDISCOVERSPEC']._serialized_start=1172
  _globals['_VMDISKRECOVERYPOINTCLUSTERDISCOVERSPEC']._serialized_end=1334
  _globals['_VMRECOVERYPOINTCHANGEDREGIONSCOMPUTESPEC']._serialized_start=1337
  _globals['_VMRECOVERYPOINTCHANGEDREGIONSCOMPUTESPEC']._serialized_end=1528
  _globals['_VOLUMEGROUPDISKRECOVERYPOINTCLUSTERDISCOVERSPEC']._serialized_start=1531
  _globals['_VOLUMEGROUPDISKRECOVERYPOINTCLUSTERDISCOVERSPEC']._serialized_end=1712
  _globals['_VOLUMEGROUPRECOVERYPOINTCHANGEDREGIONSCOMPUTESPEC']._serialized_start=1715
  _globals['_VOLUMEGROUPRECOVERYPOINTCHANGEDREGIONSCOMPUTESPEC']._serialized_end=1924
# @@protoc_insertion_point(module_scope)
