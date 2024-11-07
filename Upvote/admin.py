from django.contrib import admin
from .models import Upvote
from django.utils import timezone

class UpvoteValueFilter(admin.SimpleListFilter):
    title = 'value status'
    parameter_name = 'value_status'

    def lookups(self, request, model_admin):
        return (
            ('high', 'High Value (>5)'),
            ('medium', 'Medium Value (2-5)'),
            ('low', 'Low Value (<2)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'high':
            return queryset.filter(value__gt=5)
        if self.value() == 'medium':
            return queryset.filter(value__range=(2, 5))
        if self.value() == 'low':
            return queryset.filter(value__lt=2)

class UpvoteTimeFilter(admin.SimpleListFilter):
    title = 'time period'
    parameter_name = 'time_period'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Created Today'),
            ('this_week', 'This Week'),
            ('older', 'Older'),
        )

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == 'today':
            return queryset.filter(created_at=today)
        if self.value() == 'this_week':
            return queryset.filter(created_at__gte=today-timezone.timedelta(days=7))
        if self.value() == 'older':
            return queryset.filter(created_at__lt=today-timezone.timedelta(days=7))

@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'value', 'created_at', 'updated_at', 'is_active']
    list_filter = [UpvoteValueFilter, UpvoteTimeFilter, 'is_active']
    search_fields = ['value']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 25

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        if search_term:
            try:
                value = int(search_term)
                queryset |= self.model.objects.filter(value=value)
            except ValueError:
                pass
        return queryset, use_distinct
