# views.py
from django.shortcuts import render, redirect
from .models import Publication, Rating
from Recette.forms import RecetteeModelForm
from .forms import PublicationForm
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import NewsletterSubscriber
from django.contrib import messages
from django.db.models import Avg
import json
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import get_template
from django.http import HttpResponseForbidden
from Comment.models import Comment




def ajouter_publication(request):
    if request.method == 'POST':
        # Create Recipe
        recette = Recette.objects.create(
            titre=request.POST['titre'],
            description=request.POST['description'],
            inventory=request.POST['inventory'],
            instructions=request.POST['instructions'],
            cook_time=request.POST['cook_time'],
            servings=request.POST['servings'],
            cuisine=request.POST['cuisine'],
            difficulty_level=request.POST['difficulty_level'],
            image=request.FILES['image']
        )
        
    
        publication = Publication.objects.create(
            title=request.POST['title'],
            recette=recette
        )
        
        return redirect('publication_liste')
        
    return render(request, 'Publication/Publication_list.html')



from django.shortcuts import get_object_or_404, redirect
from Comment.models import Comment

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    publication_id = comment.publication.id
    comment.delete()
    return redirect('publication_detail', pk=publication_id)  # Use 'pk' here instead of 'publication_id'


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
    return render(request, 'Publication/Publication_list.html', {'publications': publications})


from Comment.forms import CommentForm
from Comment.models import Comment
from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages

