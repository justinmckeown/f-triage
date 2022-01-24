import logging
from operator import truediv
import os
import sys
import platform
from filereadwriteutility import *
import hashlib
from datetime import datetime
import typing
from xmlrpc.client import boolean
from datamodels import HashMatch, UncheckedFiles
import tkinter as tk

logger = logging.getLogger()

class FileSearcher:
    def __init__(self, target_dir: str, save_dir: str, hash_dir: str, image_only: bool = False) -> None:
        self.target_dir = target_dir
        self.save_dir = save_dir
        self.hash_dir = hash_dir
        self.timestamps: typing.Dict[str, str] = {'start': (datetime.now()).strftime("%Y/%m/%d, %H:%M:%S") , 'finish': ''}
        self.hashes: typing.List[tuple] = [] 
        self.matches: typing.List[HashMatch] = []
        self.unhashed_files: typing.List[UncheckedFiles] = []
        self.image_only_search = image_only
        self.IMG_FILE_TYPES = ['.jpg', '.jepg', '.jpeg2000', '.jpeg 2000', '.png', '.gif', '.webp', '.tif', '.tiff', '.psd', '.raw', '.bmp', '.heif', '.indd']
        self.files_checked: int = 0
        self.files_access_denied: int = 0

    
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
    

    def search_directories(self, hashed_counter: tk.StringVar, unhashed_counter: tk.StringVar):
        for currentDir, subs, files in os.walk(self.target_dir):
            try:
                if files:
                    for fl in files:
                        f_name, f_extension = os.path.splitext(fl)
                        if self.image_only_search:
                            if f_extension in (extension for extension in self.IMG_FILE_TYPES):
                                self._compare_hashes(os.path.join(currentDir, fl))
                        else:
                            self._compare_hashes(os.path.join(currentDir, fl), fl)
                        self.files_checked += 1
                        hashed_counter.set(str(self.files_checked))
            except Exception as e:
                logger.error(f'Excepiton while trying to process files. MESSAGE {str(e)}')
                self.unhashed_files.append(UncheckedFiles(f_name, os.path.join(currentDir,f_name),str(e)))
                self.files_access_denied += 1
                unhashed_counter.set(str(self.files_access_denied))
        logger.info(f'total files searched: {self.files_checked} Total files access denied: {self.files_access_denied}')

    
    def write_report(self):
        save_file_name = (datetime.now().strftime('%Y-%m-d-%H-%M-%S'))+'-f_triage_report'
        write_txt(save_file_name+'.txt',self.save_dir,[f'START TIME: {self.timestamps.get("start")}', f'END TIME: {self.timestamps.get("finish")} ', f'NUMBER OF FILES CHECKED: {self.files_checked}' ,f'NUMBER OF HASHES MATCHED: {len(self.matches)}'])
        if len(self.matches) > 0:
            write_csv(save_file_name+'-matched.csv', self.save_dir, ['Hash File Source','Hash', 'Matched to File', 'File Path', 'Timestamp  matched'], [[x.hash_list_name, x.hash, x.file_name, x.file_path, str(x.timestamp_found)] for x in self.matches])
        write_csv(save_file_name+'-unhashed_files.csv',self.save_dir, ['File Name', 'Directory', 'Reason it was not Hashed', 'Timestamp'], [[x.file_name, x.location, x.reason, x.timestamp] for x in self.unhashed_files])



    def timestamp_finish(self):
        self.timestamps['finish'] = (datetime.now()).strftime("%Y/%m/%d, %H:%M:%S") 


    def _compare_hashes(self, the_file: str, file_name: str):
        h  = hashlib.new('md5') #NOTE: in future we may make this autodetect the hashtype using regex
        b  = bytearray(128*1024)
        mv = memoryview(b)
        with open(the_file, 'rb', buffering=0) as f:
            for n in iter(lambda : f.readinto(mv), 0):
                h.update(mv[:n])
        hash_of_file = h.hexdigest()
        hash_found = filter(lambda x: x[1] == hash_of_file, self.hashes)

        #TODO: Write any matching hashes to the self.match list
        for m in hash_found:
            self.matches.append(HashMatch(m[0], m[1], file_name,the_file))



    
        