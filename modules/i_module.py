from abc import ABCMeta, abstractmethod


class IModule:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, cmd, client):
        raise NotImplementedError
