# Generated by Django 2.2.16 on 2022-03-22 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20220130_1106'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Посты', 'verbose_name_plural': 'Посты'},
        ),
    ]
