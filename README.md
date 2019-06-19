# python-watermark

## 数字水印使用说明
## Requirements
   ```
   Python2.7 or Python3.6以上(测试用的python3.7)
   PIL
   PyPDF2
   reportlab
   ```
使用pip命令安装相关的库文件
   ```
   pip install PIL
   pip install PyPDF2
   pip install reportlab
   ```

## Usage

## 图像数字水印的嵌入和提取：
嵌入水印 python image_watermark_embed.py [文件路径] [水印信息] [输出文件]
提取水印 python image_watermark_extract.py [文件路径]
Sample:
假定文件在当前目录下
嵌入水印 python image_watermark_embed.py input.jpg qian-peng-1@qq.com output.jpg
提取水印 python image_watermark_extract.py output.jpg

## PDF数字水印的嵌入和提取：
嵌入水印 python pdf_watermark_embed.py [文件路径] [中介文件][水印信息] [输出文件]
提取水印 python pdf_watermark_extract.py [文件路径]
Sample:
假定文件在当前目录下
嵌入水印 python pdf_watermark_embed.py input.pdf tmp.pdf qian-peng-1@qq.com out.pdf
提取水印 python pdf_watermark_extract.py out.pdf
注：中介文件是一个临时pdf文档，程序会自动创建，在执行过程中会将水印信息嵌入在临时pdf文档中，通过后面的merge操作，将水印融合到需要嵌入水印的文件中。

## 图像数字水印的嵌入和验证：
A simple implementation of digital watermark based on LSB and Arnold transform
嵌入水印 python image-watermark.py [文件路径] [嵌入ID] [输出文件]
验证水印 python image-watermark-extract.py [文件路径] [验证ID]
Sample:
假定文件在当前目录下
嵌入水印 python image-watermark.py input.jpg username output.jpg
验证水印 python image-watermark_extract.py output.jpg username

