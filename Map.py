import os
import mapreduce_pb2_grpc as pb2_grpc
import mapreduce_pb2 as pb2
from concurrent import futures
import grpc


def euclidean_distance(point1, point2):
    return sum((a - b) ** 2 for a, b in zip(point1, point2)) ** 0.5


def read_points_from_file(file_path, start, end):
    points = []
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if start <= i < end:
                points.append(list(map(float, line.strip().split(','))))
    return points


def write_output(mapped_points, output_directory, id_for_mapper, partition_id):
    output_path = f'{
        output_directory}/M{id_for_mapper}/partition_{partition_id}.txt'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as file:
        for id_of_centroid, point in mapped_points:
            file.write(f'{id_of_centroid}\t{point}\n')


class Map(pb2_grpc.KMeansMapReduceServicer):

    def init_file_attributes(self):
        self.ip_file = None
        self.start = 0
        self.curr_index = 0
        self.end = 0

    def init_mapper_attributes(self):
        self.id_for_mapper = 0
        self.centroids = None
        self.M = 0
        self.updated_centroids = {}
        self.R = 0
        self.mapper_points = None
        self.partitions = []

    def __init__(self):
        self.init_file_attributes()
        self.init_mapper_attributes()

    def MapTask(self, request, context):
        self.initialize_mapper(request)
        points = read_points_from_file(
            self.ip_file, self.start, self.end)
        self.mapper_points = self.map_points_to_centroids(points)
        self.partition_points()
        return pb2.MapResponse(status="SUCCESS", message="Map function completed successfully")

    def initialize_mapper(self, request):
        self.start = request.start
        self.end = request.end
        self.id_for_mapper = request.id_for_mapper
        self.ip_file = request.ip_file
        self.centroids = []
        for centroid in request.centroids:
            self.centroids.append(list(centroid.coordinates))
        self.R = request.reducer_count
        self.partitions = []
        for i in range(self.R):
            self.partitions.append([])

    def map_points_to_centroids(self, points):
        return [(self.find_nearest_centroid(point), point) for point in points]

    def find_nearest_centroid(self, point):
        distances = [euclidean_distance(point, centroid)
                     for centroid in self.centroids]
        return distances.index(min(distances))

    def partition_points(self):
        for id_of_centroid, point in self.mapper_points:
            self.partitions[id_of_centroid % self.R].append((id_of_centroid, point))
        for i, partition in enumerate(self.partitions):
            write_output(partition, 'Mappers', self.id_for_mapper, i)

    def ReceiveKeyValues(self, request, context):
        id_for_reducer = request.id_for_reducer
        key_values = self.prepare_key_values_for_reducer(id_for_reducer)
        return pb2.ReceiveKeyValuesResponse(success=True, points_in_data=key_values)

    def prepare_key_values_for_reducer(self, id_for_reducer):
        arr = []
        for i, partition in enumerate(self.partitions):
            if i % self.R == id_for_reducer:
                for id_of_centroid, point in partition:
                    arr.append(pb2.DataPoint(
                        id_of_centroid=id_of_centroid, points=point))
        return arr


def handle_server(server, port):
    server.add_insecure_port(port)
    server.start()
    server.wait_for_termination()


def serve(i=0, r=2):
    import random
    import sys
    if random.randint(1, 10) <= r:
        sys.exit()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_KMeansMapReduceServicer_to_server(Map(), server)
    print(f"Mapper server started, listening on port {f'[::]:400{i}'}")
    handle_server(server, f'[::]:400{i}')


if __name__ == '__main__':
    import sys
    serve(*map(int, sys.argv[1:]))
