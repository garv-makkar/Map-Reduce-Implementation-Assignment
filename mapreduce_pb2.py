# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mapreduce.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fmapreduce.proto\"\xb9\x01\n\x0eMapTaskRequest\x12\x15\n\rid_for_mapper\x18\x01 \x01(\x05\x12\x14\n\x0cmapper_count\x18\x02 \x01(\x05\x12\x15\n\rreducer_count\x18\x03 \x01(\x05\x12\x18\n\x10iterations_count\x18\x04 \x01(\x05\x12\x0f\n\x07ip_file\x18\x05 \x01(\t\x12\r\n\x05start\x18\x06 \x01(\x05\x12\x0b\n\x03\x65nd\x18\x07 \x01(\x05\x12\x1c\n\tcentroids\x18\x08 \x03(\x0b\x32\t.Centroid\".\n\x0bMapResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"v\n\x11ReduceTaskRequest\x12\x16\n\x0eid_for_reducer\x18\x01 \x01(\x05\x12\x14\n\x0cmapper_count\x18\x02 \x01(\x05\x12\x15\n\rreducer_count\x18\x03 \x01(\x05\x12\x1c\n\tcentroids\x18\x04 \x03(\x0b\x32\t.Centroid\"T\n\x12ReduceTaskResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x1c\n\tcentroids\x18\x03 \x03(\x0b\x32\t.Centroid\"1\n\x17ReceiveKeyValuesRequest\x12\x16\n\x0eid_for_reducer\x18\x01 \x01(\x05\"O\n\x18ReceiveKeyValuesResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\"\n\x0epoints_in_data\x18\x02 \x03(\x0b\x32\n.DataPoint\"\x1f\n\x08\x43\x65ntroid\x12\x13\n\x0b\x63oordinates\x18\x01 \x03(\x01\"3\n\tDataPoint\x12\x16\n\x0eid_of_centroid\x18\x01 \x01(\x05\x12\x0e\n\x06points\x18\x02 \x03(\x01\x32\xbb\x01\n\x0fKMeansMapReduce\x12(\n\x07MapTask\x12\x0f.MapTaskRequest\x1a\x0c.MapResponse\x12\x35\n\nReduceTask\x12\x12.ReduceTaskRequest\x1a\x13.ReduceTaskResponse\x12G\n\x10ReceiveKeyValues\x12\x18.ReceiveKeyValuesRequest\x1a\x19.ReceiveKeyValuesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mapreduce_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_MAPTASKREQUEST']._serialized_start=20
  _globals['_MAPTASKREQUEST']._serialized_end=205
  _globals['_MAPRESPONSE']._serialized_start=207
  _globals['_MAPRESPONSE']._serialized_end=253
  _globals['_REDUCETASKREQUEST']._serialized_start=255
  _globals['_REDUCETASKREQUEST']._serialized_end=373
  _globals['_REDUCETASKRESPONSE']._serialized_start=375
  _globals['_REDUCETASKRESPONSE']._serialized_end=459
  _globals['_RECEIVEKEYVALUESREQUEST']._serialized_start=461
  _globals['_RECEIVEKEYVALUESREQUEST']._serialized_end=510
  _globals['_RECEIVEKEYVALUESRESPONSE']._serialized_start=512
  _globals['_RECEIVEKEYVALUESRESPONSE']._serialized_end=591
  _globals['_CENTROID']._serialized_start=593
  _globals['_CENTROID']._serialized_end=624
  _globals['_DATAPOINT']._serialized_start=626
  _globals['_DATAPOINT']._serialized_end=677
  _globals['_KMEANSMAPREDUCE']._serialized_start=680
  _globals['_KMEANSMAPREDUCE']._serialized_end=867
# @@protoc_insertion_point(module_scope)
