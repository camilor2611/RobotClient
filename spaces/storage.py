import os


class LocalStorage():
    def __init__(self, path_process):
        self.__path_process = os.path.normpath(path_process)
        
    def load_local_settings(self) -> dict():
        pass

    def abspath_file_input(self, name):
        pass

    def abspath_file_output(self, name):
        pass

    def abspath_file_temp(self, name):
        pass
