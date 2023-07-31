import tkinter as tk
from tkinter import ttk, StringVar
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText
from utils.convert import simple2Trad, translate_and_convert, translate_and_convert_japanese
from utils.download import Downloader, Japanese_downloader
from utils.config import FINDS, JAPANESE_SOURCE_NAME, MAX_CHAPTER_NAME_LEN, TMP_DIRECTORY, TMP_RAR_PATH, TMP_TXT_PATH, SOURCE_NAME,GOOGLE_DRIVE_PATH
from utils.config import reset_TMP_DIRECTORY, delete_if_exist, is_compressed_file, Setting
from utils.ebook import integrate_japanese_epubs
from utils.tkinter import clear_text_var, open_explorer, create_label_frame
import os 
import glob
import patoolib
import webbrowser
#from utils.google_drive import upload
### Error Message ###
ERROR_MESSAGE = {'read_error':lambda : showinfo(title="錯誤",message="無法解析此檔案編碼"),
                 'download_error':lambda : showinfo(title="錯誤",message="下載錯誤"),
                 'copyright_error':lambda : showinfo(title="訊息",message="該小說有版權問題，無法下載"),
                 'search_error':lambda : showinfo(title="訊息",message="找不到此小說"),
}
### Setting ###
setting = Setting()

### Global Variable ###
FILE_PATH = ""
NOVEL_METADATA = []
DOWNLOADER = Downloader()
JAPANESE_DOWNLOADER = Japanese_downloader()
SELECTED_IDX = -1
BLACKED_ELEMENT_SELECTED_IDX = -1

### Windows ###
win = tk.Tk()
win.title('Ebook Creator')
win.resizable(False, False)
# Revise window size depending the size of the screen 
base_screen_w = 1920
base_screen_h = 1080
base_win_w = 900
base_win_h = 900
screen_w = win.winfo_screenwidth()
screen_h = win.winfo_screenheight()
win_w = int(base_win_w * (screen_w / base_screen_w))
win_h = int(base_win_h * (screen_h / base_screen_h))
win.geometry(f'{win_w}x{win_h}') # set application window size

### Set Style ###
s = ttk.Style() 
s.configure('normal.TButton', font=('courier', 14, 'normal'))
s.configure('normal.TCheckbutton', font=('courier', 12, 'normal'))
lableFrame_font = ('courier', 14, 'normal')


### Tkinter Variable ###
## For tab1(Convert epub)
file_path_var = StringVar()
encoding_var = StringVar()
output_name_var = StringVar()
# Output directory
output_dir_var  = StringVar()
output_dir_var.set(setting['output_dir'])
# Input directory for select file
input_dir  = StringVar()
input_dir.set(setting['input_dir'])
# Output setting
max_chapter_len_var = tk.IntVar()
max_chapter_len_var.set(MAX_CHAPTER_NAME_LEN)
# Options
open_explorer_var =  tk.BooleanVar(value=True)
auto_extract_var = tk.BooleanVar()
auto_extract_var.set(True)
auto_convert_var = tk.BooleanVar()
auto_convert_var.set(False)

## For tab2(Search China novel)
search_var = StringVar()
selected_novel_var = tk.StringVar()
gdrive_link_var = tk.StringVar()

## For tab3(Setting)
new_black_list_element = tk.StringVar()
black_list_elements_list = []
black_list_elements = tk.StringVar(value=black_list_elements_list)
# Output setting
max_chapter_len_var = tk.IntVar()
max_chapter_len_var.set(MAX_CHAPTER_NAME_LEN)
## For tab4
multi_file_paths = []

## For tab5
selected_japanese_novel_var = tk.StringVar()
auto_download_japanese_var = tk.BooleanVar()
auto_download_japanese_var.set(False)
output_japanese_name_var = tk.StringVar()



def open_gdrive_link():
    if gdrive_link_var.get() != "":
        webbrowser.open_new(gdrive_link_var.get())

def copy_gdrive_link():
    if gdrive_link_var.get() != "":
        win.clipboard_clear()
        win.clipboard_append(gdrive_link_var.get())
        showinfo(title="訊息",message="複製成功!")
def get_output_path():
    output_dir = output_dir_var.get()
    if output_dir == "":
        output_dir = ".\\output"
    return os.path.join(output_dir, output_name_var.get() )
