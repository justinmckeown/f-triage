import typing
from datetime import datetime

class HashMatch:
    def __init__(self, hash_list_name: str, hash: str, file_name: str, file_path: str) -> None:
        self.hash_list_name: str = hash_list_name
        self.hash = hash
        self.file_name: str = file_name
        self.file_path: str = file_path
        self.timestamp_found = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S.%f")

class UncheckedFiles:
    def __init__(self, file_name: str, location: str, reason: str) -> None:
        self.file_name = file_name
        self.location = location
        self.reason = reason
        self.timestamp = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S.%f")
