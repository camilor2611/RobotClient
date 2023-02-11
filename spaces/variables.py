class MemoryVariablesError(Exception):
    """Exception class from which every exception in this library will derive.
    It enables other projects using this library to catch all errors coming
    from the library with a single "except" statement
    """
    pass


class NoExistPath(MemoryVariablesError):
    """A specific error"""
    pass


class ReservedName(MemoryVariablesError):
    """Reserved Name"""
    pass


class MemoryVariables(object):
    __instance = None
    __variables = {
        "fatal_error": False
    }
    reserved_names = ['settings', 'fatal_error']

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(MemoryVariables, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __get_obj_path(self, list_path: list, make_path_recursive=True):
        current_path = self.__variables
        current_path_str = ""
        for path_key in list_path:
            current_path_str = f"{current_path_str}/{path_key}"
            if path_key in current_path:
                current_path = current_path[path_key]
            elif make_path_recursive:
                current_path[path_key] = dict()
                current_path = current_path[path_key]
            else:
                raise NoExistPath(f"Not exist path '{current_path_str[1:]}' in MemoryVariables")
        return current_path

    def new(self, key: str, value):
        parts_key = key.split("/")
        if parts_key[0] in self.reserved_names:
            raise ReservedName("The first part of path cannot contain reserved names")
        paths_key = parts_key[:-1]
        save_as = parts_key[-1]
        current_path = self.__get_obj_path(paths_key)
        current_path[save_as] = value
        return True

    def get(self, key: str):
        parts_key = key.split("/")
        var = self.__get_obj_path(parts_key, make_path_recursive=False)
        return var

    def get_fatal_error(self,) -> bool:
        return self.__variables['fatal_error']

    def set_fatal_error(self, value: bool) -> None:
        self.__variables['fatal_error'] = value
