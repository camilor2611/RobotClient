from types import MethodType
from functools import wraps
from schema import Schema
import inspect


class ControlSchemaAsyncError(Exception):
    """Exception class from which every exception in this library will derive.
    It enables other projects using this library to catch all errors coming
    from the library with a single "except" statement
    """
    pass


class NotIsSchema(ControlSchemaAsyncError):
    """Variable is not DataFrame or Series"""
    pass


class FailedSchema(ControlSchemaAsyncError):
    """"""
    pass


class ControlSchemaAsync():
    def __init__(self, schema, arg_with_schema) -> None:
        self.schema = schema
        self.arg_with_schema = arg_with_schema
        if not isinstance(schema, Schema):
            raise NotIsSchema("The schema is incorrect")

    def __call__(self, function_):
        @wraps(function_)
        async def wrapped(*args, **kwargs):
            args_names_function = inspect.getfullargspec(function_).args
            index = args_names_function.index(self.arg_with_schema)
            if self.schema.is_valid(args[index]):
                status, value = await function_(*args, **kwargs)
                return status, value
            else:
                raise FailedSchema(f"The {self.arg_with_schema} does not have a valid schema in {function_.__name__}")
        return wrapped

    def __get__(self, instance, _):
        return self if instance is None else MethodType(self, instance)
