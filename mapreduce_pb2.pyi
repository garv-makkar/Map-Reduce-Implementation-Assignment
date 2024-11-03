from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapTaskRequest(_message.Message):
    __slots__ = ("id_for_mapper", "mapper_count", "reducer_count", "iterations_count", "ip_file", "start", "end", "centroids")
    ID_FOR_MAPPER_FIELD_NUMBER: _ClassVar[int]
    MAPPER_COUNT_FIELD_NUMBER: _ClassVar[int]
    REDUCER_COUNT_FIELD_NUMBER: _ClassVar[int]
    ITERATIONS_COUNT_FIELD_NUMBER: _ClassVar[int]
    IP_FILE_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    CENTROIDS_FIELD_NUMBER: _ClassVar[int]
    id_for_mapper: int
    mapper_count: int
    reducer_count: int
    iterations_count: int
    ip_file: str
    start: int
    end: int
    centroids: _containers.RepeatedCompositeFieldContainer[Centroid]
    def __init__(self, id_for_mapper: _Optional[int] = ..., mapper_count: _Optional[int] = ..., reducer_count: _Optional[int] = ..., iterations_count: _Optional[int] = ..., ip_file: _Optional[str] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., centroids: _Optional[_Iterable[_Union[Centroid, _Mapping]]] = ...) -> None: ...

class MapResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    def __init__(self, status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class ReduceTaskRequest(_message.Message):
    __slots__ = ("id_for_reducer", "mapper_count", "reducer_count", "centroids")
    ID_FOR_REDUCER_FIELD_NUMBER: _ClassVar[int]
    MAPPER_COUNT_FIELD_NUMBER: _ClassVar[int]
    REDUCER_COUNT_FIELD_NUMBER: _ClassVar[int]
    CENTROIDS_FIELD_NUMBER: _ClassVar[int]
    id_for_reducer: int
    mapper_count: int
    reducer_count: int
    centroids: _containers.RepeatedCompositeFieldContainer[Centroid]
    def __init__(self, id_for_reducer: _Optional[int] = ..., mapper_count: _Optional[int] = ..., reducer_count: _Optional[int] = ..., centroids: _Optional[_Iterable[_Union[Centroid, _Mapping]]] = ...) -> None: ...

class ReduceTaskResponse(_message.Message):
    __slots__ = ("success", "message", "centroids")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CENTROIDS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    centroids: _containers.RepeatedCompositeFieldContainer[Centroid]
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., centroids: _Optional[_Iterable[_Union[Centroid, _Mapping]]] = ...) -> None: ...

class ReceiveKeyValuesRequest(_message.Message):
    __slots__ = ("id_for_reducer",)
    ID_FOR_REDUCER_FIELD_NUMBER: _ClassVar[int]
    id_for_reducer: int
    def __init__(self, id_for_reducer: _Optional[int] = ...) -> None: ...

class ReceiveKeyValuesResponse(_message.Message):
    __slots__ = ("success", "points_in_data")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    POINTS_IN_DATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    points_in_data: _containers.RepeatedCompositeFieldContainer[DataPoint]
    def __init__(self, success: bool = ..., points_in_data: _Optional[_Iterable[_Union[DataPoint, _Mapping]]] = ...) -> None: ...

class Centroid(_message.Message):
    __slots__ = ("coordinates",)
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    coordinates: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, coordinates: _Optional[_Iterable[float]] = ...) -> None: ...

class DataPoint(_message.Message):
    __slots__ = ("id_of_centroid", "points")
    ID_OF_CENTROID_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    id_of_centroid: int
    points: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, id_of_centroid: _Optional[int] = ..., points: _Optional[_Iterable[float]] = ...) -> None: ...
