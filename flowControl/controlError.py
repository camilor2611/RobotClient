from datetime import datetime
from types import MethodType
from ..spaces.variables import MemoryVariables


class ControlExecutionAsyc():
    def __init__(self, print_function) -> None:
        self.variables = MemoryVariables()
        self.print_function = print_function
        self.__format_date = "%d/%m/%Y %H:%M:%S"
        self.__format_hour = "%H:%M:%S.%f"
        self.data_message_default = {
            "error": "[Fatal Error] {function_name} - wasted time: {wasted_time} now = {now}",
            "success": "[Success] {function_name} - wasted time: {wasted_time} now = {now}",
            "warning": "[Warning] {function_name} - wasted time: {wasted_time} now = {now}"
        }

    def __call__(self, function_):
        async def wrapped(*args, **kwargs):
            try:
                if not self.variables.get_fatal_error():
                    start_time = datetime.now()
                    status, value = await function_(*args, **kwargs)
                    end_time = datetime.now()
                    wasted_time_datetime = (
                        datetime.strptime(str(end_time - start_time), self.__format_hour)
                        if end_time != start_time else
                        datetime.strptime("00:00:00.000000", self.__format_hour)
                    )
                    wasted_time = wasted_time_datetime.strftime(self.__format_hour)
                    self.print_function(self.data_message_default[status].format(
                        function_name=function_.__qualname__,
                        wasted_time=wasted_time,
                        now=end_time.strftime(self.__format_date)
                        )
                    )
                    fatal_error = True if status == 'error' else False
                    self.variables.set_fatal_error(fatal_error)
                    return value
            except Exception as e:
                self.print_function(f"Error: {str(e)}")
                self.variables.set_fatal_error(True)
        return wrapped
        
    def __get__(self, instance, cls):
        return self if instance is None else MethodType(self, instance)
