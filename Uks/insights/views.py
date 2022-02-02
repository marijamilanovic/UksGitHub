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
from user.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def pulse(request, id, days):
    repository = get_object_or_404(Repository, id=id)
    now = datetime.now()

    if days == 1:

        today = now.strftime("%Y/%m/%d")
        today_date = datetime.strptime(today, "%Y/%m/%d")

        open_pr = Pullrequest.objects.all().filter(prRepository = repository, status=OPENED, created__range = [(now - timedelta(days=1)), now])
        closed_pr = Pullrequest.objects.all().filter(prRepository = repository, status=CLOSED, created__range = [(now - timedelta(days=1)), now])
        merge_pr = Pullrequest.objects.all().filter(prRepository = repository, status=MERGED, created__range = [(now - timedelta(days=1)), now])

        open_is = Issue.objects.all().filter(repository = repository, state = ISSUE_STATE[0][0], created__range = [(now - timedelta(days=1)), now])
        closed_is = Issue.objects.all().filter(repository = repository, state = ISSUE_STATE[1][0], created__range = [(now - timedelta(days=1)), now])


        open_pr_list = list(open_pr)
        closed_pr_list = list(closed_pr)
        merge_pr_list = list(merge_pr)

        open_is_list = list(open_is)
        closed_is_list = list(closed_is)



        context = {
            'repository': repository,
            'days': days,
            'open_pr': len(open_pr_list),
            'closed_pr': len(closed_pr_list),
            'merge_pr': len(merge_pr_list),
            'open_is': len(open_is_list),
            'closed_is': len(closed_is_list),
            'open_pr_list': open_pr_list,
            'closed_pr_list': closed_pr_list,
            'merge_pr_list': merge_pr_list,
            'open_is_list': open_is_list,
            'closed_is_list': closed_is_list,
        }

        return render(request, "insights/base_insights.html", context)

    elif days == 3:


        today = now.strftime("%Y/%m/%d")
        today_date = datetime.strptime(today, "%Y/%m/%d")

        open_pr = Pullrequest.objects.all().filter(prRepository = repository, status=OPENED, created__range = [(now - timedelta(days=3)), now])
        closed_pr = Pullrequest.objects.all().filter(prRepository = repository, status=CLOSED, created__range = [(now - timedelta(days=3)), now])
        merge_pr = Pullrequest.objects.all().filter(prRepository = repository, status=MERGED, created__range = [(now - timedelta(days=3)), now])

        open_is = Issue.objects.all().filter(repository = repository, state = ISSUE_STATE[0][0], created__range = [(now - timedelta(days=3)), now])
        closed_is = Issue.objects.all().filter(repository = repository, state = ISSUE_STATE[1][0], created__range = [(now - timedelta(days=3)), now])

        

        open_pr_list = list(open_pr)
        closed_pr_list = list(closed_pr)
        merge_pr_list = list(merge_pr)

        open_is_list = list(open_is)
        closed_is_list = list(closed_is)

        context = {
            'repository': repository,
            'days': days,
            'open_pr': len(open_pr_list),
            'closed_pr': len(closed_pr_list),
            'merge_pr': len(merge_pr_list),
            'open_is': len(open_is_list),
            'closed_is': len(closed_is_list),
            'open_pr_list': open_pr_list,
            'closed_pr_list': closed_pr_list,
            'merge_pr_list': merge_pr_list,
            'open_is_list': open_is_list,
            'closed_is_list': closed_is_list,
        }


        return render(request, "insights/base_insights.html", context)


    elif days == 7:

        today = now.strftime("%Y/%m/%d")
        today_date = datetime.strptime(today, "%Y/%m/%d")

        open_pr = Pullrequest.objects.all().filter(prRepository = repository, status=OPENED, created__range = [(now - timedelta(days=7)), now])
        closed_pr = Pullrequest.objects.all().filter(prRepository = repository, status=CLOSED, created__range = [(now - timedelta(days=7)), now])
        merge_pr = Pullrequest.objects.all().filter(prRepository = repository, status=MERGED, created__range = [(now - timedelta(days=7)), now])

        open_is = Issue.objects.all().filter(repository = repository, state = ISSUE_STATE[0][0], created__range = [(now - timedelta(days=7)), now])
        closed_is = Issue.objects.all().filter(repository = repository, state = ISSUE_STATE[1][0], created__range = [(now - timedelta(days=7)), now])

        open_pr_list = list(open_pr)
        closed_pr_list = list(closed_pr)
        merge_pr_list = list(merge_pr)

        open_is_list = list(open_is)
        closed_is_list = list(closed_is)

        context = {
            'repository': repository,
            'days': days,
            'open_pr': len(open_pr_list),
            'closed_pr': len(closed_pr_list),
            'merge_pr': len(merge_pr_list),
            'open_is': len(open_is_list),
            'closed_is': len(closed_is_list),
            'open_pr_list': open_pr_list,
            'closed_pr_list': closed_pr_list,
            'merge_pr_list': merge_pr_list,
            'open_is_list': open_is_list,
            'closed_is_list': closed_is_list,
        }

        return render(request, "insights/base_insights.html", context)


    else:

        today = now.strftime("%Y/%m/%d")
        today_date = datetime.strptime(today, "%Y/%m/%d")

        open_pr = Pullrequest.objects.all().filter(prRepository = repository, status=OPENED, created__range = [(now - timedelta(days=30)), now])
        closed_pr = Pullrequest.objects.all().filter(prRepository = repository, status=CLOSED, created__range = [(now - timedelta(days=30)), now])
        merge_pr = Pullrequest.objects.all().filter(prRepository = repository, status=MERGED, created__range = [(now - timedelta(days=30)), now])

        open_is = Issue.objects.all().filter(repository = repository, state = ISSUE_STATE[0][0], created__range = [(now - timedelta(days=30)), now])
        closed_is = Issue.objects.all().filter(repository = repository, state = ISSUE_STATE[1][0], created__range = [(now - timedelta(days=30)), now])

        open_pr_list = list(open_pr)
        closed_pr_list = list(closed_pr)
        merge_pr_list = list(merge_pr)

        open_is_list = list(open_is)
        closed_is_list = list(closed_is)

        context = {
            'repository': repository,
            'days': days,
            'open_pr': len(open_pr_list),
            'closed_pr': len(closed_pr_list),
            'merge_pr': len(merge_pr_list),
            'open_is': len(open_is_list),
            'closed_is': len(closed_is_list),
            'open_pr_list': open_pr_list,
            'closed_pr_list': closed_pr_list,
            'merge_pr_list': merge_pr_list,
            'open_is_list': open_is_list,
            'closed_is_list': closed_is_list,
        }

        return render(request, "insights/base_insights.html", context)

