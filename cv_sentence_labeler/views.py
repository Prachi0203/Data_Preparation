from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import redirect
from django.template import RequestContext
from datetime import date
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
# from .functions.functions import handle_uploaded_file
from django.shortcuts import render
import openpyxl


def index(request):
    return render(request, 'index.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return render(request, 'main.html')
            else:
                return HttpResponse('You are not a admin!')
        else:
            alert = True
            return render(request, 'main.html', {'alert': alert})
    return render(request, 'admin_login.html')


def as_user(request):
    return render(request, 'as_user.html')


def add_concept(request):
    if request.method == 'POST':
        # id = request.POST['id']
        concept = request.POST['concept']
        concept_short = request.POST['concept_short']
        save_data = CvLabelMapper()
        save_data.concept = concept
        save_data.concept_short = concept_short
        save_data.save()
        # another way to save data to the database.
        # save_data = CvLabelMapper.objects.create(concept = concept,acronym = acronym)
        # save_data.save()
        alert = True
        return render(request, 'add_concept.html', {'alert': alert})
    return render(request, 'add_concept.html')


def view_concepts(request):
    data = CvLabelMapper.objects.all()
    concept = CvLabelMapper.objects.all().values_list('concept', flat=True)
    concept_short = CvLabelMapper.objects.all().values_list('concept_short', flat=True)
    """dict = {}
    for i in data:
        print(i.concepts)
        print(i.acronym)
        if i.concepts not in dict.items():
            dict[i.concepts] = i.acronym"""
    context = {
        'data': CvLabelMapper.objects.all()
    }
    return render(request, 'view_concepts.html', context)


def edit_concept(request, myid):
    old_concept = CvLabelMapper.objects.get(id=myid)
    if request.method == "POST":
        new_concept = request.POST['concept']
        new_short_concept = request.POST['concept_short']
        concept_list = CvLabelMapper.objects.all().filter(id=myid)
        for i in concept_list:
            i.concept = new_concept
            i.concept_short = new_short_concept

            i.save()
    else:
        return render(request, "edit_concept.html", {'old_concept': old_concept})

    return redirect('/view_concepts')


def delete_concept(request, myid):
    CvLabelMapper.objects.get(id=myid).delete()
    return redirect("/view_concepts")


def add_label(request):
    sentence_labeler = SentenceLabeler.objects.all()
    label_mapper = CvLabelMapper.objects.all()

    save_sentence_label = SentenceLabeler()
    if request.method == 'POST':
        myid = request.POST['id']
        label = request.POST['label']
        label_value = request.POST['label_field']
        level_value = request.POST['level_field']
        SentenceLabeler.objects.filter(pk=myid).update(
            label=label, label_value=label_value, level_value=level_value)

        alert = True
        return render(request, 'add_label.html', {'alert': alert})
    return render(request, 'add_label.html', {'sentence_labeler': sentence_labeler, 'label_mapper': label_mapper})


def view_sentences(request):
    context = {
        'sentence_labeler': SentenceLabeler.objects.order_by('original_id')
    }
    return render(request, 'view_sentences.html', context)


def add_sentence(request):
    if request.method == 'POST':
        # id = request.POST['id']
        label = request.POST['label']
        sentence = request.POST['text_field']
        label_obj = CvLabelMapper.objects.get(concept=label)
        label_value = label_obj.concept_short
        level_value = request.POST['level_field']
        obj = SentenceLabeler.objects.create(sentence=sentence, label=label,
                                             label_value=label_value, level_value=level_value)
        obj.save()
        obj.original_id = obj.id
        obj.save()
        alert = True
        return render(request, 'add_sentence.html', {'alert': alert})
    context = {
        'label_mapper': CvLabelMapper.objects.all()
    }

    return render(request, 'add_sentence.html', context)


def delete_sentence(request, myid):
    SentenceLabeler.objects.filter(id=myid).delete()
    return redirect("/view_sentences")


def edit_sentence(request, myid):
    sentence_obj = SentenceLabeler.objects.get(id=myid)
    label_mapper = CvLabelMapper.objects.all()

    if request.method == 'POST':
        label = request.POST['label_field']
        label_obj = CvLabelMapper.objects.get(concept=label)
        label_value = label_obj.concept_short
        level_value = request.POST['level_field']
        SentenceLabeler.objects.filter(pk=myid).update(
            label=label, label_value=label_value, level_value=level_value)
        alert = True
        return render(request, 'edit_sentence.html', {'alert': alert})
    return render(request, 'edit_sentence.html', {'sentence_obj': sentence_obj, 'label_mapper': label_mapper})


def duplicate_sentence(request, myid):
    sentence_obj = SentenceLabeler.objects.get(pk=myid)

    SentenceLabeler.objects.create(sentence=sentence_obj.sentence, label=None,
                                   label_value=None, level_value=None, original_id=sentence_obj.original_id)
    return redirect('/view_sentences')


def upload_excel(request):
    if "GET" == request.method:
        return render(request, 'upload.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
        for i in range(1, len(excel_data)):
            col = excel_data[i]
            SentenceLabeler.objects.create(sentence=col[0], label=None,
                                           label_value=None, level_value=0)

    return redirect('/view_sentences')
