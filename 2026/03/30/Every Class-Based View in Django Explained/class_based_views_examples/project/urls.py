from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('', views.ViewExample.as_view(), name='view_example'),
    path('', views.TemplateViewExample.as_view(), name='template_view_example'),
    path('', views.RedirectViewExample.as_view(), name='redirect_view_example'),
    path('', views.ListViewExample.as_view(), name='list_view_example'),
    path('<int:pk>/', views.DetailViewExample.as_view(), name='detail_view_example'),
    path('', views.FormViewExample.as_view(), name='form_view_example'),
    path('', views.CreateViewExample.as_view(), name='create_view_example'),
    path('<int:pk>/', views.UpdateViewExample.as_view(), name='update_view_example'),
    path('<int:pk>/', views.DeleteViewExample.as_view(), name='delete_view_example'),
    path('', views.ArchiveIndexViewExample.as_view(), name='archive_index_view_example'),
    path('<int:year>/', views.YearArchiveViewExample.as_view(), name='year_archive_view_example'),
    path('<int:year>/<str:month>/', views.MonthArchiveViewExample.as_view(), name='month_archive_view_example'),
    path('<int:year>/<int:week>/', views.WeekArchiveViewExample.as_view(), name='week_archive_view_example'),
    path('<int:year>/<str:month>/<int:day>/', views.DayArchiveViewExample.as_view(), name='day_archive_view_example'),
    path('', views.TodayArchiveViewExample.as_view(), name='today_archive_view_example'),
    path('<int:year>/<str:month>/<int:day>/<int:pk>/', views.DateDetailViewExample.as_view(), name='date_detail_view_example'),
]
