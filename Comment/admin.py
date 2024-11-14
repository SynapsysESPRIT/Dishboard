from django.contrib import admin
from .models import Comment
from django.utils import timezone

class CommentDateFilter(admin.SimpleListFilter):
    title = 'date status'
    parameter_name = 'date_status'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Created Today'),
            ('this_week', 'Created This Week'),
            ('old', 'Older Than a Week'),
        )

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == 'today':
            return queryset.filter(created_at=today)
        if self.value() == 'this_week':
            return queryset.filter(created_at__gte=today-timezone.timedelta(days=7))
        if self.value() == 'old':
            return queryset.filter(created_at__lt=today-timezone.timedelta(days=7))

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['contenu', 'created_at', 'updated_at']
    list_filter = [CommentDateFilter, 'updated_at']
    search_fields = ['contenu']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 20

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        if search_term:
            queryset |= self.model.objects.filter(
                contenu__icontains=search_term
            )
        return queryset, use_distinct
