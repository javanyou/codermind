from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
import datetime

from records.forms import ReportForm, ReportLineFormSet, ReportUpdateForm
from records.models import Project, Report, ReportSchedule, ReportLine


class IndexView(generic.ListView):
    template_name = "records/index.html"
    context_object_name = "latest_report_list"

    def get_queryset(self):
        return Report.objects.order_by("-created_at")[:5]


class ReportListView(generic.ListView):
    model = Report
    paginate_by = 10
    context_object_name = "report_list"

    def get_queryset(self):
        return Report.objects.order_by("-created_at")


class ReportDetailView(generic.DetailView):
    model = Report

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = context["report"]
        context["report_aggregate"] = (
            report.lines.values("project_id")
            .annotate(total_cost=Sum("time_cost"))
            .values("project__name", "total_cost")
        )
        return context


class ReportCreateView(LoginRequiredMixin, generic.CreateView):
    model = Report
    form_class = ReportForm
    template_name_suffix = "_update_form"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "新的周报"
        if self.request.POST:
            context["line_formset"] = ReportLineFormSet(self.request.POST)
        else:
            context["line_formset"] = ReportLineFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context["line_formset"]
        if formset.is_valid():
            schedule = form.cleaned_data["schedule"]
            total_time_cost = sum(item.instance.time_cost for item in formset)
            if total_time_cost != schedule.labour_time():
                messages.error(
                    self.request, f"总出勤时间不正确，参考值: {schedule.labour_time()}小时"
                )
                return super().form_invalid(form)
            else:
                # Set author to current login user.
                form.instance.author = self.request.user
                response = super().form_valid(form)
                formset.instance = self.object
                formset.save()
                return response
        else:
            return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ReportUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Report
    # change template file name to report_update_form.html
    template_name_suffix = "_update_form"
    form_class = ReportUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "修改周报"
        if self.request.POST:
            context["line_formset"] = ReportLineFormSet(
                data=self.request.POST, instance=self.object
            )
            context["line_formset"].full_clean()
        else:
            context["line_formset"] = ReportLineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context["line_formset"]
        if formset.is_valid():
            schedule = form.cleaned_data["schedule"]
            total_time_cost = sum(item.instance.time_cost for item in formset)
            if total_time_cost != schedule.labour_time():
                messages.error(
                    self.request, f"总出勤时间不正确，参考值: {schedule.labour_time()}小时"
                )
                return super().form_invalid(form)
            else:
                response = super().form_valid(form)
                formset.instance = self.object
                formset.save()
                return response
        else:
            return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ReportDeleteView(generic.DeleteView):
    model = Report
    success_url = reverse_lazy("report-list")


