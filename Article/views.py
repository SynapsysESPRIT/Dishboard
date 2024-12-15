from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy
from .form import ArticleModelForm
from .models import Article
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import pipeline
import json

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    summary = article.get_summary()
    
    context = {
        'article': article,
        'summary': summary,
    }
    return render(request, 'details.html', context)

def list(request):
    articles = Article.objects.all()
    return render(request, 'Article/list.html', {"data": articles})

class AddArticle(CreateView):
    model = Article
    template_name = "Article/add.html"
    form_class = ArticleModelForm
    success_url = reverse_lazy('blog')

def detailsClass(request):
    id = request.GET.get('id')
    if id is None:
        return HttpResponse("ID is missing", status=400)

    item = get_object_or_404(Article, id=id)
    return render(request, 'Article/details.html', {'item': item})

def updateClass(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        article.titre = request.POST.get('titre', article.titre)
        article.contenu = request.POST.get('contenu', article.contenu)
        article.save()
        return redirect('blog')

    return render(request, 'Article/update.html', {'article': article})

class DeleteArticle(DeleteView):
    model = Article
    template_name = "Article/delete.html"
    success_url = reverse_lazy('blog')

def blog(request):
    articles = Article.objects.all()
    return render(request, 'Article/blog-posts.html', {"data": articles})

@csrf_exempt
def summarize_text(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            
            if not text:
                return JsonResponse({'error': 'No text provided for summarization'}, status=400)
            
            if len(text) > 1000:
                text = text[:1000]

            summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
            summarized_text = summary[0]['summary_text']

            return JsonResponse({'summary': summarized_text})
        
        except Exception as e:
            return JsonResponse({'error': f'Error during summarization: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