@login_required(login_url="login")
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

        all_commits = commits1 + commits2 + commits3

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
        
        collaborators = []
        commits_collaborator = []


        for user in list(repository.developers.all()):
            collaborators.append(user)

        filtered = []

        for x in range(0, len(collaborators)):
            filtered = filter(lambda commit: commit.author_id == collaborators[x].id, all_commits)
            commits_collaborator.append(len(list(filtered)))
            filtered = []

        print("Collaborators: ", collaborators)
        print("Commits_collaborator: ", commits_collaborator)

        zip_iterator = zip(collaborators, commits_collaborator)
        commit_dic = dict(zip_iterator)

        context = {
        'repository': repository,
        'commits': commits,
        'days': days,
        'labels': labels,
        'data': data,
        'collaborators': commit_dic,
        }

        return render(request, "insights/contributors.html", context)

    elif days == 7:
        now = datetime.now()

        today = now.strftime("%Y/%m/%d")
        today_date = datetime.strptime(today, "%Y/%m/%d")


        labels = []
        data = []

        all_commits = []

        for x in range(0, 7):
            commits = list(Commit.objects.all().filter(repository = repository, date_time__range = [today_date, (today_date + timedelta(days=1))]))
            data.append(len(commits))
            date = (now - timedelta(x)).strftime("%Y/%m/%d")
            labels.append(date)
            today_date = today_date - timedelta(days=1)
            all_commits = all_commits + commits
            
        collaborators = []
        commits_collaborator = []


        for user in list(repository.developers.all()):
            collaborators.append(user)

        filtered = []

        for x in range(0, len(collaborators)):
            filtered = filter(lambda commit: commit.author_id == collaborators[x].id, all_commits)
            commits_collaborator.append(len(list(filtered)))
            filtered = []

        print("Collaborators: ", collaborators)
        print("Commits_collaborator: ", commits_collaborator)

        zip_iterator = zip(collaborators, commits_collaborator)
        commit_dic = dict(zip_iterator)


        print("Labels: ", labels)
        print("Data: ", data)

        context = {
        'repository': repository,
        'commits': commits,
        'days': days,
        'labels': labels,
        'data': data,
        'collaborators': commit_dic,
        }

        return render(request, "insights/contributors.html", context)

    elif days == 30:
        now = datetime.now()

        today = now.strftime("%Y/%m/%d")
        today_date = datetime.strptime(today, "%Y/%m/%d")


        labels = []
        data = []

        all_commits = []

        for x in range(0, 30):
            commits = list(Commit.objects.all().filter(repository = repository, date_time__range = [today_date, (today_date + timedelta(days=1))]))
            data.append(len(commits))
            date = (now - timedelta(x)).strftime("%Y/%m/%d")
            labels.append(date)
            today_date = today_date - timedelta(days=1)
            all_commits = all_commits + commits

        collaborators = []
        commits_collaborator = []


        for user in list(repository.developers.all()):
            collaborators.append(user)

        filtered = []

        for x in range(0, len(collaborators)):
            filtered = filter(lambda commit: commit.author_id == collaborators[x].id, all_commits)
            commits_collaborator.append(len(list(filtered)))
            filtered = []

        print("Collaborators: ", collaborators)
        print("Commits_collaborator: ", commits_collaborator)

        zip_iterator = zip(collaborators, commits_collaborator)
        commit_dic = dict(zip_iterator)
            


        print("Labels: ", labels)
        print("Data: ", data)

        context = {
        'repository': repository,
        'commits': commits,
        'days': days,
        'labels': labels,
        'data': data,
        'collaborators': commit_dic,
        }

        return render(request, "insights/contributors.html", context)
    else:
        now = datetime.now()

        today = now.strftime("%Y/%m/%d")
        today_date = datetime.strptime(today, "%Y/%m/%d")


        labels = []
        data = []

        all_commits = []

        for x in range(0, 12):
            commits = list(Commit.objects.all().filter(repository = repository, date_time__range = [today_date, (today_date + timedelta(days=30))]))
            data.append(len(commits))
            date = (now - timedelta(x*30)).strftime("%Y/%m")
            labels.append(date)
            today_date = today_date - timedelta(days=30)
            all_commits = all_commits + commits
            
        collaborators = []
        commits_collaborator = []


        for user in list(repository.developers.all()):
            collaborators.append(user)

        filtered = []

        for x in range(0, len(collaborators)):
            filtered = filter(lambda commit: commit.author_id == collaborators[x].id, all_commits)
            commits_collaborator.append(len(list(filtered)))
            filtered = []

        print("Collaborators: ", collaborators)
        print("Commits_collaborator: ", commits_collaborator)

        zip_iterator = zip(collaborators, commits_collaborator)
        commit_dic = dict(zip_iterator)

        print("Labels: ", labels)
        print("Data: ", data)

        context = {
        'repository': repository,
        'commits': commits,
        'days': days,
        'labels': labels,
        'data': data,
        'collaborators': commit_dic,
        }

        return render(request, "insights/contributors.html", context)
        

    commits = list(Commit.objects.all().filter(repository = repository, date_time__range = [yesterday, now]))



    context = {
        'repository': repository,
        'commits': commits,
        'days': days,
    }

    return render(request, "insights/contributors.html", context)

@login_required(login_url="login")
def commits(request, id):
    repository = get_object_or_404(Repository, id=id)

    now = datetime.now()

    today = now.strftime("%Y/%m/%d")
    today_date = datetime.strptime(today, "%Y/%m/%d")


    labels7 = []
    data7 = []

    labels18 = []
    data18 = []

    all_commits = []

    for x in range(0, 7):
        commits = list(Commit.objects.all().filter(repository = repository, date_time__range = [today_date, (today_date + timedelta(days=1))]))
        data7.append(len(commits))
        date = (now - timedelta(x)).strftime("%m/%d")
        labels7.append(date)
        today_date = today_date - timedelta(days=1)
        
    for x in range(0, 18):
        commits = list(Commit.objects.all().filter(repository = repository, date_time__range = [today_date, (today_date + timedelta(days=10))]))
        data18.append(len(commits))
        date = (now - timedelta(x*10)).strftime("%m/%d")
        labels18.append(date)
        today_date = today_date - timedelta(days=30)


    print(labels18)
    print(data18)


    
    context = {
        'repository': repository,
        'labels7': labels7,
        'data7': data7,
        'labels18': labels18,
        'data18': data18,
    }

    return render(request, "insights/commits.html", context)












