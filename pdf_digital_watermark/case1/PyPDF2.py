from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.units import cm

# 简单的读写
readFile = 'read.pdf'
writeFile = 'write.pdf'
# 获取一个 PdfFileReader 对象
pdfReader = PdfFileReader(open(readFile, 'rb'))
# 获取 PDF 的页数
pageCount = pdfReader.getNumPages()
print(pageCount)
# 返回一个 PageObject
page = pdfReader.getPage(i)
# 获取一个 PdfFileWriter 对象
pdfWriter = PdfFileWriter()
# 将一个 PageObject 加入到 PdfFileWriter 中
pdfWriter.addPage(page)
# 输出到文件中
pdfWriter.write(open(writeFile, 'wb'))


# 合并分割
def split_pdf(infn, outfn):
    pdf_output = PdfFileWriter()
    pdf_input = PdfFileReader(open(infn, 'rb'))
    # 获取 pdf 共用多少页
    page_count = pdf_input.getNumPages()
    print(page_count)
    # 将 pdf 第五页之后的页面，输出到一个新的文件
    for i in range(5, page_count):
        pdf_output.addPage(pdf_input.getPage(i))
    pdf_output.write(open(outfn, 'wb'))


def merge_pdf(infnList, outfn):
    pdf_output = PdfFileWriter()
    for infn in infnList:
        pdf_input = PdfFileReader(open(infn, 'rb'))
        # 获取 pdf 共用多少页
        page_count = pdf_input.getNumPages()
        print(page_count)
        for i in range(page_count):
            pdf_output.addPage(pdf_input.getPage(i))
    pdf_output.write(open(outfn, 'wb'))


def create_watermark(content):
    # 默认大小为21cm*29.7cm
    file_name = "mark.pdf"
    c = canvas.Canvas(file_name, pagesize=(30 * cm, 30 * cm))
    # 移动坐标原点(坐标系左下为(0,0))
    c.translate(10 * cm, 5 * cm)
    # 设置字体
    c.setFont("Helvetica", 80)
    # 指定描边的颜色
    c.setStrokeColorRGB(0, 1, 0)
    # 指定填充颜色
    c.setFillColorRGB(0, 1, 0)
    # 画一个矩形
    # c.rect(cm, cm, 7*cm, 17*cm, fill=1)
    # 旋转45度,坐标系被旋转
    c.rotate(45)
    # 指定填充颜色
    c.setFillColorRGB(0.6, 0, 0)
    # 设置透明度,1为不透明
    c.setFillAlpha(0.3)
    # 画几个文本,注意坐标系旋转的影响
    c.drawString(3 * cm, 0 * cm, content)
    c.setFillAlpha(0.6)
    # 关闭并保存pdf文件
    c.save()
    return file_name


def add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out):
    pdf_output = PdfFileWriter()
    input_stream = open(pdf_file_in, 'rb')
    pdf_input = PdfFileReader(input_stream)

    # PDF文件被加密了
    if pdf_input.getIsEncrypted():
        print('该PDF文件被加密了.')
        # 尝试用空密码解密
        try:
            pdf_input.decrypt('')
        except Exception as e:
            print('尝试用空密码解密失败.')
            return False
        else:
            print('用空密码解密成功.')
    # 获取PDF文件的页数
    pageNum = pdf_input.getNumPages()
    # 读入水印pdf文件
    pdf_watermark = PdfFileReader(open(pdf_file_mark, 'rb'))
    # 给每一页打水印
    for i in range(pageNum):
        page = pdf_input.getPage(i)
        page.mergePage(pdf_watermark.getPage(0))
        page.compressContentStreams()  # 压缩内容
        pdf_output.addPage(page)
    pdf_output.write(open(pdf_file_out, 'wb'))


if __name__ == '__main__':
    infn = 'infn.pdf'
    outfn = 'outfn.pdf'
    split_pdf(infn, outfn)
