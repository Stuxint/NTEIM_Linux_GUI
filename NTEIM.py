from tkinter import *
from tkinter import font
from tkinter import ttk
import os
import shutil
import shlex
import subprocess
from itertools import islice
from collections import deque
from tkinter import PhotoImage


root = Tk()
root.configure(bg="lightgreen")   # Wrap at word boundaries
root.option_add("*Label.wrapLength", 1200)
root.geometry("750x400")
root.title("NTEIM")

logo = PhotoImage(file="C:\\Users\\hitte\\Downloads\\NTEIM_logo.png")  # Replace with your logo file path
# Set the window's icon to the logo
root.iconphoto(False, logo)


# Create a canvas and a scrollbar
canvas = Canvas(root, bg="lightgreen", width=700, height=400)
canvas.config(highlightthickness=0, borderwidth=0)
scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
scrollable_frame = Frame(canvas, bg="lightgreen")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack canvas and scrollbar
canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

# Styles
f = font.Font(family="Courier", size=20)

l = Label(scrollable_frame, text="NTEIM by Ekyarele[Version 1.0.0]", font=f, bg='lightgreen')
l.pack(anchor=W, padx=10, pady=5)

x = Label(scrollable_frame, text="(c) Ekyarele Inc. All rights reserved", font=f, bg='lightgreen')
x.pack(anchor=W, padx=10, pady=5)

y_offset = 10
command_labels = []

