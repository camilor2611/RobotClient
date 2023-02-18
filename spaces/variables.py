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
    """This module is Singleton"""
    __instance = None
    __variables = {
        "fatal_error": False
    }
    reserved_names = ['settings', 'fatal_error']

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(MemoryVariables, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __get_obj_path(self, path_list: list, make_path_recursive=True):
        """This method searches a path through the argument "path_list" into variables.

        :param path_list: this argument contains all parts of a path.
        :type path_list: list
        :param make_path_recursive: if this argument is true create all parts of a path. The default vaule is True.
        :raises NoExistPath: if there is not exist any path raise this error.
        :type make_path_recursive: bool, optional
        :return: a string like that "part_one/part_two".
        """
        current_path = self.__variables
        current_path_str = ""
        for path_key in path_list:
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
        """This method defines a new variable, if the path does not exist, all parts of the path will be created..
        besides, if value is a dictionary it could access with path "path_a/key_dict".
        
        :param key: the key is ubication where it will be saved the value, this key must be similar to "path_a/path_b".
        :type key: str
        :param value: is the value that it is saved in the key.
        :type key: obj
        """
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

    def get_fatal_error(self) -> bool:

        return self.__variables['fatal_error']

    def set_fatal_error(self, value: bool) -> None:
        self.__variables['fatal_error'] = value
