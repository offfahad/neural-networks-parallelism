#load_balancer_example.py
#task_distribution.py
#parallel_processing.py
#multi_process_load_balancing.py
#distributed_task_execution.py

import multiprocessing
import time
import random

# Define more computationally intensive tasks
def coding_task_1():
    # Example: Simulate a computationally intensive task
    result = 0
    for _ in range(10**7):
        result += 1
    return f"Result from Task 1: {result}"

def coding_task_2():
    # Example: Simulate another computationally intensive task
    # The entire expression is effectively summing the squares of numbers from 0 to 999,999.
    result = sum(i**2 for i in range(10**7))
    return f"Result from Task 2: {result}"

def coding_task_3():
    # Example: Simulate another computationally intensive task
    result = sum(i**3 for i in range(10**7))
    return f"Result from Task 3: {result}"


tasks = [coding_task_1, coding_task_2, coding_task_3]


def worker(task_queue, result_queue):
    while True:
        task_func = task_queue.get()
        if task_func is None:
            break

        result = task_func()
        result_queue.put(result)

def load_balancer(task_functions, num_workers):
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    # Start worker processes
    workers = [multiprocessing.Process(target=worker, args=(task_queue, result_queue)) for _ in range(num_workers)]
    for w in workers:
        w.start()

    # Distribute tasks to workers
    for task_func in task_functions:
        task_queue.put(task_func)

    # Signal workers to stop
    for _ in range(num_workers):
        task_queue.put(None)

    # Wait for all workers to finish
    for w in workers:
        w.join()

    # Collect results
    results = []
    while not result_queue.empty():
        result = result_queue.get()
        results.append(result)

    return results

if __name__ == "__main__":
    # Measure execution time without load balancing
    start_time = time.time()

    # Perform tasks without load balancing
    results_without_load_balancing = [task() for task in tasks]

    end_time = time.time()
    execution_time_without_load_balancing = end_time - start_time

    # Print results and execution time  
    print("Results without load balancing:")
    for result in results_without_load_balancing:
        print(result)

    print("Execution time without load balancing:", execution_time_without_load_balancing)

    # Measure execution time with load balancing
    start_time = time.time()

    # Perform tasks with load balancing
    results_with_load_balancing = load_balancer(tasks, num_workers=3)

    end_time = time.time()
    execution_time_with_load_balancing = end_time - start_time

    # Print results and execution time
    print("\nResults with load balancing:")
    for result in results_with_load_balancing:
        print(result)

    print("Execution time with load balancing:", execution_time_with_load_balancing)