# Generated by Django 3.2.7 on 2021-10-16 07:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='parent',
        ),
        migrations.AddField(
            model_name='project',
            name='parent_project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subprojects', to='records.project', verbose_name='父项目'),
        ),
        migrations.CreateModel(
            name='ReportLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=256, verbose_name='标题')),
                ('time_cost', models.FloatField(default=0.0, verbose_name='耗时(小时)')),
                ('progress', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='进度(0～100)')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='records.project', verbose_name='项目')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='records.report', verbose_name='所属周报')),
            ],
            options={
                'verbose_name': '周报条目',
                'verbose_name_plural': '周报详情',
            },
        ),
    ]