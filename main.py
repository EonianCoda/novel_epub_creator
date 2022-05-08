import tkinter as tk
from tkinter import ttk, StringVar
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText

from utils.convert import simple2Trad, translate_and_convert
from utils.download import Downloader
from utils.config import TMP_DIRECTORY, TMP_RAR_PATH, TMP_TXT_PATH, SOURCE_NAME, reset_TMP_DIRECTORY, get_OUTPUT_PATH, delete_if_exist, is_compressed_file
from utils.tkinter import clear_text_var, open_explorer, create_label_frame
import os 
import glob
import patoolib

ERROR_MESSAGE = {'read_error':lambda : showinfo(title="錯誤",message="無法解析此檔案編碼"),
                 'search_error':lambda : showinfo(title="訊息",message="找不到此小說"),
}

### Global Variable ###
FILE_PATH = ""
NOVEL_METADATA = []
DOWNLOADER = Downloader()
SELECTED_IDX = -1
# Windows
win = tk.Tk()
win.title('Ebook Creator')
win.resizable(False, False)
win.geometry('1000x920')

### TK Variable ###
# For tab1
file_path_var = StringVar()
encoding_var = StringVar()
output_name_var = StringVar()
open_explorer_var =  tk.BooleanVar()
auto_extract_var = tk.BooleanVar()
auto_extract_var.set(True)
# For tab2
search_var = StringVar()
selected_novel_var = tk.StringVar()

### Set Style ###
s = ttk.Style() 
s.configure('normal.TButton', font=('courier', 14, 'normal'))
s.configure('normal.TCheckbutton', font=('courier', 12, 'normal'))
lableFrame_font = ('courier', 14, 'normal')

def extract_and_setpath(input_path:str):
    """
    """
    global FILE_PATH
    if not is_compressed_file(input_path):
        raise ValueError(f"{input_path} is not rar or zip file !!")
    reset_TMP_DIRECTORY()
    patoolib.extract_archive(input_path, outdir=TMP_DIRECTORY)
    files = glob.glob(os.path.join(TMP_DIRECTORY,'*.txt'))
    FILE_PATH = files[0]

def select_files():
    global FILE_PATH
    filetypes = [('Accepted files', '*.txt'),
                ('Accepted files', '*.rar'),
                ('Accepted files', '*.zip'),
                ('text files', '*.txt'),
                ('compressed files','*.rar'),
                ('compressed files','*.zip')]
    file_path = fd.askopenfilename(
        title='Open files',
        initialdir='./',
        filetypes=filetypes)

    # Cancell
    if file_path == '':
        return

    file_path_var.set(file_path)
    # File is rar or zip file
    if auto_extract_var.get() == True and is_compressed_file(file_path):
        extract_and_setpath(file_path)
        book_name = os.path.basename(FILE_PATH).split('.')[0]
    else:
        # Update the file name
        FILE_PATH = file_path
        # Get book name from file name
        book_name = os.path.basename(file_path).split('.')[0]

    book_name = simple2Trad(book_name)
    # Set output path
    output_name_var.set(get_OUTPUT_PATH(book_name))
    # Enable the convert button
    convert_btn['state'] = 'normal'
    clear_text_var(chapter_preview)

def convert2epub():
    global FILE_PATH
    if is_compressed_file(FILE_PATH):
        extract_and_setpath(FILE_PATH)

    clear_text_var(chapter_preview)

    chapters = translate_and_convert(FILE_PATH, output_name_var.get())
    chapter_preview.insert(tk.INSERT, "".join(chapters))
    showinfo(title="訊息",message="轉換成功")
    
    # Open explorer
    if open_explorer_var.get() == True:
        path = os.path.dirname(output_name_var.get())
        if path == '':
            path = '.'
        open_explorer(path)

def search_novel():
    global NOVEL_METADATA, DOWNLOADER

    keyword = search_var.get()
    result = DOWNLOADER.search(keyword)
    # Not found
    if result == None:
        ERROR_MESSAGE["search_error"]()
        # Reset variable
        selected_novel_var.set([])
        output_name_var.set('')
        # Disable button
        download_and_convert_btn['state'] = 'disable'
        sure_select_btn['state'] = 'disable'
        return

    NOVEL_METADATA = result
    novel_names = [metadata['novel_name'] + ' ({})'.format(SOURCE_NAME[metadata['source_idx']]) for metadata in NOVEL_METADATA]
    selected_novel_var.set(novel_names)
    # Set button state
    download_and_convert_btn['state'] = 'disable'
    sure_select_btn['state'] = 'normal'

def select_novel():
    """確定選取
    """
    global NOVEL_METADATA, SELECTED_IDX
    SELECTED_IDX = novel_listbox.curselection()[0]
    download_and_convert_btn['state'] = 'normal' # Enable convert button
    # Set output name
    novel_name = NOVEL_METADATA[SELECTED_IDX]['novel_name']
    output_name_var.set(get_OUTPUT_PATH(novel_name))

def download_and_convert_novel():
    global NOVEL_METADATA, FILE_PATH, SELECTED_IDX
    # Get selected novel and its index

    # Download novel and convert
    DOWNLOADER.download(NOVEL_METADATA[SELECTED_IDX])
    FILE_PATH = TMP_TXT_PATH # set global file path for function convert2epub
    convert2epub()
    if NOVEL_METADATA[SELECTED_IDX]['source_idx'] == 0:
        delete_if_exist(TMP_RAR_PATH)


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
ttk.Checkbutton(options, text="選取後自動解壓縮",variable=auto_extract_var, style="normal.TCheckbutton").grid(column=1, row=0)

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