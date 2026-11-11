import tkinter
from tkinter import filedialog
import threading
import fitz
import os
import sys

class display:
    def __init__(self):
        #make window
        self.window = tkinter.Tk()
        #make frames in the window
        self.top = tkinter.Frame(self.window)
        self.mid = tkinter.Frame(self.window)
        self.extra = tkinter.Frame(self.window)
        self.bot = tkinter.Frame(self.window)
        #make string variable
        self.text_value = tkinter.StringVar()
        #make text widget for top frame
        self.output = tkinter.Label(self.top,
                                    textvariable = self.text_value,
                                    height=20,
                                    width=50,
                                    font=("Times", 25, "bold"),
                                    background="#D2B48C")
        #pack text widget
        self.output.pack(side = "left")
        #make file name widget for middle frame
        self.path_input = tkinter.Button(self.mid,
                                         width = 28,
                                         text = "Choose File",
                                         command = self.choose_file)
        #pack file name widget
        self.path_input.pack(side = "left")
        #make delay widget for extra frame
        self.delay_prompt = tkinter.Label(self.extra,
                                          text = "Delay")
        self.delay_input = tkinter.Entry(self.extra,
                                         width = 26)
        #pack extra widgets
        self.delay_prompt.pack(side = "left")
        self.delay_input.pack(side = "left")
        #make button widgets for bottom frame
        self.read = tkinter.Button(self.bot,
                                   text = "Read",
                                   command = self.reader_manager)
        self.close = tkinter.Button(self.bot, text = "Close",
                                    command = self.window.destroy,)
        self.pause_event = threading.Event()
        self.pause = tkinter.Button(self.bot,
                                    text = "Pause/Unpause",
                                    command = self.pause_toggle)
        self.clear = tkinter.Button(self.bot,
                                    text = "Clear",
                                    command = self.reset)
        #pack and colour button widgets
        self.read.pack(side = "left")
        self.close.pack(side = "left")
        self.pause.pack(side = "left")
        self.clear.pack(side = "left")
        self.read.configure(background = "#C5A059")
        self.close.configure(background = "#C5A059")
        self.pause.configure(background = "#C5A059")
        self.clear.configure(background = "#C5A059")
        #pack frames
        self.top.pack()
        self.mid.pack()
        self.extra.pack()
        self.bot.pack()
        #color
        self.window.configure(background="#D2B48C")
        self.top.configure(background="#D2B48C")
        self.mid.configure(background="#D2B48C")
        self.extra.configure(background="#D2B48C")
        self.bot.configure(background="#D2B48C")
        self.delay_prompt.configure(background="#D2B48C")
        self.path_input.configure(background="#C5A059")
        self.delay_input.configure(background="#C5A059")
        #misc
        self.is_reading = False
        self.path_chosen = False
        self.current_job = None
        #start loop
        self.window.mainloop()
    
    def reset(self):
        if self.current_job is not None:
           self.window.after_cancel(self.current_job)
           self.current_job = None 
        self.is_reading = False
        self.pause_event.clear()
        if hasattr(self, "selected_file_path"):
           delattr(self, "selected_file_path")  
        self.text_value.set("")
        self.path_input.config(text="Choose File")
    
    def choose_file(self):
        self.reset()
        file_path = filedialog.askopenfilename(title="Select File")
        if file_path:
            self.selected_file_path = file_path
            file_name = os.path.basename(file_path)
            self.path_input.config(text=f"{file_name}")
            
    def reader_manager(self):
        if self.is_reading:
           return
        self.is_reading = True
        self.reader()
        
    def reader(self):
        raw_delay = self.delay_input.get().strip()
        if not hasattr(self, 'selected_file_path'):
            self.text_value.set("Please select a file first.")
            self.is_reading = False
            return
        file_path = self.selected_file_path
        if not raw_delay:
            self.text_value.set("Please input a delay.")
            self.is_reading = False
            return
        try:
            delay = int(raw_delay)
        except ValueError:
            self.text_value.set("Delay must be a whole number.")
            self.is_reading = False
            return
        if file_path.endswith(".txt"):
            with open(self.selected_file_path, "r") as f:
                file_list = f.read().split()
                self.index = 0
                self.file_list = file_list
                self.delay = delay
                self.show_next()
        elif file_path.endswith(".pdf"):
            with open(self.pdf_to_text(file_path), "r") as f:
                file_list = f.read().split()
                self.index = 0
                self.file_list = file_list
                self.delay = delay
                self.show_next()
        else:
            self.text_value.set("Please select a .pdf or a .txt file.")
            self.is_reading = False
            return
            
    def pdf_to_text(self, file_path):
        base_name = os.path.splitext(self.selected_file_path)[0]
        txt_path = base_name + ".txt"
        doc = fitz.open(self.selected_file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        return txt_path

    def show_next(self):
        if self.pause_event.is_set():
           self.current_job = self.window.after(100, self.show_next)
           return
        if self.index < len(self.file_list):
           self.text_value.set(self.file_list[self.index])
           if "," in self.file_list[self.index] or ":" in self.file_list[self.index] or ";" in self.file_list[self.index] or "?" in self.file_list[self.index] or "!" in self.file_list[self.index]:
               self.index += 1
               self.current_job = self.window.after(self.delay*2,
                                                    self.show_next)
           elif "." in self.file_list[self.index]:
               self.index+=1
               self.current_job = self.window.after(self.delay*3,
                                                    self.show_next)
           else:
               self.index += 1
               self.current_job = self.window.after(self.delay,
                                                    self.show_next)
        else:
            self.text_value.set("Finished.")
            self.is_reading = False
            self.current_job = None

    def pause_toggle(self):
        if self.pause_event.is_set():
            self.pause_event.clear()
        else:
            self.pause_event.set()
    
 
if __name__ == '__main__':
    g = display( )