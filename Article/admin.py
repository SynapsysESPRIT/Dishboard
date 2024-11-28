from django.contrib import admin


from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'created_at', 'updated_at')  # Affiche ces champs dans la liste des articles
    search_fields = ('titre', 'contenu')  # Ajoute une barre de recherche pour le titre et le contenu
    list_filter = ('created_at', 'updated_at')  # Filtre par date de création et de mise à jour
