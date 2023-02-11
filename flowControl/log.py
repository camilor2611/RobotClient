class CustomLogger(object):
    __instance = None
    __function_print = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(CustomLogger, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def set_print(self, function_):
        self.__function_print = function_

    def info(self, msg):
        if self.__function_print is not None:
            self.__function_print(msg)
        else:
            print(msg)

custom_logger = CustomLogger()
