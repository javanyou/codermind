from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class Project(models.Model):
    """
    项目/TMP
    """

    name = models.CharField(max_length=16, verbose_name="名称")
    code = models.CharField(max_length=10, verbose_name="代码", null=True, blank=True)
    description = models.CharField(
        max_length=512, verbose_name="描述", null=True, blank=True
    )
    parent_project = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subprojects",
        verbose_name="父项目",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目一览表"


class ReportSchedule(models.Model):
    """
    周报时间计划表
    """

    start_date = models.DateField(verbose_name="开始日期")
    end_date = models.DateField(verbose_name="结束日期")
    public_holidays = models.FloatField(default=2, verbose_name="公休天数")

    @property
    def sid(self):
        """获取字符串id -- 格式 YyyyMmDd-YyyyMmDd 例子：202004020-20200424"""
        return f'{self.start_date.strftime("%Y-%m-%d")} ~ {self.end_date.strftime("%Y-%m-%d")}'

    def labour_time(self):
        """获取周报实际工作时长"""
        # +1 是用来修正实际计算时间[start ,end_date]
        return ((self.end_date - self.start_date).days - self.public_holidays + 1) * 7.5

    labour_time.short_description = "出勤时长(小时)"

    def get_absolute_url(self):
        return reverse("report-detail", args=[str(self.id)])

    def __str__(self):
        return self.sid

    class Meta:
        verbose_name = "期号"
        verbose_name_plural = "周报计划表"


class Report(models.Model):
    """
    周报，用户可以创建的周报
    """

    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="报告者")
    schedule = models.ForeignKey(
        ReportSchedule, on_delete=models.PROTECT, verbose_name="周报号"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"{self.schedule.sid} by {self.author}"

    def get_absolute_url(self):
        return reverse("report-detail", kwargs={"pk": self.id})

    class Meta:
        verbose_name = "周报"
        verbose_name_plural = "周报列表"


class ReportLine(models.Model):
    """
    周报记录条目
    """

    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name="lines", verbose_name="所属周报"
    )
    project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name="项目")
    title = models.CharField(max_length=256, default="", verbose_name="标题")
    time_cost = models.FloatField(default=0.0, verbose_name="耗时(小时)")
    progress = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        verbose_name="进度(0～100)",
    )

    def __str__(self):
        return f"{self.report.id}: line-{self.id}"

    class Meta:
        verbose_name = "周报条目"
        verbose_name_plural = "周报详情"
