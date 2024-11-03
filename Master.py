# Import necessary libraries
import os
import sys
import multiprocessing
import random
import time

# Import the Map and Reduce modules
import Map
import Reduce

# Import the gRPC generated classes
import mapreduce_pb2 as pb2
import mapreduce_pb2_grpc as pb2_grpc
import grpc


Mappers_dict = {}
Reducers_dict = {}
mapper_count = 0
reducer_count = 0
iterations_count = 0


def launchProcess(num, target):
    for i in range(num):
        process = multiprocessing.Process(target=target, args=(i, -1))
        process.start()
        time.sleep(0.5)
        if not process.is_alive():
            print(f"Process {i} terminated")
            process = multiprocessing.Process(target=target, args=(i, -1))
            process.start()
        else:
            print(f"Process {i} running")
        (Mappers_dict if target == Map.serve else Reducers_dict)[i] = process


def launchMappersAndReducers():
    launchProcess(mapper_count, Map.serve)
    launchProcess(reducer_count, Reduce.serve)


def log_and_write(message):
    with open("dump.txt", "a") as file:
        print(message)
        file.write(message + "\n")


def check_convergence(centroids, final_centroids):
    a = sorted(centroids)
    b = sorted(final_centroids)
    return a == b


def perform_map_tasks():
    log_and_write("Map tasks started...")
    call_mappers(centroids)


def perform_reduce_tasks():
    log_and_write("Reduce tasks started...")
    new = call_reducers(centroids)
    new = [tuple(centroid.coordinates) for centroid in new]
    return new


def update_centroids_and_log(new):
    log_and_write(f"New centroids: {new}")
    with open("dump.txt", "a") as file:
        for centroid in new:
            file.write(','.join(map(str, centroid)) + '\n')
    return new


def check_convergence_and_terminate(new, iteration):
    if check_convergence(centroids, new):
        log_and_write(f"Convergence reached!! Iteration {iteration}")
        terminate_all()
        return True
    return False


def terminate(dict):
    for i in dict:
        dict[i].terminate()


def terminate_all():
    terminate(Mappers_dict)
    terminate(Reducers_dict)


def lessgooo():
    global centroids
    for iteration in range(iterations_count):
        launchMappersAndReducers()
        log_and_write(f"Iteration {iteration}")
        perform_map_tasks()
        new = perform_reduce_tasks()
        new = update_centroids_and_log(new)
        if check_convergence_and_terminate(new, iteration):
            break
        else:
            centroids = new
        terminate_all()


def calculate_indices(mapper_count, indices_per_mapper, remainder, i):
    start = i * indices_per_mapper
    end = start + indices_per_mapper
    if i == mapper_count - 1:
        end += remainder
    return start, end


def create_centroid_objects(centroids):
    return [pb2.Centroid(coordinates=centroid) for centroid in centroids]


def send_mapper_request(i, centroids, start, end):
    centroid_objects = create_centroid_objects(centroids)
    request = pb2.MapTaskRequest(
        id_for_mapper=i,
        mapper_count=mapper_count,
        reducer_count=reducer_count,
        iterations_count=iterations_count,
        ip_file=ip_file,
        start=start,
        end=end,
        centroids=centroid_objects
    )
    map_id = request.id_for_mapper
    with grpc.insecure_channel(f'localhost:400{map_id}') as channel:
        stub = pb2_grpc.KMeansMapReduceStub(channel)
        response = stub.MapTask(request)
        log_and_write(f"Mapper {map_id} response: {response.message}")


def call_mappers(centroids):
    indices_per_mapper = len(points_in_data) // mapper_count
    remainder = len(points_in_data) % mapper_count
    for i in range(mapper_count):
        start, end = calculate_indices(
            mapper_count, indices_per_mapper, remainder, i)
        send_mapper_request(i, centroids, start, end)


def prepare_and_send_reduce_request(i, centroids):
    centroid_objects = create_centroid_objects(centroids)
    request = pb2.ReduceTaskRequest(
        id_for_reducer=i,
        mapper_count=mapper_count,
        reducer_count=reducer_count,
        centroids=centroid_objects
    )
    return call_reducer(request)


def call_reducer(request):
    reduce_id = request.id_for_reducer
    with grpc.insecure_channel(f'localhost:500{reduce_id}') as channel:
        stub = pb2_grpc.KMeansMapReduceStub(channel)
        response = stub.ReduceTask(request)
        log_and_write(f"Reducer {reduce_id} response: {response.message}")
        return response.centroids


def call_reducers(centroids):
    final_reduce_output = []
    for i in range(reducer_count):
        result = prepare_and_send_reduce_request(i, centroids)
        final_reduce_output.extend(result)
    return final_reduce_output


def file_exists(file_path):
    return os.path.exists(file_path)


def parse_centroids(lines, delimiter=None):
    try:
        return [tuple(map(float, line.strip().split(delimiter))) for line in lines]
    except ValueError:
        return None


def read_centroid_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Try parsing with default whitespace
        centroids = parse_centroids(lines)
        if centroids is None:
            # Try parsing with comma as delimiter
            centroids = parse_centroids(lines, ',')
        if centroids is None:
            print("Some problem occured, maybe invalid file format")
        return centroids


def load_centroids(file_path):
    if file_exists(file_path):
        return read_centroid_data(file_path)
    print("Error - No File exists with this name")
    return None


def user_input():
    M = int(input("Number of mappers (M): "))
    R = int(input("Number of reducers (R): "))
    N = int(input("Number of iterations: "))
    C = int(input("Number of centroids (K): "))
    return M, R, N, C


def sleep_for_some_time():
    time.sleep(2)


def make_data_points():
    points_in_data = []
    with open(ip_file, 'r') as file:
        for line in file:
            data_point = tuple(map(float, line.strip().split(',')))
            points_in_data.append(data_point)
    return points_in_data


def log_initial_centroids(centroids):
    with open("dump.txt", "a") as file:
        file.write(f"Initial centroids: {centroids}\n")


ip_file = "points2.txt"

if __name__ == "__main__":

    mapper_count, reducer_count, iterations_count, num_centroids = user_input()

    sleep_for_some_time()

    points_in_data = make_data_points()

    centroids = random.sample(points_in_data, num_centroids)

    centroids = sorted(centroids, key=lambda x: x[0])

    log_initial_centroids(centroids)

    lessgooo()

    # save the final centroids to a file
    with open("centroids.txt", "w") as file:
        for centroid in centroids:
            file.write(','.join(map(str, centroid)) + '\n')
