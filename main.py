import tkinter as tk
from tkinter import ttk, StringVar
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText

from numpy import source
from convert_utils import simple2Trad, create_ebook, read_file
from download_utils import Downloader, create_metadata
import os
import subprocess
from config import TMP_FILE

ERROR_MESSAGE = {'read_error':lambda : showinfo(title="錯誤",message="無法解析此檔案編碼"),
                 'search_error':lambda : showinfo(title="訊息",message="找不到此小說"),
}

### Global Variable ###
FILE_PATH = ""
NOVEL_METADATA = []
DOWNLOADER = Downloader()
# Windows
win = tk.Tk()
win.title('Ebook Creator')
win.resizable(False, False)
win.geometry('1000x920')
### Variable ###
# For tab1
file_path_var = StringVar()
encoding_var = StringVar()
output_name_var = StringVar()
open_explorer_var =  tk.BooleanVar()
# For tab2
search_var = StringVar()
selected_novel_var = tk.StringVar()
# output_name_var_tab2 = tk.StringVar()
### Set Style ###
s = ttk.Style() 
s.configure('normal.TButton', font=('courier', 14, 'normal'))
s.configure('normal.TCheckbutton', font=('courier', 12, 'normal'))
lableFrame_font = ('courier', 14, 'normal')

def delete_if_exist():
    if os.path.exists(TMP_FILE):
        os.remove(TMP_FILE)

def clear_text_var(var):
    if var.get("1.0","end-1c") != '':
        var.delete("1.0","end")

def convert_txt():
    global FILE_PATH
    # Temp file exists
    if os.path.exists(TMP_FILE):
        return True
    else:
        content = read_file(FILE_PATH)
        # Read fail
        if content == None:
            return False

        content = simple2Trad(content)
        # Write temp file
        with open(TMP_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        return True
def open_explorer(path):
    if open_explorer_var.get():
        subprocess.Popen('explorer "{}"'.format(path))

def select_files():
    global FILE_PATH
    delete_if_exist()
    filetypes = (('text files', '*.txt'),)
    file_name = fd.askopenfilename(
        title='Open files',
        initialdir='./',
        filetypes=filetypes)

    # Update the file name
    FILE_PATH = file_name
    file_path_var.set(file_name)
    book_name = simple2Trad(os.path.basename(file_name).split('.')[0])
    
    output_name_var.set(os.path.join(".","output",book_name + '.epub'))
    # Enable the convert button
    convert_btn['state'] = 'normal'

def convert2epub():
    # Read fail
    if not convert_txt():
        ERROR_MESSAGE["read_error"]()
        return

    clear_text_var(chapter_preview)
    with open(TMP_FILE, "r",encoding = 'utf-8') as f:
        lines = f.readlines()
    chapter_names =  create_ebook(lines, output_name_var.get())
    chapter_preview.insert(tk.INSERT, "".join(chapter_names))
    showinfo(title="訊息",message="轉換結束")
    
    path = os.path.dirname(output_name_var.get())
    if path == '':
        path = '.'
    open_explorer(path)

def create_label_frame(text, parent):
    l = ttk.Label(text=text, font=lableFrame_font)
    frame = ttk.LabelFrame(parent, labelwidget=l)
    return frame

def search_novel():
    global NOVEL_METADATA, DOWNLOADER

    keyword = search_var.get()
    result = DOWNLOADER.search(keyword)
    # Not found
    if result == None:
        ERROR_MESSAGE["search_error"]()
        selected_novel_var.set([])
        download_and_convert_btn['state'] = 'disable'
        sure_select_btn['state'] = 'disable'
        output_name_var.set('')
        return

    NOVEL_METADATA = result

    novel_names = [metadata['novel_name'] + ' (來源{})'.format(metadata['source_idx']) for metadata in NOVEL_METADATA]
    selected_novel_var.set(novel_names)
    download_and_convert_btn['state'] = 'disable'
    sure_select_btn['state'] = 'normal'

def select_novel():
    global NOVEL_METADATA
    selected_idx = novel_listbox.curselection()[0]
    download_and_convert_btn['state'] = 'normal'
    novel_name = NOVEL_METADATA[selected_idx]['novel_name']
    output_name_var.set(os.path.join(".","output",novel_name  + '.epub'))

def download_and_convert_novel():
    global NOVEL_METADATA, FILE_PATH, SOURCE_IDX
    # Get selected novel and its index
    selected_idx = novel_listbox.curselection()[0]
    # Download novel
    DOWNLOADER.download(NOVEL_METADATA[selected_idx])
    # Do Covert
    delete_if_exist()
    FILE_PATH = "./tmp/novel.txt" # set global file path for convert2epub
    convert2epub()


### Control ###
tabControl = ttk.Notebook(win)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="epub轉換")
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text="下載小說")

