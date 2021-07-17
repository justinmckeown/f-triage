from tkinter import  Tk, Label, LabelFrame, Button, Entry, W, N, E, S, X,Y, Frame, LEFT, RIGHT, CENTER, Text, messagebox, Scrollbar, StringVar, OptionMenu, PhotoImage
from tkinter import ttk
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
import hashmatch


class HasherApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Hash Me Ashlee")
        self.master.minsize(750,500)
        self.master.tk.call('wm', 'iconphoto', self.master._w, PhotoImage(file='icons/window_icon.png'))
        
        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()

        search_frame = Frame(master)
        button_frame = Frame(master)
        results_frame = Frame(master)

        #Path to file setup
        self.myLabel = Label(search_frame, text="Path to Folder: ")
        self.myButton = Button(search_frame, text="Find Folder", command=self.get_filepath)
        self.the_file_path = Entry(search_frame)
        self.hashButton = Button(button_frame, text="Hash Files", command=self.go_hash)
        
        #setup hashlist
        #self.available_hashes = diectorydive.get_hashing_algs()
        
        #TODO: Finish setting the default value to sha1 hash. Replace the following 3ish lines with a list comprehension
        self.option_val = StringVar()
        place = self.option_default_val()
        self.option_val.set(self.available_hashes[place])
        self.option_menu = OptionMenu(button_frame, self.option_val, self.option_val.get(), *self.available_hashes)
        self.hashButton.update_idletasks()
        
        #Report setup
        self.report_header = LabelFrame(results_frame, text='Report')
        self.report_text = Text(self.report_header)
        self.scrollbar = Scrollbar(self.report_header, command=self.report_text.yview)
        self.report_text['yscrollcommand'] = self.scrollbar.set


        #grid layout....
        self.myLabel.grid(row=0, column=0, padx=5, pady=10)
        self.the_file_path.grid(row=0, column=1, columnspan=3, padx=5, pady=10, sticky=(W,E))
        self.myButton.grid(row=0, column=4, padx=5, pady=5, sticky=(E))
        self.option_menu.grid(row=1, column=3, padx=5, pady=2, sticky=(E,W))
        self.hashButton.grid(row=1, column=4, padx=5, pady=2, sticky=(E))
        
        self.report_header.grid(row=0, column=0, padx=10, pady=10, sticky=(N,S,W,E))
        self.report_text.grid(row=0, column=0, padx=10, pady=10, sticky=(N,S,W,E))
        self.scrollbar.grid(row=0, column=1, sticky=(N,S,E))
        
        #Add frames to 
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(N,W,E))
        button_frame.grid(row=1, column=1, sticky=(N,E))
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(N,S,E,W))

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
        

        
    def get_filepath(self):
        self.the_file_path.delete(0,'end')
        pth = askdirectory()
        print(f'PATH: {pth}')
        self.the_file_path.insert(0,pth)
    
    def go_hash(self):
        if not self.the_file_path.get():
            messagebox.showinfo("NO FILE PATH","Please set the file path to the folder containing the files you wish to produce hash signtatures for")
        else:
            try:
                diectorydive.hash_type = str(self.option_val.get())
                report = diectorydive.itterate(self.the_file_path.get())
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
    diectorydive.get_os_details() #get the details for the kind of system the program is running on...
    root = Tk()
    my_app = HasherApp(root)
    root.mainloop()