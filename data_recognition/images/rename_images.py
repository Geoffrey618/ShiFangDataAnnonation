import os
import sys

def rename_images():
    # 获取当前目录下的所有文件
    files = os.listdir('.')
    # 过滤出图片文件，可以根据需要增加其他图片格式
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]

    # 对图片文件进行重命名
    for index, image_file in enumerate(image_files, start=1):
        # 获取文件扩展名
        file_extension = os.path.splitext(image_file)[1]
        # 新文件名（此处采用imageN.jpg类型）
        new_name = f"{'image'+str(index)}{file_extension}"
        # 重命名文件
        os.rename(image_file, new_name)

    # 提示用户已全部重命名
    print("已全部重命名")

if __name__ == "__main__":
    rename_images()