tabControl.pack(expand=1,fill="both")

### Tab1: Convert epub ###
monty1 = ttk.LabelFrame(tab1)
monty1.grid(column=0, row=0)
ttk.Button(monty1, text="選擇檔案", command=select_files, style="normal.TButton", width=12).grid(column=0, row=0)
ttk.Entry(monty1, textvariable=file_path_var, state=tk.DISABLED, width=70, font=13).grid(column=1, row=0, padx=10)

ttk.Label(monty1, text="輸出名稱", font=lableFrame_font).grid(column=0, row=1, pady=10)
ttk.Entry(monty1, textvariable=output_name_var, width=70, font=13).grid(column=1, row=1, pady=10)

options = create_label_frame("選項", monty1)
options.grid(column=0, row=2, columnspan=2, pady=8)
ttk.Checkbutton(options, text="完成後開啟目錄",variable=open_explorer_var, style="normal.TCheckbutton").grid(column=0, row=0)

convert_btn = ttk.Button(monty1, text="開始轉換", command=convert2epub, state="disable", style="normal.TButton")
convert_btn.grid(column=0, row=3, columnspan=2,pady=8)

chapter_preview_frame = create_label_frame("章節預覽", monty1)
chapter_preview_frame.grid(column=0, row=4, columnspan=2)
chapter_preview = ScrolledText(chapter_preview_frame, font=5,wrap=tk.WORD)
chapter_preview.grid(column=0, row=0, columnspan=2, ipady=5)

### Tab2: Download novel ###
monty2 = ttk.LabelFrame(tab2)
monty2.grid(column=0, row=0)

search_frame = create_label_frame("搜尋", monty2)
search_frame.grid(column=0, row=0, columnspan=2)
ttk.Entry(search_frame, textvariable=search_var, width=70, font=12).grid(column=0, row=0, padx=10)
ttk.Button(search_frame, text="搜尋", command=search_novel, style="normal.TButton", width=12).grid(column=1, row=0)

search_result_frame = create_label_frame("搜尋結果", search_frame)
search_result_frame.grid(column=0, row=1, columnspan=2)


# Novel List box
novel_listbox = tk.Listbox(search_result_frame, listvariable=selected_novel_var, font=10, selectbackground="blue", selectmode="single", width=50)
novel_listbox.grid(column=0, row=1)

sure_select_btn = ttk.Button(search_result_frame, text="確定選取", command=select_novel, state="disable")
sure_select_btn.grid(column=1, row=1, padx=5)

download_options = create_label_frame("", monty2)
download_options.grid(column=0, row=1, columnspan=2)
ttk.Label(download_options, text="輸出名稱", font=lableFrame_font).grid(column=0, row=0, pady=10, padx=5)
ttk.Entry(download_options, textvariable=output_name_var, width=70, font=13).grid(column=1, row=0, columnspan=2,pady=10)
download_and_convert_btn = ttk.Button(download_options, text="下載並轉換", command=download_and_convert_novel, state="disable", style="normal.TButton", width=12)
download_and_convert_btn.grid(column=0, row=2, columnspan=3, pady=10)
ttk.Checkbutton(download_options, text="完成後開啟目錄",variable=open_explorer_var, style="normal.TCheckbutton").grid(column=0, row=1, columnspan=3,pady=10)

# chapter_preview_frame = create_label_frame("章節預覽", monty2)
# chapter_preview_frame.grid(column=0, row=2, columnspan=2)
# chapter_preview = ScrolledText(chapter_preview_frame, font=5,wrap=tk.WORD)
# chapter_preview.grid(column=0, row=0, columnspan=2, ipady=5)


if __name__ == "__main__":
    win.mainloop()