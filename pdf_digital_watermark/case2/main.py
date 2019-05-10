import os
import watermark

# pdf_one = watermark.watermark("/home/knn/Desktop/pdf_digital_watermark1/sample/trial.portre.0.1.pdf")
pdf_two = watermark.watermark("/home/knn/Desktop/pdf_digital_watermark1/sample/trial.landscape.0.1.pdf", "A4")

pdf_two._test()
