# Generated by Django 3.1.3 on 2021-03-31 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='foods', verbose_name='菜品图片'),
        ),
    ]
