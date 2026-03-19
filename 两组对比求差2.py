#!/usr/bin/env python3
# compare_diff_gui.py
# GUI 工具：比较两个表格（CSV/Excel），提取只在 A 表中出现、不在 B 表中出现的行

import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def read_table(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.csv', '.txt']:
        return pd.read_csv(path, dtype=str)
    elif ext in ['.xls', '.xlsx']:
        return pd.read_excel(path, dtype=str)
    else:
        raise ValueError(f"不支持的文件格式: {ext}")

def write_table(df, path):
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.csv', '.txt']:
        df.to_csv(path, index=False, encoding='utf-8')
    elif ext in ['.xls', '.xlsx']:
        df.to_excel(path, index=False)
    else:
        raise ValueError(f"不支持的输出格式: {ext}")

def run_compare():
    file_a = entry_a.get().strip()
    file_b = entry_b.get().strip()
    key_a = entry_key_a.get().strip()
    key_b = entry_key_b.get().strip()
    output = entry_out.get().strip()
    if not all([file_a, file_b, key_a, key_b, output]):
        messagebox.showwarning("提示", "请填写所有字段！")
        return
    try:
        df_a = read_table(file_a)
        df_b = read_table(file_b)
    except Exception as e:
        messagebox.showerror("读取错误", str(e))
        return

    if key_a not in df_a.columns:
        messagebox.showerror("列名错误", f"A 表中不存在列: {key_a}")
        return
    if key_b not in df_b.columns:
        messagebox.showerror("列名错误", f"B 表中不存在列: {key_b}")
        return

    # 去重
    df_a = df_a.drop_duplicates(subset=[key_a], keep='first')
    df_b = df_b.drop_duplicates(subset=[key_b], keep='first')

    # 差集
    mask = ~df_a[key_a].isin(df_b[key_b])
    df_diff = df_a[mask]

    # 保存
    try:
        write_table(df_diff, output)
    except Exception as e:
        messagebox.showerror("保存错误", str(e))
        return

    messagebox.showinfo("完成", f"共提取 {len(df_diff)} 条记录，已保存到：\n{output}")

# GUI 界面搭建
root = tk.Tk()
root.title("表格差集提取工具")
root.geometry("620x280")
root.resizable(False, False)

padx, pady = 10, 8

# 表 A
tk.Label(root, text="表 A (CSV/Excel)：").grid(row=0, column=0, sticky="e", padx=padx, pady=pady)
entry_a = tk.Entry(root, width=50)
entry_a.grid(row=0, column=1, padx=padx, pady=pady)
tk.Button(root, text="浏览…", command=lambda: entry_a.insert(0, filedialog.askopenfilename())).grid(row=0, column=2, padx=padx)

# 表 B
tk.Label(root, text="表 B (CSV/Excel)：").grid(row=1, column=0, sticky="e", padx=padx, pady=pady)
entry_b = tk.Entry(root, width=50)
entry_b.grid(row=1, column=1, padx=padx, pady=pady)
tk.Button(root, text="浏览…", command=lambda: entry_b.insert(0, filedialog.askopenfilename())).grid(row=1, column=2, padx=padx)

# A 表 对比列
tk.Label(root, text="A 表 对比列名：").grid(row=2, column=0, sticky="e", padx=padx, pady=pady)
entry_key_a = tk.Entry(root, width=20)
entry_key_a.grid(row=2, column=1, sticky="w", padx=padx, pady=pady)

# B 表 对比列
tk.Label(root, text="B 表 对比列名：").grid(row=3, column=0, sticky="e", padx=padx, pady=pady)
entry_key_b = tk.Entry(root, width=20)
entry_key_b.grid(row=3, column=1, sticky="w", padx=padx, pady=pady)

# 输出
tk.Label(root, text="输出文件：").grid(row=4, column=0, sticky="e", padx=padx, pady=pady)
entry_out = tk.Entry(root, width=50)
entry_out.grid(row=4, column=1, padx=padx, pady=pady)
tk.Button(root, text="保存为…", command=lambda: entry_out.insert(0, filedialog.asksaveasfilename(
    defaultextension=".xlsx",
    filetypes=[("Excel","*.xlsx;*.xls"),("CSV","*.csv")]
))).grid(row=4, column=2, padx=padx)

# 运行按钮
tk.Button(root, text="运行", width=12, command=run_compare).grid(row=5, column=1, pady=20)

root.mainloop()