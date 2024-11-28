from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse_lazy
from .form import ArticleModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from .models import Article
from User.models import Professional
from django.shortcuts import render, get_object_or_404, redirect

def list(request):
    article = Article.objects.all()
    is_professional = isinstance(request.user, Professional) if request.user.is_authenticated else False
    return render(request, 'Article/list.html', {"data": article, "is_professional": is_professional})

class AddArticle(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "Article/add.html"
    form_class = ArticleModelForm
    success_url = reverse_lazy('blog')

    def dispatch(self, request, *args, **kwargs):
        if not isinstance(request.user, Professional):
            return HttpResponseForbidden("Unauthorized")
        return super().dispatch(request, *args, **kwargs)

def detailsClass(request):
    id = request.GET.get('id')
    if id is None:
        return HttpResponse("ID is missing", status=400)

    item = get_object_or_404(Article, id=id)  # Remplacez `YourModel` par votre modèle
    return render(request, 'Article/details.html', {'item': item})

#class UpdateArticle(UpdateView):
   # model = Article
   # template_name = "Article/add.html"  # Le formulaire pour ajouter ou modifier l'article
   #  form_class = ArticleModelForm
   # success_url = reverse_lazy('list')
def updateClass(request):
    if not isinstance(request.user, Professional):
        return HttpResponse("Unauthorized", status=403)

    article_id = request.GET.get('id')
    if not article_id or not article_id.isdigit():
        return HttpResponse("Invalid or missing ID", status=400)

    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.titre = request.POST.get('titre', article.titre)
        article.contenu = request.POST.get('contenu', article.contenu)
        article.save()
        return redirect('blog')

    return render(request, 'Article/update.html', {'article': article})
        
from django.http import HttpResponseForbidden

class DeleteArticle(DeleteView):
    model = Article
    template_name = "Article/delete.html"
    success_url = reverse_lazy('blog')

    def dispatch(self, request, *args, **kwargs):
        if not isinstance(request.user, Professional):
            return HttpResponseForbidden("Unauthorized")
        return super().dispatch(request, *args, **kwargs)



def blog(request):
    article = Article.objects.all()  # Get all articles
    is_professional = isinstance(request.user, Professional) if request.user.is_authenticated else False
    return render(request, 'Article/blog-posts.html', {"data": article, "is_professional": is_professional})