def end_with_epub(novel_name:str):
    if not novel_name.endswith(".epub"):
        novel_name += '.epub'
    return novel_name

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
        initialdir=input_dir.get(),
        filetypes=filetypes)

    # Cancel
    if file_path == '':
        return

    file_path_var.set(file_path)
    # File is rar or zip file
    if auto_extract_var.get() == True and is_compressed_file(file_path):
        extract_and_setpath(file_path)
        book_name = os.path.splitext(os.path.basename(FILE_PATH))[0]
    else:
        # Update the file name
        FILE_PATH = file_path
        # Get book name from file name
        book_name = os.path.splitext(os.path.basename(file_path))[0]

    book_name = simple2Trad(book_name)
    # Set output path

    output_name_var.set(end_with_epub(book_name))
    # Enable the convert button
    convert_btn['state'] = 'normal'
    clear_text_var(chapter_preview)

    # Auto convert
    if auto_convert_var.get() == True:
        convert2epub()

def convert2epub():
    global FILE_PATH
    if is_compressed_file(FILE_PATH):
        extract_and_setpath(FILE_PATH)

    clear_text_var(chapter_preview)
    try:
        chapters = translate_and_convert(FILE_PATH, get_output_path(), white_list.get("1.0","end-1c").split('\n'), black_list_elements_list, max_chapter_len_var.get())
    except UnicodeDecodeError:
        ERROR_MESSAGE['read_error']()
        return
    chapter_preview.insert(tk.INSERT, "".join(chapters))
    showinfo(title="訊息",message="轉換成功")
    
    # Open explorer
    if open_explorer_var.get() == True:
        path = output_dir_var.get()
        if path == '':
            path = '.'
        open_explorer(path)

def search_novel():
    global NOVEL_METADATA, DOWNLOADER

    keyword = search_var.get()
    if keyword == "":
        return
    result = DOWNLOADER.search(keyword)
    # Not found
    if result == None:
        ERROR_MESSAGE["search_error"]()
        # Reset variable
        selected_novel_var.set([])
        output_name_var.set('')
        # Disable button
        download_and_convert_btn['state'] = 'disable'
        return

    NOVEL_METADATA = result
    novel_names = []
    for idx, metadata in enumerate(NOVEL_METADATA):
        novel_name = metadata['novel_name']
        source_name = SOURCE_NAME[metadata['source_idx']]
        novel_names.append(f"{idx} {novel_name} ({source_name})")
    selected_novel_var.set(novel_names)
    # Set button state
    download_and_convert_btn['state'] = 'disable'

def search_japanese_novel():
    global NOVEL_METADATA, JAPANESE_DOWNLOADER, SELECTED_IDX
    
    keyword = search_var.get()
    if keyword == "":
        return
    result = JAPANESE_DOWNLOADER.search(keyword)
    # Not found
    if result == None:
        ERROR_MESSAGE["search_error"]()
        # Reset variable
        selected_japanese_novel_var.set([])
        output_name_var.set('')
        # Disable button
        download_and_convert_btn['state'] = 'disable'
        return
    NOVEL_METADATA = result
    novel_names = []
    for idx, metadata in enumerate(NOVEL_METADATA):
        novel_name = metadata['novel_name']
        author = metadata['author']
        if author == None:
            author = "None"
        source_name = JAPANESE_SOURCE_NAME[metadata['source_idx']]
        novel_names.append(f"{idx} {novel_name} ({source_name}, 作者:{author})")
    selected_japanese_novel_var.set(novel_names)
    # Set button state
    download_and_convert_btn['state'] = 'disable'

    if auto_download_japanese_var.get() and len(NOVEL_METADATA) == 1:
        SELECTED_IDX = 0
        novel_name = NOVEL_METADATA[SELECTED_IDX]['novel_name']
        output_name_var.set(novel_name)
        output_japanese_name_var.set(novel_name)
        download_and_convert_japanese_novel()

def select_novel(event):
    """確定選取
    """
    global NOVEL_METADATA, SELECTED_IDX
    if len(NOVEL_METADATA) == 0 or len(novel_listbox.curselection()) == 0:
        return

    SELECTED_IDX = novel_listbox.curselection()[0]
    download_and_convert_btn['state'] = 'normal' # Enable convert button
    # Set output name
    novel_name = NOVEL_METADATA[SELECTED_IDX]['novel_name']
    output_name_var.set(end_with_epub(novel_name))

