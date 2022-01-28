from queue import Empty
from django.shortcuts import render, get_object_or_404, redirect
from pullrequest.models import Pullrequest
from .models import Comment, EMOJI_PICKER, Emoji
from repository.models import Repository
from django.contrib.auth.models import User
from datetime import date

def addComment(request, id):
    if request.method == 'POST':
        pullrequest = get_object_or_404(Pullrequest, id=id)
        user = request.user

        content = request.POST.get('comment')
        created_date = date.today()
        comment = Comment(author = user, content = content, created_date = created_date)
        comment.save()

        pullrequest.comments.add(comment)
        pullrequest.save()

        return redirect('/pullrequest/updatePullrequestPage/'+ str(pullrequest.id))

def addEmoji(request, id, pr_id):
    errorTitle = None
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=id)
        emoji = Emoji()
        emoji.name = request.POST.get('emoji')
        emoji.reaction_creator = request.user
        emoji_exists = Emoji.objects.filter(name=emoji.name, reaction_creator = emoji.reaction_creator)
        
        if len(emoji_exists) is 0:
            emoji.save()
            comment.emojis.add(emoji)
            comment.save()
        else:
            comment.emojis.remove(emoji_exists[0].id)
            comment.save()
            emoji_exists[0].delete()
        return redirect('/pullrequest/updatePullrequestPage/'+ str(pr_id))
       