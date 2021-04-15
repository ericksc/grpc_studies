"""
Some custom timer class
"""
import time
from functools import wraps, partial
#from helpers.log_enum import LogType

class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class CatchTime:
    """Some custom timer class"""

    def __init__(self, current_module, function_name, logger_obj):
        self.current_module = current_module
        self.logger_obj = logger_obj
        self.function_name = function_name

    def __enter__(self):
        self.time_ = time.perf_counter() # pylint: disable=attribute-defined-outside-init
        return self

    def __exit__(self, type, value, traceback): # pylint: disable=redefined-builtin
        """Stop the timer, and report the elapsed time"""
        self.time_ = time.perf_counter() - self.time_ # pylint: disable=attribute-defined-outside-init

        current_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime())
        if self.logger_obj is None:
            print('=== Profiling Timestamp: %s|TOOK: %2.5f sec|func:%r|Module: %s|' % (current_time, self.time_, self.function_name, self.current_module))


class Timer:
    """Some custom timer class"""
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        self.elapsed = f"{elapsed_time:0.4f}" # pylint: disable=attribute-defined-outside-init
        self.elapsed_seconds = elapsed_time # pylint: disable=attribute-defined-outside-init
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")

def parametrized(dec):
    """
    To apply parameters to decorator
    """
    def layer(*args, **kwargs):
        def repl(a_f):
            return dec(a_f, *args, **kwargs)
        return repl
    return layer

@parametrized
def timing(a_f, current_module, logger_obj=None):
    """
    timing decorator
    """

    logger_obj =  None

    @wraps(a_f)
    def wrap(*args, **kw):
        t_s = time.perf_counter()
        before_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime())
        result = a_f(*args, **kw)
        t_e = time.perf_counter()
        after_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime())
        if logger_obj is None:
            print('=== Profiling Timestamp| before: %s| after: %s|TOOK: %2.5f sec|func:%r|Module: %s|' % (before_time, after_time, t_e - t_s, a_f.__name__, current_module))
        else:
            logger_obj(msg='[time][Timing][Profiling Timestamp] %s|TOOK: %2.5f sec|func:%r|Module: %s|' % (current_time, t_e - t_s, a_f.__name__, current_module))
        return result
    return wrap

if __name__ == '__main__':
    @timing(current_module=__file__)  # pylint: disable=no-value-for-parameter
    def f_example(a_parameter):
        """
        just an example
        """
        a_i = 0
        for _ in range(a_parameter):
            a_i += 1
        return a_i

    f_example(int(1e6))


    def a_function(a_parameter):
        """
        just an example
        """
        a_i = 0
        for _ in range(a_parameter):
            a_i += 1
        return a_i


    with CatchTime(current_module=__file__, function_name='example', logger_obj=None) as my_time:
        ARESULT = a_function(int(1e6))

    print(ARESULT)
