import grpc
import os
from concurrent import futures
import mapreduce_pb2 as pb2
import mapreduce_pb2_grpc as pb2_grpc
import random
import sys


def save_centroids(centroids, id_for_reducer):
    path = f"Reducers/Reducer{id_for_reducer}.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as file:
        for id_of_centroid, coordinates in centroids.items():
            coordinates_str = ' '.join(map(str, coordinates))
            file.write(f"{id_of_centroid} {coordinates_str}\n")


class Reducer(pb2_grpc.KMeansMapReduceServicer):
    def __init__(self):
        self.id_for_reducer = 0
        self.centroids = []
        self.updated_centroids = {}
        self.allocated_data = []
        self.mapper_count = 0
        self.reducer_count = 0

    def ReduceTask(self, request, context):
        self.initialize_reducer(request)
        updated_centroids = self.process_data_points()
        save_centroids(updated_centroids, self.id_for_reducer)
        return pb2.ReduceTaskResponse(success=True, message=f"Reducer {self.id_for_reducer} completed",
                                      centroids=[pb2.Centroid(coordinates=coords) for coords in updated_centroids.values()])

    def initialize_reducer(self, request):
        self.id_for_reducer = request.id_for_reducer
        self.mapper_count = request.mapper_count
        self.reducer_count = request.reducer_count
        self.centroids = []
        for centroid in request.centroids:
            self.centroids.append(list(centroid.coordinates))

    def process_data_points(self):
        self.receive_data_points()
        return self.calculate_updated_centroids()

    def receive_data_points(self):
        request = pb2.ReceiveKeyValuesRequest(id_for_reducer=self.id_for_reducer)
        i = 0
        while (i < self.mapper_count):
            with grpc.insecure_channel(f'localhost:400{i}') as channel:
                response = pb2_grpc.KMeansMapReduceStub(
                    channel).ReceiveKeyValues(request)
                self.allocated_data.extend(
                    (d.id_of_centroid, d.points) for d in response.points_in_data)
            i += 1

    def calculate_updated_centroids(self):
        sorted_data = self.sort_data_by_centroid()
        updated_centroids = {}
        for id_of_centroid, points in sorted_data.items():
            if points:
                updated_centroids[id_of_centroid] = self.update_centroid(points)
            else:
                updated_centroids[id_of_centroid] = self.centroids[id_of_centroid]
        return updated_centroids

    def sort_data_by_centroid(self):
        sorted_data = {}
        for id_of_centroid, point in self.allocated_data:
            if id_of_centroid not in sorted_data:
                sorted_data[id_of_centroid] = []
            sorted_data[id_of_centroid].append(point)
        return sorted_data

    def update_centroid(self, points):
        num_points = len(points)
        num_dimensions = len(points[0])
        centroid = [sum(point[dim] for point in points) /
                    num_points for dim in range(num_dimensions)]
        return centroid


def handle_server(server, port):
    server.add_insecure_port(port)
    server.start()
    server.wait_for_termination()


def serve(i=0, r=2):
    if random.randint(1, 10) <= r:
        sys.exit()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_KMeansMapReduceServicer_to_server(Reducer(), server)
    print(f"Reducer server started, listening on port {f'[::]:500{i}'}")
    handle_server(server, f'[::]:500{i}')


if __name__ == '__main__':
    serve()
