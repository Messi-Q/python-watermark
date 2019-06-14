import PyPDF2
import sys


def extract_watermark(file_watermarked):
    # 输入文件
    pdf_input = PyPDF2.PdfFileReader(open(file_watermarked, 'rb'))
    pageNum = pdf_input.getNumPages()
    extractedText = pdf_input.getPage(pageNum - 1).extractText()
    watermarkInfo = extractedText.split()[-1]
    result = watermarkInfo.split("-", 2)
    print("资源所有者email：", result[0], "当前使用者email：", result[1], "资源ID：", result[2])


if __name__ == '__main__':
    # file_watermarked = "./out.pdf"
    file_watermarked = sys.argv[1]
    extract_watermark(file_watermarked)
