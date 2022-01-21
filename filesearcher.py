import logging
from operator import truediv
import os
import sys
import platform
import hashlib
from datetime import datetime
import typing
from xmlrpc.client import boolean
from datamodels import HashMatch

logger = logging.getLogger()

class FileSearcher:
    def __init__(self, target_dir: str, save_dir: str, hash_dir: str, image_only: bool = False) -> None:
        self.target_dir = target_dir
        self.save_dir = save_dir
        self.hash_dir = hash_dir
        self.timestamps: typing.Dict[str, str] = {'start': (datetime.now()).strftime("%Y/%m/%d, %H:%M:%S") , 'finish': ''}
        self.hashes: typing.List[tuple] = [] 
        self.matches: typing.List[HashMatch] = []
        self.image_only_search: bool = image_only
        self.IMG_FILE_TYPES = ['.jpg', '.jepg', '.jpeg2000', '.jpeg 2000', '.png', '.gif', '.webp', '.tif', '.tiff', '.psd', '.raw', '.bmp', '.heif', '.indd']

    
    def build_hash_lists(self):
        '''
        This method reads all the hash files in the has directory and makes them into a list of objects for comparing to the hasehs of files
        '''
        logger.debug(f'BEGIN: FileSearcher.build_hash_lists()')
        try:
            for currentDir, subs, files in os.walk(self.hash_dir):
                for f in files:
                    f_name, f_extension = os.path.splitext(f)
                    with open(os.path.join(currentDir, f), 'r') as keyword_list:
                        for line in keyword_list:
                            self.hashes.append((f,line.rstrip()))
        except Exception as e:
            logger.error(f'ERROR: Unbound exception in FileSearcher.build_hash_lists. Message: {str(e)}')
        finally: 
            logger.debug(f'COMPLETE: FileSearcher.build_hash_lists()')
    

    def search_directories(self):
        for currentDir, subs, files in os.walk(self.target_dir):
            if files:
                for fl in files:
                    f_name, f_extension = os.path.splitext(fl)
                    if self.image_only_search:
                        if f_extension in (extension for extension in self.IMG_FILE_TYPES):
                            self._compare_hashes(os.path.join(currentDir, fl))
                    else:
                        self._compare_hashes(os.path.join(currentDir, fl), f_name)

    
    def write_report(self):
        print(f'FOR REPORT: ')
        for mtc in self.matches:
            print(f'LIST: {mtc.hash_list_name} NAME: {mtc.file_name} HASH: {mtc.hash} PATH: {mtc.file_path} TIMESTAMP: {mtc.timestamp_found}')




    def _compare_hashes(self, the_file: str, file_name: str):
        h  = hashlib.new('md5') #NOTE: in future we may make this autodetect the hashtype using regex
        b  = bytearray(128*1024)
        mv = memoryview(b)
        with open(the_file, 'rb', buffering=0) as f:
            for n in iter(lambda : f.readinto(mv), 0):
                h.update(mv[:n])
        hash_of_file = h.hexdigest()
        hash_found = filter(lambda x: x[1] == hash_of_file, self.hashes)
        [print(f'self.hashes LIST: {x}') for x in self.hashes]

        #TODO: Write any matching hashes to the self.match list
        for m in hash_found:
            self.matches.append(HashMatch(m[0], m[1], file_name,the_file))



    
        