import json
import os
import tkinter as tk
from tkinter import messagebox, font
from tkinter import filedialog
from PIL import Image, ImageTk


def main():
    # 初始化Tkinter窗口
    root = tk.Tk()
    root.title("数据标注工具 by Yo1ogreyZz")
    root.geometry("1200x800")
    root.configure(bg="#f0f0f0")

    # 定义全局字体
    global_font = font.Font(family="Times New Roman", size=12)

    # 显示标注进度
    frame_filename = tk.Frame(root, bg="#f0f0f0", pady=10)
    frame_filename.pack(fill="x")
    label_filename = tk.Label(frame_filename, text="标注数据: 1/...", bg="#f0f0f0", font=global_font)
    label_filename.pack(side="left", padx=10)

    # 图像显示框架
    frame_image = tk.Frame(root, bg="#f0f0f0", pady=10)
    frame_image.pack(side="left", padx=10)
    label_image = tk.Label(frame_image, text="图像:", bg="#f0f0f0", font=global_font)
    label_image.pack()
    canvas_image = tk.Canvas(frame_image, width=400, height=400, bg="#ffffff")
    canvas_image.pack()

    # 问题显示框架
    frame_question = tk.Frame(root, bg="#f0f0f0", pady=10)
    frame_question.pack(fill="x")
    label_question = tk.Label(frame_question, text="问题:", bg="#f0f0f0", font=global_font)
    label_question.pack(anchor="w", padx=10)
    text_question = tk.Text(frame_question, height=2, width=100, wrap="word", bg="#ffffff", relief="solid", bd=1,
                            font=global_font)
    text_question.pack(padx=10, pady=5)
    text_question.config(state=tk.DISABLED)  # 设置为只读

    # 答案显示框架
    frame_content = tk.Frame(root, bg="#f0f0f0", pady=10)
    frame_content.pack(fill="both", expand=True)
    label_content = tk.Label(frame_content, text="原始答案:", bg="#f0f0f0", font=global_font)
    label_content.pack(anchor="w", padx=10)
    text_content = tk.Text(frame_content, height=10, width=100, wrap="word", bg="#ffffff", relief="solid", bd=1,
                           font=global_font)
    text_content.pack(padx=10, pady=5)
    text_content.config(state=tk.DISABLED)  # 设置为只读

    # 修正答案输入框架
    frame_fix_content = tk.Frame(root, bg="#f0f0f0", pady=10)
    frame_fix_content.pack(fill="both", expand=True)
    label_fix_content = tk.Label(frame_fix_content, text="修正答案:", bg="#f0f0f0", font=global_font)
    label_fix_content.pack(anchor="w", padx=10)
    text_fix_content = tk.Text(frame_fix_content, height=10, width=100, wrap="word", bg="#ffffff", relief="solid", bd=1,
                               font=global_font)
    text_fix_content.pack(padx=10, pady=5)

    # 提交、下一条、上一条和退出按钮
    frame_button = tk.Frame(root, bg="#f0f0f0", pady=10)
    frame_button.pack(fill="x")
    button_container = tk.Frame(frame_button, bg="#f0f0f0")
    button_container.pack(expand=True)
    button_submit = tk.Button(button_container, text="保存修改", bg="#4CAF50", fg="white", relief="raised", bd=2,
                              font=global_font, width=20, height=2)
    button_submit.pack(side="left", padx=10, pady=10)
    button_previous = tk.Button(button_container, text="上一条", bg="#2196F3", fg="white", relief="raised", bd=2,
                                font=global_font, width=20, height=2)
    button_previous.pack(side="left", padx=10, pady=10)
    button_next = tk.Button(button_container, text="下一条", bg="#2196F3", fg="white", relief="raised", bd=2,
                            font=global_font, width=20, height=2)
    button_next.pack(side="left", padx=10, pady=10)
    button_exit = tk.Button(button_container, text="退出", bg="#f44336", fg="white", relief="raised", bd=2,
                            font=global_font, width=20, height=2)
    button_exit.pack(side="left", padx=10, pady=10)

    # 创建输出目录
    output_dir = 'fixed_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    record_index = 1
    input_index = 1
    question_index = 0
    total_files = len(os.listdir('./origin_data'))
    current_data = []
    current_file = ""
    fixed_data = []

    def load_image(image_path):
        try:
            image = Image.open(image_path)
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            canvas_image.create_image(0, 0, anchor=tk.NW, image=photo)
            canvas_image.image = photo
        except Exception as e:
            print(f"加载图像出错: {e}")
            canvas_image.image = None

    def save_data():
        nonlocal record_index, current_file, fixed_data

        output_file = os.path.join(output_dir, f'fixed_data{input_index}.json')

        # 添加 image_number 和 image_url 到 fixed_data 的开头
        annotated_data = {
            "image_number": input_index,
            "image_url": f"images/image{input_index}.jpg"
        }
        all_data = [annotated_data] + fixed_data

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

        print(f"\n标注数据已保存到 {output_file}")

    def load_file(file_index):
        nonlocal input_index, question_index, current_data, current_file, fixed_data

        if file_index < 1 or file_index > total_files:
            messagebox.showinfo("信息", "没有更多文件进行标注！")
            return

        try:
            input_index = file_index
            question_index = 0
            current_file = f'./origin_data/response{input_index}.json'
            with open(current_file, 'r', encoding='utf-8') as f:
                current_data = json.load(f)

            label_filename.config(text=f"标注数据: {input_index}/{total_files}")

            load_image(f'./images/image{input_index}.jpg')

            fixed_file = os.path.join(output_dir, f'fixed_data{input_index}.json')
            if os.path.exists(fixed_file):
                with open(fixed_file, 'r', encoding='utf-8') as f:
                    fixed_data = json.load(f)[1:]  # 跳过第一个字典
            else:
                fixed_data = []

            load_question(question_index)

        except FileNotFoundError:
            messagebox.showinfo("信息", "没有更多文件进行标注！")
            root.destroy()

    def load_question(q_index):
        nonlocal current_data, question_index, fixed_data

        if q_index < 0 or q_index >= len(current_data):
            messagebox.showinfo("信息", "该文件中没有更多问题！")
            return

        question_index = q_index
        question_value = current_data[question_index]['question']
        content_value = current_data[question_index]['response']['choices'][0]['message']['content'][0]['text']

        if question_index < len(fixed_data):
            fix_content_value = fixed_data[question_index]['fixed_answer']
        else:
            fix_content_value = content_value

        text_question.config(state=tk.NORMAL)
        text_question.delete("1.0", tk.END)
        text_question.insert(tk.END, question_value)
        text_question.config(state=tk.DISABLED)

        text_content.config(state=tk.NORMAL)
        text_content.delete("1.0", tk.END)
        text_content.insert(tk.END, content_value)
        text_content.config(state=tk.DISABLED)

        text_fix_content.delete("1.0", tk.END)
        text_fix_content.insert(tk.END, fix_content_value)

    def on_submit():
        nonlocal fixed_data

        fix_content_value = text_fix_content.get("1.0", tk.END).strip()
        content_value = text_content.get("1.0", tk.END).strip()

        annotated_data = {
            "question": current_data[question_index]['question'],
            "answer": content_value,
            "fixed_answer": fix_content_value
        }

        if question_index < len(fixed_data):
            fixed_data[question_index] = annotated_data
        else:
            fixed_data.append(annotated_data)

        save_data()
        if question_index < len(current_data) - 1:
            load_question(question_index + 1)
        else:
            load_file(input_index + 1)

    def on_previous():
        if question_index > 0:
            load_question(question_index - 1)
        elif input_index > 1:
            load_file(input_index - 1)

    def on_next():
        if question_index < len(current_data) - 1:
            load_question(question_index + 1)
        elif input_index < total_files:
            load_file(input_index + 1)

    def on_exit():
        root.destroy()

    button_submit.config(command=on_submit)
    button_previous.config(command=on_previous)
    button_next.config(command=on_next)
    button_exit.config(command=on_exit)

    # 加载第一个文件
    load_file(input_index)

    # 启动Tkinter事件循环
    root.mainloop()


if __name__ == '__main__':
    main()