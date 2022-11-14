import xlrd
#from cv_sentence_labeler.models import *
def handle_uploaded_file(f):
    with open('cv_sentence_labeler/functions/uploads'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def open_excel_file(f):
    book = xlrd.open_workbook(f)

f = 'ml_preparation/cv_sentence_labeler/static/cv_sentences_150.xlsx'
open_excel_file(f)