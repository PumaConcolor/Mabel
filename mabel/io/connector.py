from abc import ABC, abstractmethod


class DataConnector(ABC):
    def __init__(self, path):
        self._path = path

    @abstractmethod
    def getFilesList(self):
        pass

    @abstractmethod
    def getFile(self, path):
        pass
