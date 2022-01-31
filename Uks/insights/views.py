from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from repository.models import Repository
from pullrequest.models import Pullrequest, OPENED, CLOSED, MERGED
from issue.models import Issue, ISSUE_STATE



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


def contributors(request, id):
    repository = get_object_or_404(Repository, id=id)

    context = {
        'repository': repository
    }

    return render(request, "insights/contributors.html", context)












