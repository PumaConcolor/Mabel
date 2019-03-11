import os
import zipfile
import tarfile
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


class FolderConnector(DataConnector):

    def __init__(self, path):
        super().__init__(path)

    def getFilesList(self):
        return [os.path.join(dir, file) for dir, _, file in os.walk(self._path)]

    def getFile(self, path):
        path = os.path.join(self._path, path)
        with open(path, 'rb') as binaryFile:
            file = binaryFile.read()
        return file


class ZipConnector(DataConnector):

    def __init__(self, path):
        super().__init__(path)

    def getFilesList(self):
        with zipfile.ZipFile(self._path) as archive:
            files = archive.namelist()
        return files

    def getFile(self, path):
        with zipfile.ZipFile(self._path) as archive:
            file = archive.open(path)
            file = file.read()
        return file


class TarConnector(DataConnector):

    def __init__(self, path, mode='r'):
        super().__init__(path)
        self._mode = mode

    def getFilesList(self):
        files = []
        with tarfile.open(self._path, self._mode) as archive:
            for file in archive.getmembers():
                if file.isfile():
                    files.append(file.path)
        return files

    def getFile(self, path):
        with tarfile.open(self._path, self._mode) as archive:
            file = archive.extractfile(path)
            file = file.read()
        return file


class TarGzConnector(TarConnector):

    def __init__(self, path):
        super().__init__(path, 'r:gz')


class TarBz2Connector(TarConnector):

    def __init__(self, path):
        super().__init__(path, 'r:bz2')


class TarXzConnector(TarConnector):

    def __init__(self, path):
        super().__init__(path, 'r:xz')
