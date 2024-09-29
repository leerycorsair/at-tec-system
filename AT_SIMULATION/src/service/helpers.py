from contextlib import contextmanager


@contextmanager
def handle_rollback(cleanup_func, *args, **kwargs):
    try:
        yield
    except Exception as e:
        cleanup_func(*args, **kwargs)
        raise e
