from abc import ABC, abstractmethod


class DataConnector(ABC):

    @abstractmethod
    def getFilesList(self, path):
        pass

    @abstractmethod
    def getFile(self, path):
        pass
