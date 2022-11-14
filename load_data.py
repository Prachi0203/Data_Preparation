import xlrd


def open_excel_file(f):
    book = xlrd.open_workbook(f)

f = 'ml_preparation/cv_sentence_labeler/static/cv_sentences_150.xlsx'
open_excel_file(f)