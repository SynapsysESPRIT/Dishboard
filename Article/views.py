from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse_lazy
from .form import ArticleModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
# Create your views here.
from .models import Article
def list(request):
     
    article = Article.objects.all()
    
    return render(request ,'Article/list.html' , {"data" :article})
class AddArticle(CreateView):
    
    model=Article
    template_name="Article/add.html"
    
    form_class=ArticleModelForm
    success_url = reverse_lazy('list')
class Details(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "article/details.html"  # Modifiez le chemin du template pour "article/details.html"
    context_object_name = "article"  # Le nom du contexte qui sera utilisé dans le template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        article = self.get_object()  # Récupère l'instance de l'article
        
        # Vous pouvez ajouter d'autres données supplémentaires au contexte si nécessaire
        # Par exemple, vous pourriez ajouter des commentaires associés à l'article (si vous avez un modèle de commentaire)
        # context['comments'] = Comment.objects.filter(article=article)
        
        return context
class UpdateArticle(UpdateView):
    model = Article
    template_name = "Article/add.html"  # Le formulaire pour ajouter ou modifier l'article
    form_class = ArticleModelForm
    success_url = reverse_lazy('list')
        
class DeleteArticle(DeleteView):
    model = Article
    template_name = "Article/delete.html"  # Template pour la confirmation de suppression
    success_url = reverse_lazy('list')