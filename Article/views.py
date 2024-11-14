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
from django.shortcuts import render, get_object_or_404, redirect

def list(request):
     
    article = Article.objects.all()
    
    return render(request ,'Article/list.html' , {"data" :article})
class AddArticle(CreateView):
    
    model=Article
    template_name="Article/add.html"
    
    form_class=ArticleModelForm
    success_url = reverse_lazy('blog')

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
    # Récupère l'ID passé dans l'URL
    article_id = request.GET.get('id')  # Utilisation de 'id' comme paramètre de l'URL
    if not article_id or not article_id.isdigit():  # Vérifier si l'ID est manquant ou invalide
        return HttpResponse("Invalid or missing ID", status=400)

    # Récupère l'article en fonction de l'ID
    article = get_object_or_404(Article, id=article_id)

    # Traite la mise à jour des champs lorsque la méthode est POST
    if request.method == 'POST':
        # Met à jour les champs de l'article directement avec les données POST
        article.titre = request.POST.get('titre', article.titre)  # Utilisez les bons noms de champs
        article.contenu = request.POST.get('contenu', article.contenu)  # Utilisez les bons noms de champs
        # Ajoutez d'autres champs à mettre à jour ici...

        article.save()  # Sauvegarde les modifications
        return redirect('blog')  # Redirige vers la page du blog après la mise à jour

    # Affiche l'article pour la mise à jour (même si vous n'utilisez pas de formulaire)
    return render(request, 'Article/update.html', {'article': article})
        
class DeleteArticle(DeleteView):
    model = Article
    template_name = "Article/delete.html"  # Template pour la confirmation de suppression
    success_url = reverse_lazy('blog')



def blog(request):
    article = Article.objects.all()
    return render(request, 'Article/blog-posts.html', {"data": article})

