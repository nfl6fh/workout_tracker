from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
import datetime
from .models import *

# Create your views here.

def home(request):
    return render(request, 'tracker/home.html')
    
def workout_calendar(request):
    # get current month
    now = datetime.datetime.now()
    current_month = now.strftime("%B")
    current_year = now.strftime("%Y")
    current_month_num = now.month
    print(current_month_num)

    # create a list of weeks in the current month where each week is a list of days, start each week on Sunday. Fill in the days of the previous month and next month as needed
    weeks = []
    week = []
    # get the first day of the month
    first_day = datetime.datetime(int(current_year), now.month, 1)
    # print(first_day)
    # get the weekday of the first day of the month
    weekday = first_day.weekday()
    # get the number of days in the month
    num_days = (datetime.datetime(int(current_year), (now.month+1), 1) - datetime.timedelta(days=1)).day
    # get the number of days in the previous month
    prev_month = now.month - 1
    prev_year = now.year
    if prev_month == 0:
        prev_month = 12
        prev_year = now.year - 1
    num_days_prev_month = (first_day - datetime.timedelta(days=1)).day
    print(num_days_prev_month)
    # get the number of days in the next month
    next_month = now.month + 1
    next_year = now.year
    if next_month == 13:
        next_month = 1
        next_year = now.year + 1
    # fill in the days of the previous month
    for i in range(weekday):
        # week.append(num_days_prev_month - weekday + i + 1)
        week.append(0)
    # fill in the days of the current month
    for i in range(1, num_days + 1):
        week.append(i)
        if len(week) == 7:
            weeks.append(week)
            week = []
    # fill in the days of the next month
    for i in range(1, 8-len(week)):
        week.append(0)
    weeks.append(week)
    # add filtering by user later
    workouts = list(Workout.objects.filter(date__year=current_year, date__month=now.month).order_by('date'))
    print(workouts)
    return render(request, 'tracker/workout_calendar.html', {'calendar': weeks, 'current_month': current_month, 'current_year': current_year, 'workouts': workouts, 'current_month_num': current_month_num})
