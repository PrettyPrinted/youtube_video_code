from django.shortcuts import render

from django.views import View
class ViewExample(View):
    def get(self, request):
        return render(request, 'index.html')


from django.views.generic.base import TemplateView
class TemplateViewExample(TemplateView):
    template_name = "index.html"


from django.views.generic.base import RedirectView
class RedirectViewExample(RedirectView):
    url = "https://prettyprinted.com" # or pattern_name


from django.views.generic.list import ListView
class ListViewExample(ListView):
    model = Event

from django.views.generic.detail import DetailView
class DetailViewExample(DetailView):
    model = Event


from django.views.generic.edit import FormView
class FormViewExample(FormView):
    form_class = EventForm
    template_name = "form.html"
    success_url = "/"

from django.views.generic.edit import CreateView
class CreateViewExample(CreateView):
    model = Event
    fields = ["name", "event_date"]


from django.views.generic.edit import UpdateView
class UpdateViewExample(UpdateView):
    model = Event
    fields = ["name", "event_date"]


from django.views.generic.edit import DeleteView
class DeleteViewExample(DeleteView):
    model = Event
    success_url = "/"


from django.views.generic.dates import ArchiveIndexView
class ArchiveIndexViewExample(ArchiveIndexView):
    model = Event
    date_field = "event_date"


from django.views.generic.dates import YearArchiveView
class YearArchiveViewExample(YearArchiveView):
    model = Event
    date_field = "event_date"

from django.views.generic.dates import MonthArchiveView
class MonthArchiveViewExample(MonthArchiveView):
    model = Event
    date_field = "event_date"


from django.views.generic.dates import WeekArchiveView
class WeekArchiveViewExample(WeekArchiveView):
    model = Event
    date_field = "event_date"


from django.views.generic.dates import DayArchiveView
class DayArchiveViewExample(DayArchiveView):
    model = Event
    date_field = "event_date"

from django.views.generic.dates import TodayArchiveView
class TodayArchiveViewExample(TodayArchiveView):
    model = Event
    date_field = "event_date"


from django.views.generic.dates import DateDetailView
class DateDetailViewExample(DateDetailView):
    model = Event
    date_field = "event_date"