def select_japanese_novel(event):
    """確定選取
    """
    global NOVEL_METADATA, SELECTED_IDX
    if len(NOVEL_METADATA) == 0 or len(japanese_novel_listbox.curselection()) == 0:
        return
    SELECTED_IDX = japanese_novel_listbox.curselection()[0]
    download_and_convert_japanese_btn['state'] = 'normal' # Enable convert button
    # Set output name
    novel_name = NOVEL_METADATA[SELECTED_IDX]['novel_name']
    output_name_var.set(novel_name)
    output_japanese_name_var.set(novel_name)

def download_and_convert_novel():
    global NOVEL_METADATA, FILE_PATH, SELECTED_IDX, DOWNLOADER
    # Get selected novel and its index

    # Download novel and convert
    success = DOWNLOADER.download(NOVEL_METADATA[SELECTED_IDX])
    if not success:
        ERROR_MESSAGE["download_error"]()
        download_and_convert_btn['state'] = 'disable'
        output_name_var.set('')
        return
    FILE_PATH = TMP_TXT_PATH # set global file path for function convert2epub
    convert2epub()
    if NOVEL_METADATA[SELECTED_IDX]['source_idx'] == 0:
        delete_if_exist(TMP_RAR_PATH)

def download_and_convert_japanese_novel():
    global NOVEL_METADATA, SELECTED_IDX, JAPANESE_DOWNLOADER
    # Get selected novel and its index

    # Download novel and convert
    error_code = JAPANESE_DOWNLOADER.download(NOVEL_METADATA[SELECTED_IDX])
    if error_code != 0:
        if error_code == 1:
            ERROR_MESSAGE["download_error"]()
        else:
            ERROR_MESSAGE["copyright_error"]()
        download_and_convert_btn['state'] = 'disable'
        output_name_var.set('')
        return

    # output dir
    output_dir = output_dir_var.get()
    if output_dir == "":
        output_dir = ".\\output"
    output_dir = os.path.join(output_dir, output_japanese_name_var.get())
    os.makedirs(output_dir, exist_ok=True)
    # Get author
    author = NOVEL_METADATA[SELECTED_IDX]['author']
    if author == None:
        author = ""
    books = os.listdir(TMP_DIRECTORY)
    threads = []
    file_names = []
    file_paths = []
    
    
    big_chapters, book_chapters = JAPANESE_DOWNLOADER.get_book_titles(NOVEL_METADATA[SELECTED_IDX])
    for book_idx in range(len(books)):
        path = os.path.join(TMP_DIRECTORY, str(book_idx))
        files = glob.glob(os.path.join(path,'*.txt'))
        txt_file = files[0]
        # This book has images
        imgs_path = os.path.join(path, 'imgs')
        if not os.path.exists(imgs_path):
            imgs_path = ""
        # Get file_name(e.g 第一卷.txt、第三卷.txt), and then convert it to  novel_name + chapter_name
        file_name = os.path.basename(txt_file).replace('.txt','.epub')
        file_names.append(file_name.replace('.epub',''))
        file_name = output_japanese_name_var.get() + ' '+ file_name
        output_path = os.path.join(output_dir, file_name)
        file_paths.append(output_path)

        # set white list 
        cur_white_list = book_chapters[book_idx]
        if len(cur_white_list) == 0:
            cur_white_list = white_list.get("1.0","end-1c").split('\n')
            translate_and_convert_japanese(input_path=txt_file,
                                            output_path=output_path,
                                            white_list=cur_white_list,
                                            black_list=black_list_elements_list,
                                            max_chapter_name_len=max_chapter_len_var.get(),
                                            author=author,
                                            imgs_path=imgs_path)
        else:
            cur_white_list = [f'{big_chapters[book_idx]} {s}'for s in cur_white_list]
            translate_and_convert_japanese(input_path=txt_file,
                                        output_path=output_path,
                                        ordered_white_list=cur_white_list,
                                        black_list=black_list_elements_list,
                                        max_chapter_name_len=max_chapter_len_var.get(),
                                        author=author,
                                        imgs_path=imgs_path)
        # translate_and_convert_japanese(txt_file, output_path, white_list.get("1.0","end-1c").split('\n'), black_list_elements_list, max_chapter_len_var.get(), author, imgs_path)

    for t in threads:
        t.start()
    for t in threads:
        t.join()


    output_path = os.path.join(output_dir, f"{output_japanese_name_var.get()}(全).epub")
    integrate_japanese_epubs(file_paths, file_names, output_path)
    showinfo(title="訊息",message="轉換成功")
    
    # Open explorer
    if open_explorer_var.get() == True:
        path = output_dir_var.get()
        if path == '':
            path = '.'
        path = os.path.join(path, output_japanese_name_var.get())
        open_explorer(path)



