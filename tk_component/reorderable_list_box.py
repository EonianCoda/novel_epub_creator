import tkinter as tk
from tkinter import Listbox
from tkinter.font import Font
from typing import List

class ReorderableListbox(tk.Frame):
    def __init__(self, parent, font_size=12):
        super().__init__(parent)

        # 設定字體大小
        self.font = Font(size=font_size)
        
        # 建立 Listbox，設置字體和大小
        self.listbox = Listbox(self, selectmode=tk.SINGLE, height=10, font=self.font)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # 綁定拖放事件
        self.listbox.bind("<Button-1>", self.on_select)
        self.listbox.bind("<B1-Motion>", self.on_drag)
        self.listbox.bind("<ButtonRelease-1>", self.on_drop)

        self.selected_index = None  # 儲存目前選擇的項目索引
        self.highlighted_index = None  # 儲存當前加深底色的項目索引

    def on_select(self, event):
        """記錄使用者選中的項目"""
        self.selected_index = self.listbox.nearest(event.y)
        self.update_highlight(self.selected_index)

    def on_drag(self, event):
        """實時移動選中的項目，並更新底色"""
        if self.selected_index is not None:
            new_index = self.listbox.nearest(event.y)
            if new_index != self.selected_index:
                self.swap_items(self.selected_index, new_index)
                self.selected_index = new_index
                self.update_highlight(self.selected_index)

    def on_drop(self, event):
        """清空選中狀態並重置底色"""
        self.clear_highlight()
        self.selected_index = None

    def swap_items(self, index1, index2):
        """交換兩個項目的位置"""
        item1 = self.listbox.get(index1)
        item2 = self.listbox.get(index2)
        self.listbox.delete(index1)
        self.listbox.insert(index1, item2)
        self.listbox.delete(index2)
        self.listbox.insert(index2, item1)

    def update_highlight(self, index):
        """加深選中項目的底色"""
        self.clear_highlight()  # 清除之前的加深底色
        self.listbox.itemconfig(index, background="#0078D7")  # 設置新底色
        self.highlighted_index = index

    def clear_highlight(self):
        """清除所有項目的加深底色"""
        if self.highlighted_index is not None:
            self.listbox.itemconfig(self.highlighted_index, background="white")
            self.highlighted_index = None

    def insert_items(self, items):
        """插入多個項目，並更新寬度"""
        for item in items:
            self.listbox.insert(tk.END, item)
        self.update_width()

    def update_width(self):
        """根據最長的項目動態調整 Listbox 寬度"""
        max_width = 0
        for item in self.listbox.get(0, tk.END):
            item_width = self.font.measure(item)  # 計算項目的像素寬度
            max_width = max(max_width, item_width)
        # 將像素寬度轉換為字符寬度
        char_width = max_width // self.font.measure("0") + 2
        self.listbox.config(width=char_width)

    def get_items(self):
        """取得清單的最終順序"""
        return list(self.listbox.get(0, tk.END))

    def clear_items(self):
        """清空所有清單項目"""
        self.listbox.delete(0, tk.END)

if __name__ == "__main__":
    from tkinter import messagebox
    # 建立主視窗
    root = tk.Tk()
    root.title("可調整順序的清單（獲取最終順序）")

    # 建立可調整順序的清單
    reorderable_listbox = ReorderableListbox(root)
    reorderable_listbox.pack(fill=tk.BOTH, expand=True)

    # 插入初始項目
    items = ["項目 1", "項目 2", "項目 3", "項目 4", "項目 5"]
    reorderable_listbox.insert_items(items)

    # 新增按鈕來顯示最終順序
    def show_final_order():
        order = reorderable_listbox.get_items()
        messagebox.showinfo("清單順序", f"最終順序：\n{', '.join(order)}")

    btn_get_order = tk.Button(root, text="獲取清單順序", command=show_final_order)
    btn_get_order.pack(pady=10)

    # 運行主迴圈
    root.mainloop()