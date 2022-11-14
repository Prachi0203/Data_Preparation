from django.contrib import admin
from .models import CvLabelMapper,SentenceLabeler,SentenceLabelerTest

# Register your models here.
admin.site.register(CvLabelMapper)
admin.site.register(SentenceLabeler)
admin.site.register(SentenceLabelerTest)