from django.contrib import admin
from django.utils import timezone
from .models import Publication

class LastFivePublicationsFilter(admin.SimpleListFilter):
    title = "Dernières publications"
    parameter_name = "last_five"

    def lookups(self, request, model_admin):
        return (
            ('last_five', "Les 5 dernières publications"),
        )

    def queryset(self, request, queryset):
        if self.value() == 'last_five':
            # Récupérer les IDs des 5 dernières publications
            last_five_ids = queryset.order_by('-created_at').values_list('id', flat=True)[:5]
            # Filtrer le queryset par ces IDs sans utiliser slice
            return queryset.filter(id__in=last_five_ids)
        return queryset

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    search_fields = ['title', 'created_at']
    list_filter = (LastFivePublicationsFilter, 'created_at')
