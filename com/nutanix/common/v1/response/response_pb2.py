# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: com/nutanix/common/v1/response/response.proto
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
    'com/nutanix/common/v1/response/response.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.nutanix.common.v1.config import config_pb2 as com_dot_nutanix_dot_common_dot_v1_dot_config_dot_config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-com/nutanix/common/v1/response/response.proto\x12\x1e\x63om.nutanix.common.v1.response\x1a)com/nutanix/common/v1/config/config.proto\"&\n\x07\x41piLink\x12\r\n\x04href\x18\xe9\x07 \x01(\t\x12\x0c\n\x03rel\x18\xea\x07 \x01(\t\"\x99\x02\n\x13\x41piResponseMetadata\x12\x32\n\x05\x66lags\x18\xe9\x07 \x03(\x0b\x32\".com.nutanix.common.v1.config.Flag\x12\x37\n\x05links\x18\xea\x07 \x03(\x0b\x32\'.com.nutanix.common.v1.response.ApiLink\x12 \n\x17total_available_results\x18\xeb\x07 \x01(\x05\x12\x38\n\x08messages\x18\xec\x07 \x03(\x0b\x32%.com.nutanix.common.v1.config.Message\x12\x39\n\nextra_info\x18\xed\x07 \x03(\x0b\x32$.com.nutanix.common.v1.config.KVPairBB\n\x1e\x63om.nutanix.common.v1.responseP\x01Z\x1e\x63om/nutanix/common/v1/responseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.nutanix.common.v1.response.response_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\036com.nutanix.common.v1.responseP\001Z\036com/nutanix/common/v1/response'
  _globals['_APILINK']._serialized_start=124
  _globals['_APILINK']._serialized_end=162
  _globals['_APIRESPONSEMETADATA']._serialized_start=165
  _globals['_APIRESPONSEMETADATA']._serialized_end=446
# @@protoc_insertion_point(module_scope)
