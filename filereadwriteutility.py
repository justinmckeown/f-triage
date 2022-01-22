import csv
import json
import logging
import typing
import os
import pandas as pd
import openpyxl

logger = logging.getLogger()


def write_txt(file_name: str, save_pth: str, text_to_write: typing.List[str]):
    fp = os.path.join(save_pth,file_name)
    logger.debug(f'Writing {file_name} to  {fp}')
    with open(fp, 'a') as txtfile:
        txtfile.write('\n'.join(text_to_write)) #TODO: update this so we use the apporpriate newline char based on the detected os


#FIXME: CSV File does something funny to the dates when they're input into excel. Figure out why and fix this. 
def write_csv(file_name: str, save_pth: str, title_row: typing.List[str], data: typing.List[list]):
    fp = os.path.join(save_pth,file_name)
    logger.debug(f'Writing {file_name} to  {fp}')
    with open(fp, 'a', newline='') as csvfile:
        w = csv.writer(csvfile, dialect='excel') 
        w.writerow(title_row)
        for row in data: 
            w.writerow(row)


def read_csv(file_name: str, unique_path: str = '') -> typing.List[tuple]:
    data = []
    fp = unique_path+  file_name
    print(f'OPENING: {fp}')
    with open(fp, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        data.extend([tuple(row) for row in reader])
    return data


def write_json(file_path_and_name: str, dc: typing.Dict[str, typing.Dict]):
    j = json.dumps(dc, indent=4)
    with open(file_path_and_name, 'w') as f: 
        f.write(j)


def read_json(file_path_and_name: str) -> typing.Dict[str, typing.Union[str, typing.Dict[str, typing.Union[str, int, bool, None]]]]:
    with open (file_path_and_name) as f:
        return json.load(f)

def read_all_files_in_dir(path: str):
    data = []
    for root, dir, files in os.walk(path):
            for file in files:
                print(f'FILE: {file}')
                data.extend(read_csv(file,path))
    
    for n, r in enumerate(data):
        print(f'{n} : {r}')

def get_file_list(path: str) -> typing.List[str]:
    data = []
    for root, dir, files in os.walk(path):
            for file in files:
                print(f'FILE: {file}')
                data.append(file)
    
    return data
 
def make_excel_workbook_from_csv(pth: str, write_dir: str, write_file_name: str):
    writer = pd.ExcelWriter(write_dir+write_file_name, engine='openpyxl')
    for root, dir, files in os.walk(pth):
        for file in files:
            print(f'FILE: {pth}{file}')
            f = pd.read_csv(pth+file)
            f.to_excel(writer,sheet_name=os.path.splitext(file)[0], index=False,header=True)    
    writer.save()


