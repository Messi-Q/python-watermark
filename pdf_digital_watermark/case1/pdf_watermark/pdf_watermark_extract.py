import PyPDF2


def extract_watermark(file_watermarked):
    # 输入文件
    pdf_input = PyPDF2.PdfFileReader(open(file_watermarked, 'rb'))
    pageNum = pdf_input.getNumPages()
    extractedText = pdf_input.getPage(pageNum - 1).extractText()
    print(extractedText.split()[-1])


if __name__ == '__main__':
    origin_file = "./GCN.pdf"
    file_watermarked = "./out.pdf"
    extract_watermark(file_watermarked)
