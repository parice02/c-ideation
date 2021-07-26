# Generated by Django 3.2.1 on 2021-07-26 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_contact_card_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='field',
            field=models.CharField(max_length=30, verbose_name='Département'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='job',
            field=models.CharField(max_length=30, verbose_name='UFR'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='work_place',
            field=models.CharField(max_length=30, verbose_name='Établissement'),
        ),
    ]