### Control ###
tabControl = ttk.Notebook(win)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="epub轉換")
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text="中國小說")
tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text="設定")
tab4 = ttk.Frame(tabControl)
tabControl.add(tab4, text="批量轉換")
tab5 = ttk.Frame(tabControl)
tabControl.add(tab5, text="日輕下載")
tabControl.pack(expand=1,fill="both")

### Tab1: Convert epub ###
monty1 = ttk.LabelFrame(tab1)
monty1.grid(column=0, row=0)
ttk.Button(monty1, text="選擇檔案", command=select_files, style="normal.TButton", width=12).grid(column=0, row=0)
ttk.Entry(monty1, textvariable=file_path_var, state=tk.DISABLED, width=70, font=13).grid(column=1, row=0, padx=10)

ttk.Label(monty1, text="輸入預設目錄", font=lableFrame_font).grid(column=0, row=1, pady=10)
ttk.Entry(monty1, textvariable=input_dir, width=70, font=13).grid(column=1, row=1, pady=10)

ttk.Label(monty1, text="輸出目錄", font=lableFrame_font).grid(column=0, row=2, pady=10)
ttk.Entry(monty1, textvariable=output_dir_var, width=70, font=13).grid(column=1, row=2, pady=10)

ttk.Label(monty1, text="輸出名稱", font=lableFrame_font).grid(column=0, row=3, pady=10)
ttk.Entry(monty1, textvariable=output_name_var, width=70, font=13).grid(column=1, row=3, pady=10)

options = create_label_frame("選項", monty1)
options.grid(column=0, row=4, columnspan=2, pady=8)
ttk.Checkbutton(options, text="完成後開啟目錄",variable=open_explorer_var, style="normal.TCheckbutton").grid(column=0, row=0)
ttk.Checkbutton(options, text="選取後自動解壓縮",variable=auto_extract_var, style="normal.TCheckbutton").grid(column=1, row=0)
ttk.Checkbutton(options, text="選取後直接轉換",variable=auto_convert_var, style="normal.TCheckbutton").grid(column=2, row=0)

convert_btn = ttk.Button(monty1, text="開始轉換", command=convert2epub, state="disable", style="normal.TButton")
convert_btn.grid(column=0, row=5, columnspan=2,pady=8)

chapter_preview_frame = create_label_frame("章節預覽", monty1)
chapter_preview_frame.grid(column=0, row=6, columnspan=2)
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
novel_listbox = tk.Listbox(search_result_frame, listvariable=selected_novel_var, font=10, selectbackground="blue", selectmode="single", width=80)
novel_listbox.bind("<<ListboxSelect>>", select_novel)
novel_listbox.grid(column=0, row=1)


download_options = create_label_frame("", monty2)
download_options.grid(column=0, row=1, columnspan=2)
ttk.Label(download_options, text="輸出目錄", font=lableFrame_font).grid(column=0, row=0, pady=10, padx=5)
ttk.Entry(download_options, textvariable=output_dir_var, width=70, font=13).grid(column=1, row=0, columnspan=2,pady=10)
ttk.Label(download_options, text="輸出名稱", font=lableFrame_font).grid(column=0, row=1, pady=10, padx=5)
ttk.Entry(download_options, textvariable=output_name_var, width=70, font=13).grid(column=1, row=1, columnspan=2,pady=10)

ttk.Checkbutton(download_options, text="完成後開啟目錄",variable=open_explorer_var, style="normal.TCheckbutton").grid(column=0, row=2, columnspan=3,pady=10)


download_and_convert_btn = ttk.Button(download_options, text="下載並轉換", command=download_and_convert_novel, state="disable", style="normal.TButton", width=12)
download_and_convert_btn.grid(column=0, row=3, columnspan=3, pady=10)

