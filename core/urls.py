from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'core'

router = routers.SimpleRouter()
router.register('transaction', views.TransactionViewSet, basename="transaction")

urlpatterns = [
    path('', include(router.urls)),
    path('report/montly_summary', views.MonthlySummaryReport.as_view(), name='monthly_summary_report'),
    path('report/category', views.CategoryReport.as_view(), name='category_report'),
]
