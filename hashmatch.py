import os 
import sys
import platform
import gc
import hashlib
from datetime import datetime
from hashlists import Hashlists

os_details = {}
BUFFER_SIZE = 65536 #control memory use on the host machien running it
FILE_TYPES = ['.jpg', '.jepg', '.jpeg2000', '.jpeg 2000', '.png', '.gif', '.webp', '.tif', '.tiff', '.psd', '.raw', '.bmp', '.heif', '.indd']


#HACK: The method for setting the slash off of the environment doesnt always work. so this is a workaround 
def execution_slash(pth : str):
    if '/' in pth:
        os_details['env_slash'] = '/'
    else:
        os_details['env_slash'] = '\\'

def get_os_details():
    try:
        os_details['os'] = platform.system()
        if platform.system() == 'Linux':
            os_details['slash'] = '//'
        else:
            os_details['slash'] = '\\'
    except Exception as e:
        print(f'Exception thrown in get_os_details: {e}')

def check_path_details(d, s, f):
    print(f'********************************************************************************\nCURRENT DIR: {d}\nSUB-DIRS: {s}\n FILES: {f}\n******************************************************\n ')


def get_application_path():
    # determine if application is a script file or frozen 
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(__file__)
    return application_path

def get_hashes(target_dir):
    hash_list = []
    try:
        print(f'Target Dir: {target_dir}')
        for currentDir, subs, files in os.walk(target_dir):
            for f in files:
                f_name, f_extension = os.path.splitext(f)
                hashrepo = Hashlists(f_name, [], [])
                thefile = target_dir+os_details.get('env_slash')+f
                
                with open(thefile, 'r') as keyword_list:
                    for line in keyword_list:
                        hashrepo.hashes.append(line.rstrip())
                hash_list.append(hashrepo)
    except Exception as e:
        print(f'ERROR: Unbound exception in get_hashes(). Message: {e}')
    finally:
        return hash_list         

def check_for_hashes(kwrds, target_dir):
    counter = 1
    unsearched = 0
    files_extensions_searched = []
    files_not_searched = []
    report = []
    print(f'begining check_for_keywords')
    try:
        for currentDir, subs, files in os.walk(target_dir):
            if files:
                #print(f'CURRENT DIR: {currentDir}')
                try:
                    for f in files:
                        f_name, f_extension = os.path.splitext(f)                        
                        thefile = os.path.join(currentDir, f)
                        #print(f'CURRENT FILE: {thefile}')
                        #do the hashing...
                        #print(f'Examining File named: {f}')
                        if f_extension.lower() in (extension for extension in FILE_TYPES):
                            print(f'{f_name} is an image file. Running hash check against it')
                            h  = hashlib.new('md5')
                            b  = bytearray(128*1024)
                            mv = memoryview(b)
                            with open(thefile, 'rb', buffering=0) as f:
                                for n in iter(lambda : f.readinto(mv), 0):
                                    h.update(mv[:n])
                            hash_of_file = h.hexdigest()
                            #print(f'the MD5 hash of this file is: {hash_of_file}\nChecking hash against those in our list of hashes...')
                            try:
                                for word_list in kwrds:
                                    for hsh in word_list.hashes:
                                        if hash_of_file == hsh:
                                            print(f'Hash found! for {f}')
                                            dt = datetime.strftime(datetime.now(), '%Y-%m-%d-%H:%M:%S')
                                            print(f'{word_list.name}, {hsh}, {thefile}, {dt}')
                                            word_list.report.append((word_list.name, hsh, thefile, dt))
                            except UnicodeDecodeError:
                                files_not_searched.append(f_name)
                                unsearched += 1
                            except UnicodeEncodeError:
                                files_not_searched.append(f_name)
                            except Exception as e:
                                print(f'unhandled exception in cehck_for_hashes() line 106')
                except Exception as e:
                    unsearched +=1
                    print('--------------------------------------------------------------------------------------------------------------------------------')
                    print(f'Unhandled exception when walking directories in check_for_hashes():')
                    print(type(e))
                    print(e)
                    print(e.args)
                    check_path_details(currentDir, subs, files)
                    print('--------------------------------------------------------------------------------------------------------------------------------\n')
                else:
                    files_extensions_searched.append(f_extension)
                    counter +=1
                
    except Exception as e:
        print('------------------------------------------------------------------------------------------------------------------------------')
        print(f'Unhandled exception when attempting to talk directories in check_for_hashes():')
        print(type(e))
        print(e)
        print(e.args)
        check_path_details(currentDir, subs, files)
        print('--------------------------------------------------------------------------------------------------------------------------------\n')
    finally:
        if files_not_searched: 
            print_warnings(files_not_searched) 
        print(f'returning hashes...')
        return kwrds

def print_warnings(warnings : list):
    print(f'WARNNG: Owing to encoding anomalies encountered when examining the following files, they should be checked mannually:')
    for x in warnings:
        print(x)


if __name__ == '__main__':
    print('hello')
    args = get_args()
    sourcepath = args[0]
    writepath = args[1]
    get_os_details() #get the operating system so you can use the correct slahsed for file paths
    keyword_path = get_application_path() #get the path to the dir the applicaiotn is running in
    print(f'APPLICATION PATH: {keyword_path}')
    execution_slash(keyword_path)
    watch_words = get_hashes(keyword_path+os_details.get('env_slash')+'userhashlists'+os_details.get('env_slash')) #append the path to the folder where keywords are kept to the give keyword_path
    updated_reports = check_for_hashes(watch_words,sourcepath)
    
    for repo in updated_reports:
        print(len(updated_reports))
        repo.write_report(writepath+os_details.get('env_slash')+repo.name+'-hash-check-report.csv')
    print(f'Process complete')
    
