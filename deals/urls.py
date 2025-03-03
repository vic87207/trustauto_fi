from django.urls import path
from .views import (
    DealListView,
    DealCreateView,
    DealUpdateView,
    DealDeleteView,
    ReportView,
)

urlpatterns = [
    path("", DealListView.as_view(), name="deal-list"),
    path("create/", DealCreateView.as_view(), name="deal-create"),
    path("update/<int:pk>/", DealUpdateView.as_view(), name="deal-update"),
    path("delete/<int:pk>/", DealDeleteView.as_view(), name="deal-delete"),
    path("report/", ReportView.as_view(), name="report"),
]