# Logic
def on_key_release(event):
    global y_offset
    e = event.widget

    p = e.get("1.0", "end-1c")
    e.config(state="normal")  
    e.config(bg="lightgreen")
    e.config(state="disabled")
    

    if "help".lower() in p:
        #For files
        Label(scrollable_frame, text="Commands Here: ", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
        Label(scrollable_frame, text="  touch [filename/path to file]: creates file(no path, creates path in home)", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
        Label(scrollable_frame, text="  mv [filename/path to file] [new destinaiton]: moves file(do specify intial path if file not in home)", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
        Label(scrollable_frame, text="  cat [filename/path to file]: displays contents of file(do specify path if file not in home)", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
        Label(scrollable_frame, text="  tail [filename/path to file]: displays last 10 lines of file(do specify path if file not in home)", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
        Label(scrollable_frame, text="  head [filename/path to file]: displays first 10 lines of file(do specify path if file not in home)", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
        Label(scrollable_frame, text="  rm [filename/path to file]: deletes file(do specify path if file not in home)", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
        Label(scrollable_frame, text="  vi [name of editor you wish to use] [filename/path to file]: allows you to edit file(do specify path if file not in home)", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

        #For directories
        Label(scrollable_frame, text="  mkdir [directory name/path to directory]: creates directory(no path, creates path in home)", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
        Label(scrollable_frame, text="  cd [directory name/path to directory] [new destinaiton]: moves directory(do specify intial path if directory not in home)", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
        Label(scrollable_frame, text="  ls-l [directory name/path to directory]: displays contents of directory(do specify path if directory not in home)", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
        Label(scrollable_frame, text="  chmod [numeric code] [filename/path to file]: change permissions of file(do specify path if directory not in home; only use numeric code(e.g: 755) and no letters(e.g: u=rwx))", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
        Label(scrollable_frame, text="  rm-r [directory name/path to directory]: deletes directory(do specify path if directory not in home)", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

    elif "touch".lower() in p:
        a = p.split(" ", 1)
        ab = str(a[1])
        with open(ab, 'w') as my_file:
            Label(scrollable_frame, text=f"File successfully created", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
    
    elif "mv".lower() in p:
        b1 = shlex.split(p, posix=False)
        b2, b3 = b1[1], b1[2]
        try:
            if os.path.exists(b2):
                shutil.move(b2, b3)
                Label(scrollable_frame, text=f"File successfully moved", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
            else:
                raise FileNotFoundError(f"File not found or directory doesn't exist.") 
        except Exception as e:
            Label(scrollable_frame, text=f"Error: {e}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
    
    elif "rm".lower() in p:
        d = p.split(" ", 1)
        da = str(d[1])
        try:
            if os.path.exists(da):
                os.remove(da)
                Label(scrollable_frame, text=f"File successfully deleted", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
            else:
                raise FileNotFoundError(f"File '{da}' not found.") 
        except Exception as e:
            Label(scrollable_frame, text=f"Error: {e}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
        
    elif "chmod".lower() in p: 
        c1 = shlex.split(p, posix=False)
        ca = c1[1]
        cb = c1[2]
        c4 = int(ca, 8)

        try:
            if os.path.exists(cb):
                os.chmod(cb, c4)
                Label(scrollable_frame, text=f"Permissions successfully changed", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
               
            else:
                # If the file doesn't exist, raise FileNotFoundError explicitly
                raise FileNotFoundError(f"File not found or directory doesn't exist.") 

        except FileNotFoundError as e:
            Label(scrollable_frame, text=f"Error: {e}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
            

        except PermissionError:
            Label(scrollable_frame, text=f"Error: You do not have the right to change priviliges at {cb}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
           

        except Exception as e:
            # Handle other potential exceptions, if needed
            Label(scrollable_frame, text=f"An unexpected error occurred: {e}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

    elif "mkdir".lower() in p: 
        ela = p.split(" ", 1)
        elb = str(ela[1])

        try:
                os.makedirs(elb, exist_ok=True)
                Label(scrollable_frame, text=f"Directory successfully made", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
            
        except FileNotFoundError:
            Label(scrollable_frame, text=f"Error: Path doesn't exist", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

        except FileExistsError:
            Label(scrollable_frame, text=f"Error: Directory already exists", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

        except PermissionError:
            Label(scrollable_frame, text=f"Error: You don't have the permission to create a directory", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
                 
        except Exception as e:
            # Handle other potential exceptions, if needed
            Label(scrollable_frame, text=f"An unexpected error occurred: {e}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

    elif "rm-r".lower() in p: 
        love = shlex.split(p)
        peace = love[2]

        try:
                shutil.rmtree(peace)
                Label(scrollable_frame, text=f"Directory successfully deleted", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
            
        except FileNotFoundError:
            Label(scrollable_frame, text=f"Error: Path doesn't exist", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

        except PermissionError:
            Label(scrollable_frame, text=f"Error: You don't the permission to delete this directory", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
                 
        except Exception as e:
            # Handle other potential exceptions, if needed
            Label(scrollable_frame, text=f"An unexpected error occurred: {e}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
  
    elif "cd".lower() in p:
        dad = shlex.split(p, posix=False)
        mom = dad[1]
        bro = dad[2]

        try:
           shutil.move(mom, bro)
           Label(scrollable_frame, text=f"Directory successfully moved", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
            
        except FileNotFoundError:
            Label(scrollable_frame, text=f"Error: Path doesn't exist", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

        except PermissionError:
            Label(scrollable_frame, text=f"Error: You don't the permission to move this directory", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
                 
        except Exception as e:
            # Handle other potential exceptions, if needed
            Label(scrollable_frame, text=f"An unexpected error occurred: {e}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
 
    elif "ls-l".lower() in p:
        mama = shlex.split(p, posix=False)
        dada = mama[1]

        try:
           with os.scandir(dada) as entries:
            for entry in entries:
                file_type = "Directory" if entry.is_dir() else "File"
                size = entry.stat().st_size  # File size in bytes
                mod_time = entry.stat().st_mtime  # Last modified time (epoch)
                Label(scrollable_frame, text=f"Name:{entry.name}-Type:{file_type}-Size:{size} bytes-Last time modified:{mod_time}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
   
        except FileNotFoundError:
            Label(scrollable_frame, text=f"Error: Path doesn't exist", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

        except PermissionError:
            Label(scrollable_frame, text=f"Error: You don't the permission to view this directory", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
                 
        except Exception as e:
            # Handle other potential exceptions, if needed
            Label(scrollable_frame, text=f"An unexpected error occurred: {e}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
 
    elif "vi".lower() in p: 
        command = shlex.split(p, posix=False)
        editor = command[1]
        path = command[2]

        try:
            if os.path.exists(path):
                subprocess.run([editor, path])
                Label(scrollable_frame, text=f"File successfully edited", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

            else:
                raise FileNotFoundError(f"File not found or directory doesn't exist.") 
        
        except PermissionError:
            Label(scrollable_frame, text=f"Error: You don't have the permission to edit this file", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
                 
        except Exception as e:
            # Handle other potential exceptions, if needed
            Label(scrollable_frame, text=f"An unexpected error occurred: {e}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

    elif "head".lower() in p:
        boy = p.split(" ", 1)
        girl = str(boy[1])

        try:
            with open(girl, "r") as file:
                for line in islice(file, 10):
                    Label(scrollable_frame, text=f"{line}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
            
        except FileNotFoundError:
            Label(scrollable_frame, text=f"Error: Path doesn't exist", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)


        except PermissionError:
            Label(scrollable_frame, text=f"Error: You don't have the permission to view the contents of this file", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
                 
        except Exception as e:
            # Handle other potential exceptions, if needed
            Label(scrollable_frame, text=f"An unexpected error occurred: {e}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

    elif "cat".lower() in p:
        man = p.split(" ", 1)
        woman = str(man[1])

        try:
            with open(woman, "r") as file:
                content = file.read()
                Label(scrollable_frame, text=f"Contents of file:\n{content}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
            
        except FileNotFoundError:
            Label(scrollable_frame, text=f"Error: File/Path doesn't exist", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)


        except PermissionError:
            Label(scrollable_frame, text=f"Error: You don't have the permission to view the contents of this file", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
                 
        except Exception as e:
            # Handle other potential exceptions, if needed
            Label(scrollable_frame, text=f"An unexpected error occurred: {e}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

    elif "tail".lower() in p:
        old = p.split(" ", 1)
        young = str(old[1])

        try:
            with open(young, "r") as file:
                last_10_lines = deque(file, 10)  # Keeps only the last 10 lines in memory

            for line in last_10_lines:
                Label(scrollable_frame, text=f"{line}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
            
        except FileNotFoundError:
            Label(scrollable_frame, text=f"Error: File/Path doesn't exist", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)


        except PermissionError:
            Label(scrollable_frame, text=f"Error: You don't have the permission to view the contents of this file", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
                 
        except Exception as e:
            # Handle other potential exceptions, if needed
            Label(scrollable_frame, text=f"An unexpected error occurred: {e}", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)

    else:
       Label(scrollable_frame, text=f"'{p}' is not recognized as a command. Please type 'help' to see available commands.", font=f, bg='lightgreen').pack(anchor=W, padx=10, pady=5)
         
    add_command_line()
    canvas.yview_moveto(1)  # Scroll to bottom automatically

# Repeating labels
def add_command_line():
    frame = Frame(scrollable_frame, bg="lightgreen")
    frame.pack(anchor=W, padx=10, pady=20)
    Label(frame, text="Type in command: ", font=f, bg='lightgreen').pack(side=LEFT)

    # Create a Text widget instead of Entry for better control
    e = Text(frame, font=f, bg="lightgreen", bd=0, highlightthickness=0,  height=1, width=60, wrap='word')
    e.pack(side=LEFT, fill=X, expand=True)
    e.bind("<Return>", on_key_release)
    e.focus_set()
    
    command_labels.append(frame)
add_command_line()

root.mainloop()
