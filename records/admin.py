from django.contrib import admin

from .models import Project, Report, ReportLine, ReportSchedule

admin.site.register(Project)
# 报告计划时间表
admin.site.register(ReportSchedule)


class ReportLineInline(admin.TabularInline):
    model = ReportLine
    extra = 1


class ReportAdmin(admin.ModelAdmin):
    """周报报告管理类"""

    inlines = [ReportLineInline]


# 周报对象
admin.site.register(Report, ReportAdmin)