class ReportsByUserListView(LoginRequiredMixin, generic.ListView):
    """展示当前用户已提交周报"""

    model = Report
    template_name = "records/report_list_by_user.html"
    paginate_by = 10

    def get_queryset(self):
        user_id = self.kwargs.pop("user_id", None)
        if user_id is not None:
            try:
                author = User.objects.get(id=user_id)
            except User.DoesNotExist:
                author = self.request.user
        else:
            author = self.request.user
        self.kwargs["author"] = author
        return Report.objects.filter(author=author).order_by("created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.kwargs["author"]
        return context


class ReportScheduleListView(generic.ListView):
    model = ReportSchedule
    context_object_name = "schedule_list"
    template_name = "records/report_schedule_list.html"
    paginate_by = 10

    def get_queryset(self):
        return ReportSchedule.objects.order_by("-start_date")


class ReprotScheduleDetailView(generic.DetailView):
    model = ReportSchedule
    template_name = "records/schedule_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report_schedule = context["reportschedule"]
        collection_by_project = (
            ReportLine.objects.filter(
                report_id__in=report_schedule.report_set.values("id")
            )
            .values("report__author_id", "time_cost", "project_id", "project__name")
            .values("project_id")
            .annotate(project_cost=Sum("time_cost"))
            .values("project__name", "project_cost", "report__author_id")
        )
        reporter_list = list(
            User.objects.filter(id__in=report_schedule.report_set.values("author_id"))
        )
        context["total_by_project"] = (
            ReportLine.objects.filter(
                report_id__in=report_schedule.report_set.values("id")
            )
            .values("project_id")
            .annotate(project_cost=Sum("time_cost"))
            .values("project__name", "project_cost")
        )
        # 获取项目数组
        x_categories = [item["project__name"] for item in context["total_by_project"]]
        context["x_categories"] = x_categories

        series = {}
        for reporter in reporter_list:
            series[reporter.get_full_name()] = [0] * len(x_categories)
        for item in collection_by_project:
            found = list(
                filter(
                    lambda r: True if r.id == item["report__author_id"] else False,
                    reporter_list,
                )
            )
            if len(found) != 0:
                reporter = found[0]
                series[reporter.get_full_name()][
                    x_categories.index(item["project__name"])
                ] = item["project_cost"]
        context["series_by_project"] = series
        return context


class ProjectListView(generic.ListView):
    model = Project


class ReportByUser(generic.TemplateView):
    """基于人的数据报表"""

    template_name = "records/datagram/report_by_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        default_from_date = (
            datetime.datetime.now() + datetime.timedelta(days=-6)
        ).strftime("%Y-%m-%d")
        default_to_date = datetime.datetime.now().strftime("%Y-%m-%d")
        from_date = self.request.GET.get("from_date", default_from_date)
        to_date = self.request.GET.get("to_date", default_to_date)
        schedules = ReportSchedule.objects.filter(
            (Q(start_date__gte=from_date) & Q(end_date__lte=to_date))
            | (Q(start_date__lte=from_date) & Q(end_date__gte=from_date))
        ).values("id")
        report_list = Report.objects.filter(schedule_id__in=schedules).values("id")
        reporter_list = list(
            User.objects.filter(
                id__in=Report.objects.filter(schedule_id__in=schedules)
                .values("author_id")
                .annotate(report_count=Count("author_id"))
                .values("author_id")
            )
        )
        # 获取成员数据
        x_categories = [reporter.get_full_name() for reporter in reporter_list]

        # 获取汇报的项目列表
        series_by_user = {}
        for project in (
            ReportLine.objects.filter(report_id__in=report_list)
            .values("project_id")
            .annotate(project_cost=Sum("time_cost"))
            .values("project__name", "project_cost")
        ):
            series_by_user[project["project__name"]] = [0] * len(x_categories)

        reportline_list = (
            ReportLine.objects.filter(report_id__in=report_list)
            .values("project_id")
            .annotate(project_cost=Sum("time_cost"))
            .values("report__author_id", "project_cost", "project__name")
        )

        for line in reportline_list:
            found_index = next(
                (
                    index
                    for index, value in enumerate(reporter_list)
                    if value.id == line["report__author_id"]
                ),
                None,
            )
            if found_index is not None:
                series_by_user[line["project__name"]][found_index] = line[
                    "project_cost"
                ]

        context["x_categories"] = x_categories
        context["from_date"] = from_date
        context["to_date"] = to_date
        context["series_by_user"] = series_by_user
        return context


class ReportByProjectView(generic.TemplateView):
    template_name = "records/datagram/report_by_project.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        default_from_date = (
            datetime.datetime.now() + datetime.timedelta(days=-6)
        ).strftime("%Y-%m-%d")
        default_to_date = datetime.datetime.now().strftime("%Y-%m-%d")
        from_date = self.request.GET.get("from_date", default_from_date)
        to_date = self.request.GET.get("to_date", default_to_date)
        schedules = ReportSchedule.objects.filter(
            (Q(start_date__gte=from_date) & Q(end_date__lte=to_date))
            | (Q(start_date__lte=from_date) & Q(end_date__gte=from_date))
        ).values("id")
        report_list = Report.objects.filter(schedule_id__in=schedules).values("id")
        project_list = (
            ReportLine.objects.filter(report_id__in=report_list)
            .values("project_id")
            .annotate(project_cost=Sum("time_cost"))
            .values("project_cost", "project__name")
        )

        x_categories = []
        series = {}
        for project in project_list:
            series[project["project__name"]] = project["project_cost"]
            x_categories.append(project["project__name"])
        context["x_categories"] = x_categories
        context["from_date"] = from_date
        context["to_date"] = to_date
        context["series_by_project"] = series
        return context
