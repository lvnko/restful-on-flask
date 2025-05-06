# performance.py
from datetime import datetime
# This file will be used for server logging and performance monitoring.
class Performance():
    def __init__(self, fpath):
        self.fpath = fpath

    def log(self, g):
        with open(self.fpath, "a") as f:
            uuid = g.uuid
            status_code = g.status_code
            response_time = (g.end - g.start) * 1000
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {uuid}, {status_code}, {response_time:.3f}\n")

# import logging
# import time
# from functools import wraps

# # Basic configuration for logging
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     handlers=[logging.FileHandler("server_performance.log"),
#                               logging.StreamHandler()])

# logger = logging.getLogger(__name__)

# def log_performance(func):
#     """
#     A decorator to log the execution time of a function.
#     """
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         execution_time = end_time - start_time
#         logger.info(f"Function {func.__name__} executed in {execution_time:.4f} seconds")
#         return result
#     return wrapper

# def setup_logging():
#     """
#     Call this function to ensure logging is configured.
#     Can be expanded with more sophisticated configuration if needed.
#     """
#     logger.info("Performance logging initialized.")

# if __name__ == '__main__':
#     # Example usage of the logger and decorator
#     setup_logging()

#     @log_performance
#     def example_function(delay):
#         logger.info(f"Running example_function with delay: {delay}")
#         time.sleep(delay)
#         logger.info("example_function finished.")
#         return f"Completed with delay {delay}"

#     example_function(1)
#     example_function(0.5)
