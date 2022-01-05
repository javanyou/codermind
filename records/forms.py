from datetime import timedelta

import django.utils.timezone
from django import forms
from django.utils import timezone

from .models import Report, ReportLine, ReportSchedule


class ReportForm(forms.ModelForm):
    schedule = forms.ModelChoiceField(
        queryset=ReportSchedule.objects.filter(end_date__gte=(timezone.now() - timedelta(1))),
        # disabled=True,
        widget=forms.Select({"class": "form-control"}),
    )

    class Meta:
        model = Report
        fields = ("schedule",)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ReportForm, self).__init__(*args, **kwargs)

    def clean_schedule(self):
        """对 schedule 进行数据校验"""
        schedule = self.cleaned_data["schedule"]
        if Report.objects.filter(author=self.user, schedule=schedule).exists():
            raise forms.ValidationError("该期周报你已经提交过啦～ 请勿重复提交喔")
        return schedule


class ReportUpdateForm(forms.ModelForm):
    schedule = forms.ModelChoiceField(
        queryset=ReportSchedule.objects.filter(end_date__gte=(timezone.now() - timedelta(1))),
        # disabled=True,
        widget=forms.Select({"class": "form-control"}),
    )

    class Meta:
        model = Report
        fields = ("schedule",)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ReportUpdateForm, self).__init__(*args, **kwargs)

    def clean_schedule(self):
        """对 schedule 进行数据校验"""
        schedule = self.cleaned_data["schedule"]
        found = Report.objects.filter(author=self.user, schedule=schedule).first()
        if found.id != self.instance.id:
            raise forms.ValidationError("该期周报你已经提交过啦～ 请勿重复提交喔")
        return schedule


class ReportLineForm(forms.ModelForm):
    class Meta:
        model = ReportLine
        fields = "__all__"
        widgets = {
            "project": forms.Select({"class": "form-control"}),
            "title": forms.TextInput({"class": "form-control"}),
            "time_cost": forms.NumberInput({"class": "form-control"}),
            "progress": forms.NumberInput({"class": "form-control"}),
        }


ReportLineFormSet = forms.inlineformset_factory(
    Report,
    ReportLine,
    form=ReportLineForm,
    fields=["project", "title", "time_cost", "progress"],
    can_delete=True,
)
