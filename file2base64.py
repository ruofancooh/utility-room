import base64
from tkinter import Tk, filedialog


#在同一文件夹下把文件转为base64，存为txt。可选是否加上"data:image/png;base64,"
def file2base64(file_paths, data_uri=False):
    #依次处理同一目录下的多个文件
    for file_path in file_paths:
       
        #输出的路径
        output_path = f'{file_path}-base64.txt'

        #读取文件，生成base64字符串
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
            base64_str = base64.b64encode(file_bytes).decode('utf-8')

        #把base64字符串写入txt
        with open(output_path, 'w') as f:
            if data_uri is False:
                f.write(base64_str)
            else:
                #获取文件扩展名
                filename_extension = file_path.split('.')[-1]

                #判断文件类型
                if filename_extension in ('png', 'jpg', 'jpeg', 'svg', 'ico', 'webp',
                                          'gif', 'tiff', 'bmp'):
                    file_type = 'image'
                else:
                    pass
                if filename_extension == 'svg':
                    filename_extension = 'svg+xml'

                f.write(
                    f'data:{file_type}/{filename_extension};base64,{base64_str}'
                )


root = Tk()
root.withdraw()
file_paths = filedialog.askopenfilenames()
file2base64(file_paths)
