# views.py
from django.shortcuts import render, redirect
from .models import Publication
from Recette.forms import RecetteeModelForm
from .forms import PublicationForm
from django.shortcuts import render, get_object_or_404
def ajouter_publication(request):
    if request.method == 'POST':
        publication_form = PublicationForm(request.POST)
        recette_form = RecetteeModelForm(request.POST, request.FILES)  # Inclure request.FILES ici

        if publication_form.is_valid() and recette_form.is_valid():
            # Sauvegarder la recette avec l'image
            recette = recette_form.save()

            # Créer une publication et l'associer à la recette
            publication = publication_form.save(commit=False)
            publication.recette = recette  # Associe la recette à la publication
            publication.save()

            return redirect('publication_liste')  # Redirige vers la liste des publications après l'ajout

    else:
        publication_form = PublicationForm()
        recette_form = RecetteeModelForm()

    return render(request, 'Publication/ajouter.html', {
        'publication_form': publication_form,
        'recette_form': recette_form
    })


# def publication_liste(request):
#     query = request.GET.get('titre')  # Get the search query from the request
#     if query:
#         publications = Publication.objects.filter(titre__icontains=query)  # Filter by `titre`
#     else:
#         publications = Publication.objects.all()
    
#     return render(request, 'Publication/publication_liste.html', {'publications': publications})

# views.py
# from django.shortcuts import render
# from .models import Publication
# from django.db.models import Q
# from datetime import datetime

# def publication_liste(request):
#     query = request.GET.get('title')
#     min_date = request.GET.get('min_date')
#     max_date = request.GET.get('max_date')
    
#     publications = Publication.objects.all()
    
#     if query:
#         publications = publications.filter(title__icontains=query)
#     if min_date:
#         publications = publications.filter(created_at__gte=min_date)
#     if max_date:
#         publications = publications.filter(created_at__lte=max_date)
    
#     return render(request, 'Publication/publication_liste.html', {'publications': publications})
# views.py
from django.shortcuts import render
from .models import Publication

def publication_liste(request):
    # Start with all publications
    publications = Publication.objects.select_related('recette').all()

    # Filter by title of the publication
    title_query = request.GET.get('title')
    if title_query:
        publications = publications.filter(title__icontains=title_query)

    # Filter by title of the associated recipe
    recette_title_query = request.GET.get('recette_title')
    if recette_title_query:
        publications = publications.filter(recette__title__icontains=recette_title_query)

    # Filter by cuisine of the associated recipe
    cuisine_query = request.GET.get('cuisine')
    if cuisine_query:
        publications = publications.filter(recette__cuisine__icontains=cuisine_query)

    # Filter by servings of the associated recipe
    servings_query = request.GET.get('servings')
    if servings_query:
        try:
            servings_query = int(servings_query)
            publications = publications.filter(recette__servings=servings_query)
        except ValueError:
            pass  # Ignore filter if conversion fails

    # Filter by cook time of the associated recipe
    min_cook_time = request.GET.get('min_cook_time')
    max_cook_time = request.GET.get('max_cook_time')
    if min_cook_time:
        try:
            min_cook_time = int(min_cook_time)
            publications = publications.filter(recette__cook_time__gte=min_cook_time)
        except ValueError:
            pass
    if max_cook_time:
        try:
            max_cook_time = int(max_cook_time)
            publications = publications.filter(recette__cook_time__lte=max_cook_time)
        except ValueError:
            pass

    # Filter by difficulty level of the associated recipe
    difficulty_query = request.GET.get('difficulty')
    if difficulty_query:
        publications = publications.filter(recette__difficulty_level__iexact=difficulty_query)

    # Render the filtered publications to the template
    return render(request, 'Publication/publication_liste.html', {'publications': publications})


from Comment.forms import CommentForm
from Comment.models import Comment
from django.shortcuts import get_object_or_404, redirect

def publication_detail(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    comments = Comment.objects.filter(publication=publication)

    # Handle the comment form submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.publication = publication  # Link the comment to the publication
            comment.save()
            return redirect('publication_detail', pk=publication.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'Publication/publication_detail.html', {
        'publication': publication,
        'comments': comments,
        'comment_form': comment_form
    })
from django import forms
from .models import Publication, Recette

