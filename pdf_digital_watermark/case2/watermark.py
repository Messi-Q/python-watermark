# -*- coding: utf-8 -*-
"""
Author      : Messi-q
Purpose     : Insert Watermark to a pdf document
Version     : 0.0.1
"""

import os
import datetime
import time
import reportlab
import pyPdf


class watermark:
    """ A watermark class customized with the reportlab module.
     Attributes:
        checkpage_type
        watermark_it
    """
    _papertype = {"A4": [210, 297], "A0": [841, 1189], "A1": [594, 841], "A2": [420, 594], "A3": [297, 420],
                  "A5": [148, 210]}  # mm
    _papertype_conversion_factor = 0.352778

    def __init__(self, fname, pagetype="AA"):
        self.fname = fname
        self.pagetype = pagetype
        self.pagesize = [0, 0]
        self.pagecount = 0
        self.getPageExtend()

    def checkpage_type(self):
        if self.pagetype not in self._papertype.keys():
            raise RuntimeError('Page size must be A4 for this version of image_digital_watermark.')
        else:
            return True

    def getPageExtend(self, page=0):
        self.pagesize = [int(round(float(row) * self._papertype_conversion_factor)) for row in
                         pyPdf.PdfFileReader(file(self.fname, 'rb')).getPage(page).mediaBox[2:4]]
        self.getPageSize()

    def getPageSize(self):
        for row in self._papertype.keys():
            if (self._papertype[row][0] - 2 < self.pagesize[0] < self._papertype[row][0] + 2) and (
                    self._papertype[row][1] - 2 < self.pagesize[1] < self._papertype[row][1] + 2):
                self.pagetype = row
                print(row)
            elif (self._papertype[row][1] - 2 < self.pagesize[0] < self._papertype[row][1] + 2) and (
                    self._papertype[row][0] - 2 < self.pagesize[1] < self._papertype[row][0] + 2):
                self.pagetype = row + "Reversed"
                print(row + "Reversed")
            else:
                self.pagetype = "AA"

    def watermark_it(self, word):
        self.checkpage_type()
        self.watermarktext = word
        return True

    def _test(self):
        for pages in range(5):
            print(pages)
            self.getPageExtend(pages)
            print(pages, " : : ", self.pagetype)
        print("test")
