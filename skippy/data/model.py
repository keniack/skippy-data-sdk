from typing import List


class DataFile:
    content: str
    name: str
    size: int

    def __init__(self, size: int, name: str, content: str):
        self.size = size
        self.name = name
        self.content = content


class DataArtifact:
    data: List[DataFile]

    def __init__(self, data: List[DataFile]):
        self.data = data