# google drive link block
gdrive_frame = create_label_frame("檔案雲端連結", monty2)
gdrive_frame.grid(column=0, row=3, columnspan=2)

gdrive_link_show = ttk.Entry(gdrive_frame, textvariable=gdrive_link_var, width=70, font=13, state="disable")
gdrive_link_show.grid(column=0, row=0, columnspan=2,pady=10)

open_browser_chinese = ttk.Button(gdrive_frame, text="開啟瀏覽器", command=open_gdrive_link, style="normal.TButton", width=12, state="disable")
open_browser_chinese.grid(column=0, row=1, columnspan=1, pady=10)
copy_link_chinese = ttk.Button(gdrive_frame, text="複製到剪貼簿", command=copy_gdrive_link, style="normal.TButton", width=12, state="disable")
copy_link_chinese.grid(column=1, row=1, columnspan=1, pady=10)


### Tab3: Convert epub ###
def reset_white_list():
    clear_text_var(white_list)
    white_list.insert(tk.INSERT, "\n".join(FINDS))

def reset_black_list():
    global black_list_elements_list
    black_list_elements.set([])
    black_list_delete_btn['state'] = 'disable'
    black_list_elements_list = []
def reset_setting():
    max_chapter_len_var.set(MAX_CHAPTER_NAME_LEN)
    reset_white_list()
    reset_black_list()

def add_new_black_list():
    if new_black_list_element.get() != "":
        black_list_elements_list.append(new_black_list_element.get())
        black_list_elements.set(black_list_elements_list)
        new_black_list_element.set('')

def select_black_element(event):
    """確定選取黑名單元素
    """
    global BLACKED_ELEMENT_SELECTED_IDX
    if len(black_list_elements_list) == 0 or len(black_list_listbox.curselection()) == 0:
        return
    BLACKED_ELEMENT_SELECTED_IDX = black_list_listbox.curselection()[0]
    black_list_delete_btn['state'] = 'normal' # Enable convert button

def delete_black_element():
    global BLACKED_ELEMENT_SELECTED_IDX
    black_list_elements_list.remove(black_list_elements_list[BLACKED_ELEMENT_SELECTED_IDX])
    black_list_elements.set(black_list_elements_list)
    black_list_delete_btn['state'] = 'disable'


monty3 = ttk.LabelFrame(tab3)
monty3.grid(column=0, row=0)
ttk.Button(monty3, text="重置設定", command=reset_setting, style="normal.TButton", width=12).grid(column=0, row=0)
max_chapter_len = create_label_frame("章節名稱最大長度", monty3)
max_chapter_len.grid(column=0, row=1, columnspan=1, pady=8)
ttk.Spinbox(max_chapter_len, textvariable=max_chapter_len_var, from_=10, to=100, font=12).grid(column=0, row=0)

white_list_frame = create_label_frame("章節白名單", monty3)
white_list_frame.grid(column=0, row=2, columnspan=1, pady=8)

ttk.Button(white_list_frame, text="回復預設", command=reset_white_list, style="normal.TButton", width=12).grid(column=0, row=0)
white_list = ScrolledText(white_list_frame, font=5, height=10,wrap=tk.WORD)
white_list.grid(column=0, row=1, ipady=5)
white_list.insert(tk.INSERT, "\n".join(FINDS))

black_list_frame = create_label_frame("章節黑名單", monty3)
black_list_frame.grid(column=0, row=3, columnspan=1, pady=8)

ttk.Entry(black_list_frame, textvariable=new_black_list_element, width=70, font=13).grid(column=0, row=0, columnspan=3, padx=10)

ttk.Button(black_list_frame, text="加入", command=add_new_black_list, style="normal.TButton", width=12).grid(column=0, row=1)
black_list_delete_btn = ttk.Button(black_list_frame, text="刪除所選項", command=delete_black_element, style="normal.TButton", width=12, state=tk.DISABLED)
black_list_delete_btn.grid(column=1, row=1)
ttk.Button(black_list_frame, text="清空", command=reset_black_list, style="normal.TButton", width=12).grid(column=2, row=1)

black_list_listbox = tk.Listbox(black_list_frame, listvariable=black_list_elements, font=10, selectbackground="blue", selectmode="single", width=60)
black_list_listbox.bind("<<ListboxSelect>>", select_black_element)
black_list_listbox.grid(column=0, row=2, rowspan=1,columnspan=3)
#ttk.Button(monty3, text="儲存設定", command=select_files, style="normal.TButton", width=12).grid(column=0, row=4)

