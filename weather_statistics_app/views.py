from django.shortcuts import render
from .forms import UserForm

from .functions import make_statistics, make_datetime


def index(request):
    if request.method == "POST":
        city = request.POST.get("option")
        period_start = request.POST.get("period_start")
        period_end = request.POST.get("period_end")
        period_start = make_datetime(period_start)
        period_end = make_datetime(period_end)
        statistics_info = make_statistics(city, period_start, period_end)
        return render(request, 'weather_statistics_app/statistics.html', 
                      statistics_info)
    else:
        userform = UserForm()
        return render(request, "index.html", {"form": userform})
