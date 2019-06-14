import sys
import PyPDF2
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def create_watermark(file_name, content):
    c = canvas.Canvas(file_name, pagesize=(30 * cm, 30 * cm))
    # 移动坐标原点(坐标系左下为(0,0))
    c.translate(50, 600)
    # 设置字体
    c.setFont("Helvetica", 5)
    # 指定填充颜色
    c.setFillColorRGB(255, 255, 255)
    # 设置透明度,1为不透明
    c.setFillAlpha(0)
    # 画几个文本,注意坐标系旋转的影响
    c.drawString(2 * cm, 0 * cm, content)
    # 关闭并保存pdf文件
    c.save()
    return file_name


def embed_watermark(pdf_file_in, tmp_file, watermarkInfo, pdf_file_out):
    pdf_file_mark = create_watermark(tmp_file, watermarkInfo)

    # 输入文件
    pdf_input = PyPDF2.PdfFileReader(open(pdf_file_in, 'rb'))
    # 读入水印pdf文件
    pdf_watermark = PyPDF2.PdfFileReader(open(pdf_file_mark, 'rb'))
    # 输出文件
    pdf_output = PyPDF2.PdfFileWriter()

    # 获取输入pdf文件的页数
    pageNum = pdf_input.getNumPages()
    for i in range(pageNum):
        page = pdf_input.getPage(i)
        # 将水印信息嵌入在最后一页上
        if i == pageNum - 1:
            page.mergePage(pdf_watermark.getPage(0))
            page.compressContentStreams()  # 压缩内容
        pdf_output.addPage(page)
    pdf_output.write(open(pdf_file_out, 'wb'))


if __name__ == '__main__':
    pdf_file = sys.argv[1]
    tmp_file = sys.argv[2]
    watermarkInfo = sys.argv[3]
    file_out = sys.argv[4]

    # tmp_file = "tmp.pdf"
    # watermark = "969289210@qq.com-123@gmail.com-sdbasbdaks"

    # pdf_file = "./GCN.pdf"
    # file_out = "./out.pdf"

    embed_watermark(pdf_file, tmp_file, watermarkInfo, file_out)
