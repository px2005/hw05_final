# Generated by Django 2.2.16 on 2022-03-23 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(help_text='Напишите текст комментария', verbose_name='Комментарий.'),
        ),
    ]
