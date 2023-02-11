from abc import ABCMeta, abstractmethod


class ITask(metaclass=ABCMeta):
    """The taks interface, that all tasks will implement"""

    @abstractmethod
    def execute(self):
        pass


class CAssistant:
    def __init__(self):
        self.__task = {}

    def register(self, task_name, task):
        """Register Task in the Invoker"""
        self.__task[task_name] = task

    def execute(self, task_name, *args, **kwargs):
        """Execute any registered Task"""
        if task_name in self.__task.keys():
            self.__task[task_name].execute(*args, **kwargs)
        else:
            print(f"Task [{task_name}] not recognised")
