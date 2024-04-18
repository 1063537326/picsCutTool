# 导入所需的模块
from tkinter import Tk, filedialog, Button, Label, messagebox
from PIL import Image
import os

# 定义切割图片的函数
def cut_image_into_nine_parts(image_path, save_path):
    try:
        # 使用PIL库打开图片
        with Image.open(image_path) as img:
            # 获取图片的宽度和高度
            width, height = img.size

            # 计算每个格子的宽度，假设图片宽度可以被3整除
            square_size = width // 3

            # 循环遍历九宫格的每一格
            for i in range(3):  # 行
                for j in range(3):  # 列
                    # 计算每个格子的坐标
                    x_start = j * square_size
                    y_start = i * square_size
                    x_end = x_start + square_size
                    y_end = y_start + square_size

                    # 裁剪图片
                    cropped_img = img.crop((x_start, y_start, x_end, y_end))

                    # 构造新的文件名，格式为：数字+原始图片的后缀名
                    file_name = f"{i*3+j+1:02d}{os.path.splitext(image_path)[1]}"

                    # 保存裁剪后的图片到指定路径
                    cropped_img.save(os.path.join(save_path, file_name))
            print("图像已被剪切并保存。")

    # 异常处理，如果发生错误，显示错误信息
    except IOError as e:
        messagebox.showerror("Error", f"无法打开或保存图像: {e}")

# 定义选择图片并切割的函数
def select_image_and_cut():
    # 使用文件对话框让用户选择图片文件
    image_path = filedialog.askopenfilename(
        title='Select an image file',
        filetypes=[('Image files', '*.jpg;*.png')]  # 限制选择的文件类型为图片
    )

    # 如果用户选择了文件
    if image_path:
        # 获取选择图片的目录，用于保存切割后的图片
        save_path = os.path.dirname(image_path)

        # 调用切割图片的函数
        cut_image_into_nine_parts(image_path, save_path)

        # 更新应用窗口的标题，显示当前处理的图片名称
        app.title(f"九宫格剪切 - {os.path.basename(image_path)}")

        # 调整窗口大小以适应新标题
        app.geometry("300x100")

# 定义继续切割或退出的函数
def continue_or_exit():
    # 弹出一个对话框询问用户是否继续或退出
    response = messagebox.askyesno("继续或退出", "是否要剪切另一个图像？")

    # 如果用户选择继续
    if response:
        # 更新窗口标题，提示用户选择图片
        app.title("九宫格剪切-选择图像")

        # 调整窗口大小回原始大小
        app.geometry("300x200")

        # 调用选择图片并切割的函数
        select_image_and_cut()
    else:
        # 用户选择退出，关闭应用窗口
        app.destroy()

# 创建Tkinter应用窗口
app = Tk()

# 设置窗口标题和大小
app.title("九宫格剪切-选择图像")
app.geometry("300x200")


# 创建一个标签，提示用户选择图片
Label(app, text="请选择要剪切成九宫格的图像文件。", wraplength=280).pack()

# 创建一个按钮，用户点击后会调用选择图片并切割的函数
Button(app, text="选择图像", command=select_image_and_cut).pack()

# 绑定关闭窗口事件到continue_or_exit函数，当用户尝试关闭窗口时调用
app.protocol("WM_DELETE_WINDOW", continue_or_exit)

# 进入事件循环，显示窗口，等待用户操作
app.mainloop()