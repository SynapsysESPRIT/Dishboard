from django.shortcuts import render, redirect
from .forms import CommentForm
from .models import Comment
from django.views.generic import ListView
from django.db.models import Q
from datetime import datetime, timedelta
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



from django.contrib import messages

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.auteur = request.user
            comment.save()

            # Add notification message
            messages.success(request, f'New comment by {request.user.username}')
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
                    Q(contenu__icontains=search)
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
    publication = comment.publication

    if request.method == 'POST':
        comment.contenu = request.POST.get('contenu')
        comment.save()
        return JsonResponse({
            'status': 'success',
            'content': comment.contenu
        })

    return render(request, 'Publication/Publication.html', {
        'comment': comment,
        'publication': publication
    })





def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    publication_id = comment.publication.id
    comment.delete()
    return redirect('publication_detail', pk=publication_id)

def comment_detail(request, id):
    comment = Comment.objects.get(id=id)
    return render(request, 'Comment/detail.html', {'comment': comment})
