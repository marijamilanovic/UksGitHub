from pickle import FALSE, TRUE
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
    if request.method == 'POST':
        have_emoji = FALSE
        emoji = Emoji()
        comment = get_object_or_404(Comment, id=id)
        emojis = comment.emojis.all()
        
        for e in emojis:
            if e.name == request.POST.get('emoji'):
                have_emoji = TRUE
                emoji = e
                
        if have_emoji == TRUE:
            add_reaction_creator(request, comment, emoji)
        else:
            create_new_emoji(request, comment)
      
        return redirect('/pullrequest/updatePullrequestPage/'+ str(pr_id))

def create_new_emoji(request, comment):
    emoji = Emoji()
    emoji.name = request.POST.get('emoji')
    emoji.save()
    user = request.user
    emoji.reaction_creators.add(user)
    emoji.save()
    comment.emojis.add(emoji)
    comment.save()

def add_reaction_creator(request, comment, emoji):
    reaction_creators = emoji.reaction_creators.all()
    for r in reaction_creators:
        if r.id == request.user.id:
            emoji.reaction_creators.remove(request.user.id)
            if len( emoji.reaction_creators.all()) == 0:
                comment.emojis.remove(emoji.id)
                comment.save()
        else:
            emoji.reaction_creators.add(request.user)
       