# Generated by Django 3.2.7 on 2021-10-21 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('records', '0002_auto_20211016_0700'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportschedule',
            options={'verbose_name': '期号', 'verbose_name_plural': '周报计划表'},
        ),
        migrations.AlterField(
            model_name='report',
            name='author',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='auth.user', verbose_name='报告者'),
            preserve_default=False,
        ),
    ]
