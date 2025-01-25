import functools
import inspect
import types


class Error(Exception):
    def __init__(self, error: str, status_code: int, http_error: str, **kwargs):
        super().__init__(error)
        self.error = error
        self.http_error = http_error
        self.status_code = status_code
        self.context = kwargs

    def to_dict(self):
        return {
            "error": str(self),
            "status_code": self.status_code,
            **self.context,
        }


class InternalServerError(Error):
    def __init__(self, error: str, **kwargs):
        super().__init__(
            error,
            status_code=500,
            http_error="Internal Server Error",
            **kwargs,
        )


class BadRequestError(Error):
    def __init__(self, error: str, **kwargs):
        super().__init__(
            error,
            status_code=400,
            http_error="Bad Request Error",
            **kwargs,
        )


class AuthError(Error):
    def __init__(self, error: str, **kwargs):
        super().__init__(
            error,
            status_code=401,
            http_error="Authorization Error",
            **kwargs,
        )


class ForbiddenError(Error):
    def __init__(self, error: str, **kwargs):
        super().__init__(
            error,
            status_code=403,
            http_error="Forbidden Error",
            **kwargs,
        )


class NotFoundError(Error):
    def __init__(self, error: str, **kwargs):
        super().__init__(
            error,
            status_code=404,
            http_error="Not Found Error",
            **kwargs,
        )


def wrap_exceptions():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Error as e:
                raise e
            except Exception as e:
                class_name = None
                if len(args) > 0:
                    instance_or_cls = args[0]
                    if inspect.isclass(instance_or_cls):
                        class_name = instance_or_cls.__name__
                    elif hasattr(instance_or_cls, "__class__"):
                        class_name = instance_or_cls.__class__.__name__

                method_name = func.__name__
                context = {"class_name": class_name, "method_name": method_name}

                raise InternalServerError(
                    f"Unhandled exception in {class_name}.{method_name}: {str(e)}",
                    **context,
                ) from e

        return wrapper

    return decorator


class WrapMethodsMeta(type):
    def __new__(cls, name, bases, dct):
        for attr_name, attr_value in dct.items():
            if isinstance(attr_value, types.FunctionType):
                dct[attr_name] = wrap_exceptions()(attr_value)
        return super().__new__(cls, name, bases, dct)
