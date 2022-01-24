# Overview
The aim of this project is to produce a simple to use, lightweight tool for checking lists of hashes against target drives and directories.

## Current status
Currently working toward minimum viable product. 

## How it Works
This tool will walk thorugh a hard drive or directory, producing hashes of each file it finds therein and checking this hash against one or more a lists of hashes that the user has supplied. If a matching hash is found it is reported to the user. At the end of the search process the programme write three reports for the user. these are:
1.  **f_triate_report.txt** - *A basic report of the search process*
2. **f_triage_report.csv** - *A list of all files matched with relevent supporting details*
3. **f_traige_report.csv** - *A list of all files which oculd not be accessed while searching* 

### Instructions for use: 
The program boots and you're presented with a GUI. The GUI has three text inputs. Click the **Select** button besude each text input to naviagate to the apporpriate folders and the fields will autopopulate. For clarity:  
- **Target** *The directory or drive you want to search*
- **Hash Files** *The **directory** containing the .txt files that list the hashes you want to search the target for*
- **Report Save L:ocation** *The **directory** you want the reports listed above under **How it Works** saved to when the proces completes*  

## Tests and Known Issues
I have performed the following tests on this software:

### Windows 10 Platform Tests 
We have tested the following which all worked without error:  
- Read from and write to Windows drives and folders on the same machine that the software is running
- Read from and write to Windows hard drives attached via a USB cable
- Read from and write to Windows hard drives accessible via an external hard drive craddle
- Search an encase EO1 drive  mountred using FTK imager. **NOTE:** You need to run **f_triage** as administrator for this to work and to keep FTK open once the image has been mounted.  

## Known issues
We are currently trying to resolve the following:
- some poeple have reported issues with Accessing network drives 

## Planned features
- Mount EO1 files from wihtin **f_traige**
- Read and examine virtual disk images