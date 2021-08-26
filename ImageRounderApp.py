import os
import threading
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from icon_data import icon_data
from image_rounder import round_image

file_separate_sign = "|"
max_progress = 100

def on_click_input_files_dialog():
    progress.set(40)
    input_images_path = filedialog.askopenfilename(
        multiple=True
    )
    in_file_path_var.set(file_separate_sign.join(input_images_path))

def on_click_output_dir_dialog():
    progress.set(10)
    init_dir = os.path.abspath(os.path.dirname(__file__))
    output_folder_path = filedialog.askdirectory(initialdir = init_dir)
    out_dir_path_var.set(output_folder_path)

def on_click_size_help():
    messagebox.showinfo("ヘルプ", "ヒャッハーーっ❕❕\n画像はそれぞれ以下のようなwidth(横幅)に統一されるぞ❕❕\n\n・small: 300px\n・large: 700px\n\nこれでいちいちPremiere proで大きさを変更しなくて済むぞ、感謝するんだな❕❕")

def round_image_target(input_images_path_list, output_folder_path):
    progressbar.pack(fill="x", side="left")
    progress.set(0)
    resize_px = 300 if size_var.get() == "small" else 700
    for i, input_image_path in enumerate(input_images_path_list):
        round_image(input_image_path, output_folder_path, resize_px)
        next_progress = ((i + 1) / len(input_images_path_list)) * max_progress
        progress.set(int(next_progress))
    messagebox.showinfo("完了", "ヒャッハーーっ❕❕\n俺様がズタズタに切り裂いてやったぞ❕❕\n次の獲物は貴様かもな❕❕震えて眠るんだな❕❕ヒャッハーーっ❕❕")
    progressbar.pack_forget()

def exe_round_image():
    input_images_path_list = in_file_path_var.get().split(file_separate_sign)
    output_folder_path = out_dir_path_var.get()
    if not input_images_path_list or len(input_images_path_list) > 0 and not input_images_path_list[0]:
        messagebox.showerror("エラー", "ヒャッハーーっ❕❕\n入力画像が選択されてないぜ❕❕\nさすがの俺様も無いもんは斬れねえぜ❕❔")
        return
    if not output_folder_path:
        messagebox.showerror("エラー", "ヒャッハーーっ❕❕\n出力フォルダが選択されてないぜ❕❕\n斬った獲物達をこの俺様が持って帰って喰っちまうぜ❕❔")
        return

    t = threading.Thread(target=round_image_target, args=(input_images_path_list, output_folder_path))
    t.start()


if __name__ == "__main__":

    # root
    root = Tk()
    root.tk.call("wm", "iconphoto", root._w, PhotoImage(data=icon_data))
    root.title("画像丸々カットくん")

    # Frame2
    in_file_container = ttk.Frame(root, padding=10)
    in_file_container.grid(row=0, column=1, sticky=E)
    in_file_label = ttk.Label(in_file_container, text="入力画像 (複数可)", padding=(5, 2))
    in_file_label.pack(side=LEFT)
    in_file_path_var = StringVar()
    in_file_entry = ttk.Entry(in_file_container, textvariable=in_file_path_var, width=30)
    in_file_entry.pack(side=LEFT)
    in_file_button = ttk.Button(in_file_container, text="参照", command=on_click_input_files_dialog)
    in_file_button.pack(side=LEFT)

    # Frame1
    out_dir_container = ttk.Frame(root, padding=10)
    out_dir_container.grid(row=2, column=1, sticky=E)
    out_dir_label = ttk.Label(out_dir_container, text="出力フォルダ", padding=(5, 2))
    out_dir_label.pack(side=LEFT)
    out_dir_path_var = StringVar()
    out_dir_entry = ttk.Entry(out_dir_container, textvariable=out_dir_path_var, width=30)
    out_dir_entry.pack(side=LEFT)
    out_dir_button = ttk.Button(out_dir_container, text="参照", command=on_click_output_dir_dialog)
    out_dir_button.pack(side=LEFT)

    size_container = ttk.Frame(root, padding=10)
    label = ttk.Label(size_container, text="サイズ", padding=(5, 2))
    label.grid(row=1, column=1)
    size_var = StringVar()
    size_var.set("small")
    size_combo = ttk.Combobox(
        size_container,
        textvariable=size_var,
        values=[
            "small",
            "large",
        ],
        width=30,
        state="readonly",
    )
    size_combo.grid(row=1, column=2)
    size_help_button = ttk.Button(size_container, text="?", width=4, command=on_click_size_help)
    size_help_button.grid(row=1, column=3, padx=4)
    size_container.grid(row=3, column=1)

    exe_button = ttk.Button(root, text="実行", command=exe_round_image)
    exe_button.grid(row=4, column=1, pady=20, ipadx=30)

    progressbar_container = ttk.Frame(root, padding=10)
    progressbar_container.grid(row=6, column=1, sticky="w")
    progress = IntVar(value=0)
    progressbar = ttk.Progressbar(
        progressbar_container,
        length=380,
        maximum=max_progress,
        mode="determinate",
        variable=progress,
    )

    root.mainloop()
# pyinstaller ImageRounderApp.py --onefile --noconsole --icon=icon.ico --name 画像丸々カットくん
# certutil -encode icon.gif icon.txt