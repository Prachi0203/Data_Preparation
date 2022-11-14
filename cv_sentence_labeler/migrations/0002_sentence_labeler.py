# Generated by Django 4.0.5 on 2022-06-18 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv_sentence_labeler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sentence_Labeler',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sentence', models.CharField(blank=True, max_length=255)),
                ('label', models.CharField(blank=True, max_length=100, null=True)),
                ('label_value', models.IntegerField(blank=True, null=True)),
                ('level_value', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sentence_labeler',
                'managed': False,
            },
        ),
    ]