### Tab4: Convert epub ###

def convert2epub_multi():
    global multi_file_paths
    # get output directory
    output_dir = output_dir_var.get()
    if output_dir == "":
        output_dir = ".\\output"
    # get output names 
    multi_output_names = multi_output_name_block_text.get("1.0","end-1c").split('\n')
    preview_texts = ""
    for in_f, out_f in zip(multi_file_paths, multi_output_names):
        output_path = os.path.join(output_dir, out_f)
        try:
            chapters = translate_and_convert(in_f, output_path, white_list.get("1.0","end-1c").split('\n'), black_list_elements_list, max_chapter_len_var.get())
            preview_texts += out_f + ":\n"+ '-'*100 + '\n' + "".join(chapters) + '\n' + '-'*100 + '\n'
        except UnicodeDecodeError:
            ERROR_MESSAGE['read_error']()
            return

    # clear chapter preview
    clear_text_var(multi_chapter_preview)
    multi_chapter_preview.insert(tk.INSERT, preview_texts)
    showinfo(title="訊息",message="轉換成功")
    
    # Open explorer
    if open_explorer_var.get() == True:
        path = output_dir_var.get()
        if path == '':
            path = '.'
        open_explorer(path)

def select_multi_files():
    global multi_file_paths
    filetypes = [('Accepted files', '*.txt'),
                ('text files', '*.txt'),
]
    file_path = fd.askopenfilenames(
        title='Open files',
        initialdir=input_dir.get(),
        filetypes=filetypes)

    # Cancel
    if file_path == '':
        return

    multi_file_paths = file_path
    #print(multi_file_paths)
    clear_text_var(multi_select_file_block_text)
    multi_select_file_block_text.insert(tk.INSERT, "\n".join(multi_file_paths))
    
    # Get book name from file name
    multi_output_names = [] # reset variable
    for f in multi_file_paths:
        book_name = os.path.splitext(os.path.basename(f))[0]
        book_name = simple2Trad(book_name)
        multi_output_names.append(end_with_epub(book_name))

    clear_text_var(multi_output_name_block_text)
    multi_output_name_block_text.insert(tk.INSERT, "\n".join(multi_output_names))
    multi_convert_btn['state'] = 'normal'
    clear_text_var(multi_chapter_preview)

    # Auto convert
    if auto_convert_var.get() == True:
        convert2epub_multi()

monty4 = ttk.LabelFrame(tab4)
monty4.grid(column=0, row=0)

select_file_frame = create_label_frame("選擇檔案", monty4)
select_file_frame.grid(column=0, row=0, columnspan=2, pady=8)

ttk.Button(select_file_frame, text="選擇", command=select_multi_files, style="normal.TButton", width=12).grid(column=0, row=0)
multi_select_file_block_text = ScrolledText(select_file_frame, height=5, font=5,wrap=tk.WORD)
multi_select_file_block_text.grid(column=0, row=1, ipady=5)

ttk.Label(monty4, text="輸入目錄", font=lableFrame_font).grid(column=0, row=1, pady=10)
ttk.Entry(monty4, textvariable=input_dir, width=70, font=13).grid(column=1, row=1, pady=10)

ttk.Label(monty4, text="輸出目錄", font=lableFrame_font).grid(column=0, row=2, pady=10)
ttk.Entry(monty4, textvariable=output_dir_var, width=70, font=13).grid(column=1, row=2, pady=10)

output_file_frame = create_label_frame("輸出名稱", monty4)
output_file_frame.grid(column=0, row=3, columnspan=2, pady=8)
multi_output_name_block_text = ScrolledText(output_file_frame, height=5, font=5,wrap=tk.WORD)
multi_output_name_block_text.grid(column=0, row=0, ipady=5)

options = create_label_frame("選項", monty4)
options.grid(column=0, row=4, columnspan=2, pady=8)
ttk.Checkbutton(options, text="完成後開啟目錄",variable=open_explorer_var, style="normal.TCheckbutton").grid(column=0, row=0)
ttk.Checkbutton(options, text="選取後直接轉換",variable=auto_convert_var, style="normal.TCheckbutton").grid(column=1, row=0)

