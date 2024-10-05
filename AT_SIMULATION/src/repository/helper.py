from functools import wraps
from sqlalchemy.exc import SQLAlchemyError


def handle_sqlalchemy_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            method_name = func.__name__
            raise RuntimeError(f"Failed to execute {method_name}: {e}") from e

    return wrapper
