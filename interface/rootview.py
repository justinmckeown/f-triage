from concurrent.futures import thread
import logging
from multiprocessing.sharedctypes import Value
import tkinter as tk
from tkinter import ttk
from tkinter import  Tk, Label, LabelFrame, Button, Entry, W, N, E, S, X,Y, Frame, LEFT, RIGHT, CENTER, Text, messagebox, Scrollbar, StringVar, OptionMenu, PhotoImage
from tkinter import ttk
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
from filesearcher import FileSearcher
import threading


logger = logging.getLogger()

class RootVieweController(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("F-Triage")
        self.minsize(750,500)
        #self.master.tk.call('wm', 'iconphoto', self.master._w, PhotoImage(file='icons/window_icon.png'))
        
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.file_count_display: int = 0

        self.search_frame = Frame(self)
        self.button_frame = Frame(self)
        self.results_frame = Frame(self)

        #Path to Target setup
        self.target_label = Label(self.search_frame, text="Target:")
        self.target_button = Button(self.search_frame, text="Select", command=self.get_target_path)
        self.the_target_path = Entry(self.search_frame)

        #Path to Hashes setup
        self.hash_label = Label(self.search_frame, text="Hash Files: ")
        self.select_hash_button = Button(self.search_frame, text="Select", command=self.get_hash_path)
        self.the_hash_path = Entry(self.search_frame)

        #Path to Save location setup
        self.report_label = Label(self.search_frame, text="Report Save Location: ")
        self.select_report_button = Button(self.search_frame, text="Select", command=self.get_report_path)
        self.the_report_path = Entry(self.search_frame)

        #Report setup
        #TODO: Make this into a Tree rather than a text area. 
        self.columns = ('hash_file', 'name', 'hash', 'path', 'timestamp')
        self.report_header = LabelFrame(self.results_frame, text='Report')
        self.tree = ttk.Treeview(self.results_frame, columns=self.columns, show='headings')
        self.tree.heading('hash_file', text='Hash File')
        self.tree.heading('name', text='File Name')
        self.tree.heading('hash', text='Matched Hash')
        self.tree.heading('path', text='Path to File')
        self.tree.heading('timestamp', text='Timestamp') 
       
        self.report_text = Text(self.report_header)
        self.scrollbar = Scrollbar(self.report_header, command=self.tree.yview)
        self.tree['yscrollcommand'] = self.scrollbar.set


        #find hashes button
        self.hash_button = Button(self.button_frame, text="Search", command=self.go_hash)
        self.hash_button.update_idletasks()
        
        
        


        #grid layout....
        
        #Row 0: the Target drive
        self.target_label.grid(row=0, column=0, padx=5, pady=10, sticky=(E))
        self.the_target_path.grid(row=0, column=1, columnspan=3, padx=5, pady=10, sticky=(W,E))
        self.target_button.grid(row=0, column=4, padx=5, pady=5, sticky=(E))

        #Row 1: the Location of the Hash files
        self.hash_label.grid(row=1, column=0, padx=5, pady=10, sticky=(E))
        self.the_hash_path.grid(row=1, column=1, columnspan=3, padx=5, pady=10, sticky=(W,E))
        self.select_hash_button.grid(row=1, column=4, padx=5, pady=5, sticky=(E))

        #Row 2: the Location of the Report
        self.report_label.grid(row=2, column=0, padx=5, pady=10, sticky=(E))
        self.the_report_path.grid(row=2, column=1, columnspan=3, padx=5, pady=10, sticky=(W,E))
        self.select_report_button.grid(row=2, column=4, padx=5, pady=5, sticky=(E))

        self.report_header.grid(row=0, column=0, padx=10, pady=10, sticky=(N,S,W,E))
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky=(N,S,W,E))
        #self.report_text.grid(row=0, column=0, padx=10, pady=10, sticky=(N,S,W,E))
        self.scrollbar.grid(row=0, column=1, sticky=(N,S,E))

        #Row 2: The Search button
        self.hash_button.grid(row=0, column=4, padx=5, pady=2, sticky=(E))
        

        #Add frames to 
        self.search_frame.grid(row=0, column=0, columnspan=2, sticky=(N,W,E))
        self.results_frame.grid(row=1, column=0, columnspan=2, sticky=(N,S,E,W))
        self.button_frame.grid(row=2, column=1, sticky=(N,E))

        #configure searchframes expanding
        self.search_frame.columnconfigure(0, weight=0)
        self.search_frame.columnconfigure(1, weight=3)
        self.search_frame.columnconfigure(2, weight=0)
        self.search_frame.columnconfigure(3, weight=0)

        self.report_header.columnconfigure(0, weight=3)
        self.report_header.rowconfigure(0,weight=3)

        self.results_frame.columnconfigure(0, weight=3)
        self.results_frame.rowconfigure(0, weight=3)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(2, weight=3)
    
    #NOTE: This method is not being used
    def option_default_val(self):
        for index, val in enumerate(self.available_hashes):
            if val == 'sha256':
                return index
        else:
            return 0
    
    def get_target_path(self):
        self.the_target_path.delete(0,'end')
        self.target_pth = askdirectory()
        logger.debug(f'Setting Target path: {self.target_pth}')
        self.the_target_path.insert(0,self.target_pth)
        
    def get_hash_path(self):
        self.the_hash_path.delete(0,'end')
        self.hash_pth = askdirectory()
        logger.debug(f'Setting Hash path: {self.hash_pth}')
        self.the_hash_path.insert(0,self.hash_pth)

    def get_report_path(self):
        self.the_report_path.delete(0,'end')
        self.report_pth = askdirectory()
        logger.debug(f'Setting Hash path: {self.report_pth}')
        self.the_report_path.insert(0,self.report_pth)

    def go_hash(self):
        if not self.the_target_path.get() or not self.the_hash_path.get() or not self.the_report_path.get():
            messagebox.showinfo("TARGET, HASH AND SAVE PATHS ARE REQUIRED: ","Please set the path to each of the required locations.")
        else:
            if self.tree.get_children():
                self._clear_tree()
            
            #Add to the GUI so we can show the user updates on the infromation being processed...
            self.files_processed = tk.StringVar(value=str(0))
            self.files_processed_label = Label(self.button_frame, textvariable=self.files_processed)
            self.files_processed_label.grid(row=1, column=4, padx=2, sticky=(E))
            t = threading.Thread(target=self._run_search_thread)
            t.start()
                
               
    
    def _run_search_thread(self): 
        try:
            file_searcher = FileSearcher(self.target_pth,self.report_pth, self.hash_pth, False)
            file_searcher.build_hash_lists()
            file_searcher.search_directories(self.files_processed)
            self.files_processed.set(str(file_searcher.files_checked))
            if file_searcher.matches:
                for m in file_searcher.matches:
                    self.tree.insert('',tk.END, values=(m.hash_list_name, m.file_name, m.hash, m.file_path, m.timestamp_found))
        except Exception as e:
             messagebox.showerror("ERROR", f"something has gone wrong while attempting to produce hashes of your files. Message is as follows:\n {e}")
        else:
            if file_searcher.matches:
                messagebox.showinfo("SUCCESS!", f"Hashing files has completed with {len(file_searcher.matches)} matching results found.")
            else:
                messagebox.showinfo("SUCCESS!", f"Hashing files has completed with No matching results")
        finally:
            file_searcher.timestamp_finish() 
            file_searcher.write_report()


    def _clear_tree(self):
        logger.debug(f'_clear_tree called')
        for item in self.tree.get_children():
            self.tree.delete(item)

