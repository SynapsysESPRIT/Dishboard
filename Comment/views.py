from django.shortcuts import render, redirect
from .forms import CommentForm
from .models import Comment

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
    else:
        form = CommentForm()
    return render(request, 'Comment/add_comment.html', {'form': form})
