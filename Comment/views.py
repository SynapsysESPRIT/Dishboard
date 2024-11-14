from django.shortcuts import render, redirect
from .forms import CommentForm
from .models import Comment
from django.views.generic import ListView
from django.db.models import Q
from datetime import datetime, timedelta



def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
    else:
        form = CommentForm()
    return render(request, 'Comment/add_comment.html', {'form': form})

class CommentListView(ListView):
        model = Comment
        template_name = "comment/list.html"
        context_object_name = "comments"

        def get_queryset(self):
            queryset = Comment.objects.all()
            search = self.request.GET.get('search')
            date_filter = self.request.GET.get('date_filter')
            sort = self.request.GET.get('sort')

            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) | Q(contenu__icontains=search)
                )

            if date_filter:
                today = datetime.now().date()
                if date_filter == 'today':
                    queryset = queryset.filter(created_at=today)
                elif date_filter == 'week':
                    week_ago = today - timedelta(days=7)
                    queryset = queryset.filter(created_at__gte=week_ago)
                elif date_filter == 'month':
                    month_ago = today - timedelta(days=30)
                    queryset = queryset.filter(created_at__gte=month_ago)

            if sort:
                queryset = queryset.order_by(sort)

            return queryset

def update_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'Comment/update_comment.html', {'form': form})


def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect('comment_list')

def comment_detail(request, id):
    comment = Comment.objects.get(id=id)
    return render(request, 'Comment/detail.html', {'comment': comment})
