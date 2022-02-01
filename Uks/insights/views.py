from ast import operator
from time import strptime
from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from repository.models import Repository
from pullrequest.models import Pullrequest, OPENED, CLOSED, MERGED
from issue.models import Issue, ISSUE_STATE
from commit.models import Commit
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta



def pulse(request, id, days):
    repository = get_object_or_404(Repository, id=id)

    open_pr = Pullrequest.objects.all().filter(prRepository = repository, status=OPENED)
    closed_pr = Pullrequest.objects.all().filter(prRepository = repository, status=CLOSED)
    merge_pr = Pullrequest.objects.all().filter(prRepository = repository, status=MERGED)

    open_is = Issue.objects.all().filter(repository = repository, state = ISSUE_STATE[0][0])
    closed_is = Issue.objects.all().filter(repository = repository, state = ISSUE_STATE[1][0])


    context = {
        'repository': repository,
        'days': days,
        'open_pr': open_pr.count,
        'closed_pr': closed_pr.count,
        'merge_pr': merge_pr.count,
        'open_is': open_is.count,
        'closed_is': closed_is.count,
    }

    return render(request, "insights/base_insights.html", context)


def contributors(request, id, days):
    repository = get_object_or_404(Repository, id=id)

    commits = []

    
    now = datetime.now()

    if days == 3:

        today = now.strftime("%Y/%m/%d")
        today_date = datetime.strptime(today, "%Y/%m/%d")

        print(today)
        print("today: ", (today_date + timedelta(days=1)))

        three_days = today_date - timedelta(days=2)
        two_days = today_date - timedelta(days=1)

        commits1 = list(Commit.objects.all().filter(repository = repository, date_time__range = [today_date, (today_date + timedelta(days=1))]))
        commits2 = list(Commit.objects.all().filter(repository = repository, date_time__range = [two_days, today_date]))
        commits3 = list(Commit.objects.all().filter(repository = repository, date_time__range = [three_days, two_days]))



        labels = []
        data = []

        data.append(len(commits1))
        data.append(len(commits2))
        data.append(len(commits3))
        date_now = now
        day = 0

        for x in range(0,3):
            date = (date_now - timedelta(x)).strftime("%Y/%m/%d")
            labels.append(date)
            print(date)

        print("Data: ", data)

        context = {
        'repository': repository,
        'commits': commits,
        'days': days,
        'labels': labels,
        'data': data,
        }

        return render(request, "insights/contributors.html", context)

    elif days == 7:
        now = datetime.now()

        today = now.strftime("%Y/%m/%d")
        today_date = datetime.strptime(today, "%Y/%m/%d")


        labels = []
        data = []

        for x in range(0, 7):
            commits = list(Commit.objects.all().filter(repository = repository, date_time__range = [today_date, (today_date + timedelta(days=1))]))
            data.append(len(commits))
            date = (now - timedelta(x)).strftime("%Y/%m/%d")
            labels.append(date)
            today_date = today_date - timedelta(days=1)
            


        print("Labels: ", labels)
        print("Data: ", data)

        context = {
        'repository': repository,
        'commits': commits,
        'days': days,
        'labels': labels,
        'data': data,
        }

        return render(request, "insights/contributors.html", context)

    elif days == 30:
        now = datetime.now()

        today = now.strftime("%Y/%m/%d")
        today_date = datetime.strptime(today, "%Y/%m/%d")


        labels = []
        data = []

        for x in range(0, 30):
            commits = list(Commit.objects.all().filter(repository = repository, date_time__range = [today_date, (today_date + timedelta(days=1))]))
            data.append(len(commits))
            date = (now - timedelta(x)).strftime("%Y/%m/%d")
            labels.append(date)
            today_date = today_date - timedelta(days=1)
            


        print("Labels: ", labels)
        print("Data: ", data)

        context = {
        'repository': repository,
        'commits': commits,
        'days': days,
        'labels': labels,
        'data': data,
        }

        return render(request, "insights/contributors.html", context)
    else:
        now = datetime.now()

        today = now.strftime("%Y/%m/%d")
        today_date = datetime.strptime(today, "%Y/%m/%d")


        labels = []
        data = []

        for x in range(0, 12):
            commits = list(Commit.objects.all().filter(repository = repository, date_time__range = [today_date, (today_date + timedelta(days=30))]))
            data.append(len(commits))
            date = (now - timedelta(x*30)).strftime("%Y/%m")
            labels.append(date)
            today_date = today_date - timedelta(days=30)
            


        print("Labels: ", labels)
        print("Data: ", data)

        context = {
        'repository': repository,
        'commits': commits,
        'days': days,
        'labels': labels,
        'data': data,
        }

        return render(request, "insights/contributors.html", context)
        

    commits = list(Commit.objects.all().filter(repository = repository, date_time__range = [yesterday, now]))



    context = {
        'repository': repository,
        'commits': commits,
        'days': days,
    }

    return render(request, "insights/contributors.html", context)












