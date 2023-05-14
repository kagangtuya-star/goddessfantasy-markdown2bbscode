import os
import tkinter as tk
import tkinter.filedialog as filedialog
import markdown
import re
from tkinter import messagebox


# 将 Markdown 转换为 BBSCode
def markdown_to_bbscode(markdown_text):
    # 将引用转换为 BBSCode
    markdown_text = re.sub(r'^>.*$', lambda m: '[quote]' + m.group(0)[1:].strip() + '[/quote]\n', markdown_text,
                           flags=re.MULTILINE)
    # 将表格转换为 BBSCode
    markdown_text = re.sub(r'\|(.+)\|\n\|([\s-]+\|)+\n((\|.+?\|\n)+)', convert_table, markdown_text, flags=re.MULTILINE)
    # 将无序列表转换为 BBSCode 标签
    markdown_text = re.sub(r'^- (.*)$', '[list]\n[li]\\1[/li]\n[/list]', markdown_text, flags=re.MULTILINE)
    # 将有序列表转换为 BBSCode 标签
    markdown_text = re.sub(r'^\d+\. (.*)$', '[list type=decimal]\n[li]\\1[/li]\n[/list]', markdown_text,
                           flags=re.MULTILINE)
    # 将各种 Markdown 语法转换为对应的 BBSCode 标签
    markdown_text = re.sub(r'^# (.*)$', '[size=6][b]\\1[/b][/size]\n', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^## (.*)$', '[size=5][b]\\1[/b][/size]\n', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^### (.*)$', '[size=4][b]\\1[/b][/size]\n', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^#### (.*)$', '[size=3][b]\\1[/b][/size]\n', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^##### (.*)$', '[size=2][b]\\1[/b][/size]\n', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^###### (.*)$', '[size=1][b]\\1[/b][/size]\n', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'\*\*(.*?)\*\*', '[b]\\1[/b]', markdown_text)
    markdown_text = re.sub(r'__(.*?)__', '[u]\\1[/u]', markdown_text)
    markdown_text = re.sub(r'\*(.*?)\*', '[i]\\1[/i]', markdown_text)
    markdown_text = re.sub(r'_(.*?)_', '[i]\\1[/i]', markdown_text)
    markdown_text = re.sub(r'~~(.*?)~~', '[s]\\1[/s]', markdown_text)
    markdown_text = re.sub(r'```([^`]*)```', '[code]\\1[/code]', markdown_text)
    markdown_text = re.sub(r'\n\*\s(.*)$', '[*] \\1', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'<(https?://.*?)>', '[url]\\1[/url]', markdown_text)
    markdown_text = re.sub(r'!\[(.*?)\]\((.*?)\)', '[img]\\2[/img]', markdown_text)
    markdown_text = re.sub(r'\n-{3,}', '\n[hr]', markdown_text)

    # 下划线紧凑美观
    markdown_text = re.sub(r'(?<=\[/size\]\n)\s*(\n+)\s*(?=\[hr\])', '', markdown_text, flags=re.MULTILINE)
    # 返回转换后的 BBSCode
    return markdown_text.strip()


# 将表格转换为 BBSCode
def convert_table(match):
    # 将输入按换行符拆分成行列表
    lines = match.group(0).strip().split('\n')

    # 移除分隔行（第二行）
    lines.pop(1)

    # 初始化BBCode表格
    bbcode_table = "[table]\n"

    # 遍历处理每一行
    for i, line in enumerate(lines):
        # 根据 | 符号拆分单元格
        cells = line.split('|')[1:-1]

        # 初始化BBCode行
        bbcode_row = "[tr]\n"

        # 遍历处理每个单元格
        for cell in cells:
            cell_content = cell.strip()

            # 如果是标题行（第一行），添加粗体标签
            if i == 0:
                cell_content = f"[b]{cell_content}[/b]"

            # 将单元格内容添加到BBCode行中
            bbcode_row += f"[td]{cell_content}[/td]"

        # 完成BBCode行并将其添加到BBCode表格中
        bbcode_row += "\n[/tr]"
        bbcode_table += bbcode_row

    # 完成BBCode表格
    bbcode_table += "\n[/table]"

    return bbcode_table


# 打开 Markdown 文件并将其转换为 BBSCode
def open_and_convert():
    # 使用文件对话框选择文件
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('Markdown 文件', '*.md')])
    # 如果用户选择了文件，则打开文件并将其转换为 BBSCode
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        bbscode_text = markdown_to_bbscode(markdown_text)
        # 将 BBSCode 写入同一路径下的 txt 文件
        txt_file_path = os.path.splitext(file_path)[0] + '.txt'
        with open(txt_file_path, 'w', encoding='utf-8') as f:
            f.write(bbscode_text)
        messagebox.showinfo(title='提示', message='已将 BBSCode 输出到' + txt_file_path)
    else:
        messagebox.showinfo(title='提示', message='未选择文件')


# 创建 GUI 窗口
root = tk.Tk()
root.title('Markdown 转换为 BBSCode')
# 创建按钮
button = tk.Button(root, text='选择 Markdown 文件并转换', command=open_and_convert)
button.pack(padx=20, pady=20)


# 关闭窗口时退出程序
def on_closing():
    root.destroy()
    exit()


root.protocol("WM_DELETE_WINDOW", on_closing)
# 运行 GUI 窗口
root.mainloop()
