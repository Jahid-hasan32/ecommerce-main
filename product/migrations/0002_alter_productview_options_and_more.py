# Generated by Django 4.2.5 on 2023-10-14 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productview',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='productview',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='productview',
            name='user',
        ),
    ]