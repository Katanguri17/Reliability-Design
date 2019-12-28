import logging
import functools
import time

"""Logger module created by Kamil Kaliś"""


def logger_setup(logger_file="results.log"):
    """Sets up the logger.
    Usage:
        1. With wrapper @log_exec_time
        2. Set logger within module as:
            2.1 log = get_logger('exec_time.log')
            2.2 use 'log' variable to use logger and write them to file"""

    logformat = "[%(asctime)s %(levelname)s] %(message)s"
    dateformat = "%d-%m-%y %H:%M:%S"
    logger = logging.getLogger(logger_file)
    formatter = logging.Formatter(logformat)
    formatter.datefmt = dateformat
    fh = logging.FileHandler(logger_file, mode="a")
    fh.setFormatter(formatter)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.propagate = False


def log_to_file(func=None, logger_file='results.log'):
    def log_exec_time(original_func):
        """Wrapper for logging execution time of marked function.
        Usage:
        Add adnotation above function: '@log_to_file(<logger_file.log>)'"""

        @functools.wraps(original_func)
        def wrapper(*args, **kwargs):
            log = logging.getLogger(logger_file)
            log.info(f"Running {original_func.__name__}...")
            start_time = time.time()
            result = original_func(*args, **kwargs)
            exec_time = time.time() - start_time
            log.info(f"Function {original_func.__name__} finished in {exec_time}s")
            return result

        return wrapper

    return log_exec_time if func is None else log_exec_time(func)


def get_logger(logger_file='results.log'):
    return logging.getLogger(logger_file)
