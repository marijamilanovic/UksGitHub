from django.shortcuts import render, get_object_or_404, redirect
from pullrequest.models import Pullrequest
from .models import Comment, EMOJI_PICKER
from repository.models import Repository
from django.contrib.auth.models import User
from datetime import date

def addComment(request, id):
    if request.method == 'POST':
        pullrequest = get_object_or_404(Pullrequest, id=id)
        repository = get_object_or_404(Repository, id=pullrequest.prRepository.id)
        user = request.user

        content = request.POST.get('comment')
        created_date = date.today()
        comment = Comment(author = user, content = content, created_date = created_date)
        comment.save()

        pullrequest.comments.add(comment)
        pullrequest.save()
        comments = pullrequest.comments.all()

        return render(request, "updatePullrequest.html", {"pullrequest": pullrequest, "repository": repository, "comments":comments})

