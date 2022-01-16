from tkinter import  Tk, Label, LabelFrame, Button, Entry, W, N, E, S, X,Y, Frame, LEFT, RIGHT, CENTER, Text, messagebox, Scrollbar, StringVar, OptionMenu, PhotoImage
from tkinter import ttk
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
import hashmatch


class HasherApp:
    def __init__(self, master):
        self.master = master
        self.master.title("F-Triage")
        self.master.minsize(750,500)
        #self.master.tk.call('wm', 'iconphoto', self.master._w, PhotoImage(file='icons/window_icon.png'))
        
        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()

        search_frame = Frame(master)
        button_frame = Frame(master)
        results_frame = Frame(master)

        #Path to Target setup
        self.target_label = Label(search_frame, text="Target:")
        self.target_button = Button(search_frame, text="Select", command=self.get_target_path)
        self.the_target_path = Entry(search_frame)

        #Path to Hashes setup
        self.hash_label = Label(search_frame, text="Hash Files: ")
        self.select_hash_button = Button(search_frame, text="Select", command=self.get_hash_path)
        self.the_hash_path = Entry(search_frame)

        #Path to Save location setup
        self.report_label = Label(search_frame, text="Report Save Location: ")
        self.select_report_button = Button(search_frame, text="Select", command=self.get_report_path)
        self.the_report_path = Entry(search_frame)

        #Report setup
        self.report_header = LabelFrame(results_frame, text='Report')
        self.report_text = Text(self.report_header)
        self.scrollbar = Scrollbar(self.report_header, command=self.report_text.yview)
        self.report_text['yscrollcommand'] = self.scrollbar.set

        #find hashes button
        self.hash_button = Button(button_frame, text="Search", command=self.go_hash)
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

        #Row 2: the Location of the Hash files
        self.report_label.grid(row=2, column=0, padx=5, pady=10, sticky=(E))
        self.the_report_path.grid(row=2, column=1, columnspan=3, padx=5, pady=10, sticky=(W,E))
        self.select_report_button.grid(row=2, column=4, padx=5, pady=5, sticky=(E))

        
        self.report_header.grid(row=0, column=0, padx=10, pady=10, sticky=(N,S,W,E))
        self.report_text.grid(row=0, column=0, padx=10, pady=10, sticky=(N,S,W,E))
        self.scrollbar.grid(row=0, column=1, sticky=(N,S,E))

        #Row 2: The Search button
        self.hash_button.grid(row=0, column=4, padx=5, pady=2, sticky=(E))


        
        #Add frames to 
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(N,W,E))
        results_frame.grid(row=1, column=0, columnspan=2, sticky=(N,S,E,W))
        button_frame.grid(row=2, column=1, sticky=(N,E))

        #configure searchframes expanding
        search_frame.columnconfigure(0, weight=0)
        search_frame.columnconfigure(1, weight=3)
        search_frame.columnconfigure(2, weight=0)
        search_frame.columnconfigure(3, weight=0)

        self.report_header.columnconfigure(0, weight=3)
        self.report_header.rowconfigure(0,weight=3)

        results_frame.columnconfigure(0, weight=3)
        results_frame.rowconfigure(0, weight=3)

        self.master.columnconfigure(0, weight=3)
        self.master.columnconfigure(1, weight=3)
        self.master.rowconfigure(2, weight=3)
    
   
    
    def option_default_val(self):
        for index, val in enumerate(self.available_hashes):
            if val == 'sha256':
                print(f'found: {val} Returning: {index}')
                return index
        else:
            return 0
    
    def get_target_path(self):
        self.the_target_path.delete(0,'end')
        pth = askdirectory()
        print(f'PATH: {pth}')
        self.the_target_path.insert(0,pth)
        
    def get_hash_path(self):
        self.the_hash_path.delete(0,'end')
        pth = askdirectory()
        self.the_hash_path.insert(0,pth)

    def get_report_path(self):
        self.the_report_path.delete(0,'end')
        pth = askdirectory()
        self.the_report_path.insert(0,pth)

    def go_hash(self):
        if not self.the_target_path.get() or not self.the_hash_path.get() or not self.the_report_path.get():
            messagebox.showinfo("TARGET, HASH AND SAVE PATHS ARE REQUIRED: ","Please set the path to each of the required locations.")
        else:
            try:
                diectorydive.hash_type = str(self.option_val.get())
                report = diectorydive.itterate(self.the_target_path.get())
            except Exception as e:
                messagebox.showerror("ERROR", f"something has gone wrong while attempting to produce hashes of your files. Message is as follows:\n {e}")
            finally:
                report.insert(2, '\n\n')
                self.write_report(report)
                messagebox.showinfo("SUCCESS!", "Hashing files has completed")
    

    def write_report(self, l: list):
        self.report_text.delete(1.0, 'end')
        for index, entry in enumerate(l,start=0):
            self.report_text.insert(float(index+1), entry)
            


if __name__ == '__main__':
    hashmatch.get_os_details() #get the details for the kind of system the program is running on...
    root = Tk()
    my_app = HasherApp(root)
    root.mainloop()