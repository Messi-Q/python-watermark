# pdf-watermark  [![Build Status](https://travis-ci.com/nuBacuk/pdf-watermark.svg?branch=master)](https://travis-ci.com/nuBacuk/pdf-watermark)
Creates watermark in pdf and makes protection from editing.

## Install 
1. apt-get install pdftk python3 python3-pip
2. pip3 install -r requirement.txt

## Use
python3 ./pdf-watermark.py -w 'File owner Ilya Khramtsov' -i test.pdf

**-i If the file is not specified, will deliver the watermarks to all pda files in the current directory.**
**-i 如果文件没有指定，则会将水印发送到当前目录中的所有pda文件。**

## Settings at the beginning of the file.
- POSITION = 'bottom-middle'  #配置
- pdfmetrics.registerFont(TTFont('FreeSa/Users/white/Downloads/pdf-watermark-master/pdf-watermark.pyns', 'FreeSans.ttf'))  # 字体名称和字体文件名称
- FONT_SIZE = 12  # 字体大小
- FONT_COLOR = '#cccccc'  # 字体的颜色
- VALIDATE = 'trustworthy'
- PREFIX = 'my'
- SECURE_NAME = 'TK_'  # 密码安装后的文件名称
- OWNER_PASS = '333'  # 编辑密码
