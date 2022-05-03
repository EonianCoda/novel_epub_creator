import subprocess
from tkinter import ttk


def clear_text_var(var):
    """Clear ScrollText content
    """
    if var.get("1.0","end-1c") != '':
        var.delete("1.0","end")

def create_label_frame(text:str, parent):
    lableFrame_font = ('courier', 14, 'normal')
    l = ttk.Label(text=text, font=lableFrame_font)
    frame = ttk.LabelFrame(parent, labelwidget=l)
    return frame

def open_explorer(path:str):
    subprocess.Popen('explorer "{}"'.format(path))

