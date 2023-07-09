import base64
from tkinter import Tk, filedialog


#在同一文件夹下把图片转为base64,存为txt
def encode_img(input_paths):
    for path in input_paths:

        file_type = path.split('.')[-1]
        output_path = f'{path}-base64.txt'

        with open(path, 'rb') as f:
            img_data = f.read()
            base64_data = base64.b64encode(img_data)
            base64_str = str(base64_data, 'utf-8')

        with open(output_path, 'w') as f:
            if file_type == 'svg':
                file_type = 'svg+xml'
            f.write(f'data:image/{file_type};base64,{base64_str}')


root = Tk()
root.withdraw()
input_paths = filedialog.askopenfilenames()
encode_img(input_paths)