multi_convert_btn = ttk.Button(monty4, text="開始批次轉換", command=convert2epub_multi, state="disable", style="normal.TButton")
multi_convert_btn.grid(column=0, row=5, columnspan=2,pady=8)

chapter_preview_frame = create_label_frame("章節預覽", monty4)
chapter_preview_frame.grid(column=0, row=6, columnspan=2)
multi_chapter_preview = ScrolledText(chapter_preview_frame, font=5,wrap=tk.WORD, height=13)
multi_chapter_preview.grid(column=0, row=0, columnspan=2, ipady=5)

### Tab5: Download japenese novel ###
monty5 = ttk.LabelFrame(tab5)
monty5.grid(column=0, row=0)

search_frame = create_label_frame("搜尋", monty5)
search_frame.grid(column=0, row=0, columnspan=2)
ttk.Entry(search_frame, textvariable=search_var, width=70, font=12).grid(column=0, row=0, padx=10)
ttk.Button(search_frame, text="搜尋", command=search_japanese_novel, style="normal.TButton", width=12).grid(column=1, row=0)

search_result_frame = create_label_frame("搜尋結果", search_frame)
search_result_frame.grid(column=0, row=1, columnspan=2)


# Novel List box
japanese_novel_listbox = tk.Listbox(search_result_frame, listvariable=selected_japanese_novel_var, font=10, selectbackground="blue", selectmode="single", width=80)
japanese_novel_listbox.bind("<<ListboxSelect>>", select_japanese_novel)
japanese_novel_listbox.grid(column=0, row=1)


download_options = create_label_frame("", monty5)
download_options.grid(column=0, row=1, columnspan=2)
ttk.Label(download_options, text="輸出目錄", font=lableFrame_font).grid(column=0, row=0, pady=10, padx=5)
ttk.Entry(download_options, textvariable=output_dir_var, width=70, font=13).grid(column=1, row=0, columnspan=2,pady=10)
ttk.Label(download_options, text="下載項目", font=lableFrame_font).grid(column=0, row=1, pady=10, padx=5)
ttk.Entry(download_options, textvariable=output_name_var, width=70, font=13, state=tk.DISABLED).grid(column=1, row=1, columnspan=2,pady=10)
ttk.Label(download_options, text="輸出檔名", font=lableFrame_font).grid(column=0, row=2, pady=10, padx=5)
ttk.Entry(download_options, textvariable=output_japanese_name_var, width=70, font=13).grid(column=1, row=2, columnspan=2,pady=10)


options = create_label_frame("選項", download_options)
options.grid(column=0, row=3, columnspan=3, pady=8)
ttk.Checkbutton(options, text="完成後開啟目錄",variable=open_explorer_var, style="normal.TCheckbutton").grid(column=0, row=0)
#ttk.Checkbutton(options, text="只有一結果時直接下載",variable=auto_download_japanese_var, style="normal.TCheckbutton").grid(column=1, row=0)
#ttk.Checkbutton(options, text="整合全卷",variable=auto_convert_var, style="normal.TCheckbutton").grid(column=2, row=0)


download_and_convert_japanese_btn = ttk.Button(download_options, text="下載並轉換", command=download_and_convert_japanese_novel, state="disable", style="normal.TButton", width=12)
download_and_convert_japanese_btn.grid(column=0, row=4, columnspan=3, pady=10)

# google drive link block
gdrive_frame = create_label_frame("檔案雲端連結", monty5)
gdrive_frame.grid(column=0, row=5, columnspan=2)

gdrive_link_show = ttk.Entry(gdrive_frame, textvariable=gdrive_link_var, width=70, font=13, state="disable")
gdrive_link_show.grid(column=0, row=0, columnspan=2,pady=10)

open_browser_japanese = ttk.Button(gdrive_frame, text="開啟瀏覽器", command=open_gdrive_link, style="normal.TButton", width=12, state="disable")
open_browser_japanese.grid(column=0, row=1, columnspan=1, pady=10)
copy_link_japanese = ttk.Button(gdrive_frame, text="複製到剪貼簿", command=copy_gdrive_link, style="normal.TButton", width=12, state="disable")
copy_link_japanese.grid(column=1, row=1, columnspan=1, pady=10)

if __name__ == "__main__":
    win.mainloop()