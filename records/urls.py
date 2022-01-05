from django.urls import path

from . import views

urlpatterns = [
    # ex: /records/reports/
    path("", views.IndexView.as_view(), name="index"),
    path("reports/create/", views.ReportCreateView.as_view(), name="report-create"),
    # /records/reports/
    path("reports/", views.ReportListView.as_view(), name="report-list"),
    # /records/reports/1/
    path(
        "reports/<int:pk>/",
        views.ReportDetailView.as_view(),
        name="report-detail",
    ),
    # /recors/reports/my/
    path("reports/my/", views.ReportsByUserListView.as_view(), name="my-reports"),
    # /records/reports/1/edit/
    path(
        "reports/<int:pk>/edit/", views.ReportUpdateView.as_view(), name="report-update"
    ),
    path(
        "users/<int:user_id>/reports/",
        views.ReportsByUserListView.as_view(),
        name="user-reports",
    ),
    path(
        "reports/<int:pk>/delete/",
        views.ReportDeleteView.as_view(),
        name="report-delete",
    ),
    # 周报计划相关
    path(
        "schedules/",
        view=views.ReportScheduleListView.as_view(),
        name="schedule-list",
    ),
    path(
        "schedules/<int:pk>/",
        views.ReportScheduleDetailView.as_view(),
        name="schedule-detail",
    ),
    path("reports/projects/", views.ProjectListView.as_view(), name="project-list"),
    path(
        "datagram/reportbyuser/",
        views.ReportByUser.as_view(),
        name="data-report-by-user",
    ),
    path(
        "datagram/reportbyproject",
        views.ReportByProjectView.as_view(),
        name="data-report-by-project",
    ),
]