def publication_detail(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    comments = Comment.objects.filter(publication=publication)
    latest_publications = Publication.objects.select_related('recette').order_by('-created_at')[:3]
    like_count = publication.ratings.filter(like=True).count()
    user_rating = None
    if request.user.is_authenticated:
        user_rating = publication.ratings.filter(user=request.user).first()

    if request.method == 'POST':
        if 'update_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            comment.title = request.POST.get('title')
            comment.contenu = request.POST.get('contenu')
            comment.save()
            messages.info(request, f'Comment updated by {request.user.username}')
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.publication = publication
                comment.auteur = request.user
                comment.save()
                messages.success(request, f'New comment added by {request.user.username} on {publication.title}')
    else:
        comment_form = CommentForm()

    context = {
        'publication': publication,
        'comments': comments,
        'comment_form': comment_form,
        'latest_publications': latest_publications,
        'like_count': like_count,
        'user_rating': user_rating,
        'average_rating': publication.ratings.aggregate(Avg('stars'))['stars__avg']
    }
   
    return render(request, 'Publication/Publication.html', context)






from django import forms
from .models import Publication, Recette

def publication_view(request):
    latest_posts = Publication.objects.select_related('recette').order_by('-created_at')[:3]
    return render(request, 'Publication/Publication.html', {'latest_posts': latest_posts})


def delete_publication(request, id):
    publication = Publication.objects.get(id=id)
    if request.method == 'POST':
        publication.delete()
        return redirect('publication_liste')

def update_publication(request, id):
    publication = Publication.objects.get(id=id)
    
    if request.method == 'POST':
        # Update the publication
        publication.title = request.POST['title']
        
        # Update the associated recipe
        recette = publication.recette
        recette.titre = request.POST['titre']
        recette.description = request.POST['description']
        recette.inventory = request.POST['inventory']
        recette.instructions = request.POST['instructions']
        recette.cook_time = request.POST['cook_time']
        recette.servings = request.POST['servings']
        recette.cuisine = request.POST['cuisine']
        recette.difficulty_level = request.POST['difficulty_level']
        
        # Handle image update if provided
        if 'image' in request.FILES:
            recette.image = request.FILES['image']
            
        recette.save()
        publication.save()
        
        return redirect('publication_liste')
        
    return redirect('publication_liste')

from django.shortcuts import render, get_object_or_404, redirect
from Comment.models import Comment
from Comment.forms import CommentForm  # Assuming you have a form for updating comments

def update_comment(request, publication_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    publication = get_object_or_404(Publication, id=publication_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('publication_detail', pk=publication_id)  # Redirect to the publication detail page
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comment/update_comment.html', {'form': form, 'comment': comment, 'publication': publication})


from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        
        if not subscriber.is_confirmed:
            confirmation_url = request.build_absolute_uri(
                reverse('confirm_subscription', args=[subscriber.confirmation_token])
            )
            
            html_message = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;">
                        <div style="background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
                            <h1 style="margin: 0;">Welcome to Our Newsletter!</h1>
                        </div>
                        
                        <div style="background: white; padding: 20px; border-radius: 10px; margin-top: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                            <h2 style="color: #333; text-align: center;">One Last Step!</h2>
                            
                            <p style="color: #666;">Thank you for subscribing to our newsletter. To complete your subscription, please click the button below:</p>
                            
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="{confirmation_url}" style="background-color: #4CAF50; color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">Confirm Subscription</a>
                            </div>
                            
                            <p style="color: #666; font-size: 0.9em;">If the button doesn't work, copy and paste this link into your browser:</p>
                            <p style="color: #666; font-size: 0.9em; word-break: break-all;">{confirmation_url}</p>
                        </div>
                        
                        <div style="text-align: center; margin-top: 20px; color: #666; font-size: 0.8em;">
                            <p>This email was sent to {email}</p>
                            <p>© 2024 Your Company Name. All rights reserved.</p>
                        </div>
                    </body>
                </html>
            """
            
            send_mail(
                'Confirm Your Newsletter Subscription',
                '',  # Plain text version
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=html_message,
                fail_silently=False,
            )
            
        return JsonResponse({'status': 'success', 'message': 'Please check your email to confirm subscription'})
    return JsonResponse({'status': 'error'})



def confirm_subscription(request, token):
    try:
        subscriber = NewsletterSubscriber.objects.get(confirmation_token=token)
        subscriber.is_confirmed = True
        subscriber.save()
        return redirect(f'{reverse("publication_liste")}?confirmed=true')
    except NewsletterSubscriber.DoesNotExist:
        return redirect('publication_liste')
    


def track_share(request, pk, platform):
    publication = Publication.objects.get(pk=pk)
    
    # Increment platform-specific counter
    if platform == 'facebook':
        publication.facebook_shares += 1
    elif platform == 'twitter':
        publication.twitter_shares += 1
    elif platform == 'linkedin':
        publication.linkedin_shares += 1
    elif platform == 'whatsapp':
        publication.whatsapp_shares += 1
    
    publication.share_count += 1
    publication.save()
    
    return JsonResponse({
        'status': 'success',
        'total_shares': publication.share_count,
        f'{platform}_shares': getattr(publication, f'{platform}_shares')
    })



def rate_publication(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        publication = get_object_or_404(Publication, id=data['publication_id'])
        
        # Check if user already has a rating for this publication
        existing_rating = Rating.objects.filter(
            publication=publication,
            user=request.user
        ).first()
        
        if existing_rating:
            # Update existing rating
            existing_rating.stars = data['rating']
            existing_rating.review = data['review']
            existing_rating.like = True if int(data['rating']) > 3 else False
            existing_rating.save()
            message = 'Rating updated successfully!'
        else:
            # Create new rating
            Rating.objects.create(
                publication=publication,
                user=request.user,
                stars=data['rating'],
                review=data['review'],
                like=True if int(data['rating']) > 3 else False
            )
            message = 'Rating submitted successfully!'

        avg_rating = publication.ratings.aggregate(Avg('stars'))['stars__avg'] or 0
        like_count = publication.ratings.filter(like=True).count()
        
        return JsonResponse({
            'success': True,
            'message': message,
            'average_rating': round(avg_rating, 1),
            'like_count': like_count,
            'is_update': existing_rating is not None
        })

    
def toggle_like(request):
    data = json.loads(request.body)
    publication = get_object_or_404(Publication, id=data['publication_id'])
    rating = Rating.objects.filter(publication=publication, user=request.user).first()
    
    if rating:
        rating.like = not rating.like
        rating.save()
    else:
        rating = Rating.objects.create(
            publication=publication,
            user=request.user,
            like=True
        )
    
    return JsonResponse({
        'success': True,
        'like_count': publication.ratings.filter(like=True).count(),
        'liked': rating.like  # Add this to track the current like state
    })

def delete_review(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id, user=request.user)
    rating.delete()
    return JsonResponse({'success': True})

def export_publication_pdf(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    template = get_template('Publication/publication_pdf.html')
    html = template.render({'publication': publication})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="publication_{publication.id}.pdf"'
    
    HTML(string=html).write_pdf(response)
    return response


#import openai
from django.conf import settings
#from openai import OpenAI

'''def chatbot_api(request):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    message = json.loads(request.body)['message']
   
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful recipe creation assistant. Provide detailed cooking instructions and ingredient lists."},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
        max_tokens=500
    )
   
    return JsonResponse({
        'response': response.choices[0].message.content,
        'status': 'success'
    })'''

#from llama_cpp import Llama

'''def chatbot_api(request):
    message = json.loads(request.body)['message']
    
    llm = Llama(
        model_path="D:/GGUFs/qwen2.5-0.5b-instruct-q5_k_m.gguf",  # Update with your model path
        n_ctx=2048,
        n_threads=4
    )
    
    prompt = f"""
    System: You are a recipe creation assistant. Create detailed recipes with instructions and ingredients.
    User: {message}
    Assistant:"""
    
    output = llm(prompt, max_tokens=500, temperature=0.7)
    
    return JsonResponse({
        'response': output['choices'][0]['text'],
        'status': 'success'
    })'''


#import replicate
import os
#import requests

'''def chatbot_api(request):
    try:
        message = json.loads(request.body)['message']
        print(f"Received message: {message}")
        
        headers = {
            'Authorization': f'Bearer {settings.LLAMA_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful recipe creation assistant."},
                {"role": "user", "content": message}
            ],
            "stream": False
        }
        
        print("Sending request to Llama API")
        response = requests.post(
            'https://api.llama-api.com/chat/completions',
            headers=headers,
            json=data
        )
        print(f"Llama API response: {response.text}")
        
        return JsonResponse({
            'response': response.json()['choices'][0]['message']['content'],
            'status': 'success'
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({
            'response': str(e),
            'status': 'error'
        })'''

#from llamaapi import LlamaAPI

'''def chatbot_api(request):
    print("API endpoint hit")
    llama = LlamaAPI('LA-d7e412c8ddd041d988f31e3cfb2d7fc8b63a34fa5cab4fa0b67da6c279ffcde0')
    message = json.loads(request.body)['message']
    print(f"Received message: {message}")
    
    api_request = {
        "messages": [
            {"role": "system", "content": "You are a recipe creation assistant that provides detailed cooking instructions and ingredient lists."},
            {"role": "user", "content": message}
        ],
        "stream": False,
        "max_length": 512
    }
    
    response = llama.run(api_request)
    return JsonResponse({
        'response': response.json()['choices'][0]['message']['content'],
        'status': 'success'
    })'''


from anthropic import Anthropic

def chatbot_api(request):
    anthropic = Anthropic(api_key='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')
    message = json.loads(request.body)['message']
    
    response = anthropic.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1000,
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": "You are a professional recipe creation assistant. Create detailed recipes with ingredients, instructions, cooking times, and helpful tips."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )
    
    return JsonResponse({
        'response': response.content[0].text,
        'status': 'success'
    })





