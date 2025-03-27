from django.contrib import admin
from django.utils.html import format_html
from .models import KnowledgeBase, Category, Intent, QueryLog

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('name',)

@admin.register(Intent)
class IntentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('name',)

@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('question', 'short_answer', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('question', 'answer')
    autocomplete_fields = ('category', 'prerequisites', 'related_questions')
    filter_horizontal = ('prerequisites', 'related_questions')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Question Information', {
            'fields': ('question', 'answer', 'category')
        }),
        ('Related Content', {
            'fields': ('prerequisites', 'related_questions'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('source_url', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def short_answer(self, obj):
        """Display truncated answer in list view"""
        return obj.answer[:100] + '...' if len(obj.answer) > 100 else obj.answer
    short_answer.short_description = 'Answer Preview'

@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('query', 'short_response', 'source', 'timestamp')
    list_filter = ('source', 'timestamp')
    search_fields = ('query', 'response')
    readonly_fields = ('query', 'response', 'source', 'timestamp')
    ordering = ('-timestamp',)

    def short_response(self, obj):
        """Display truncated response in list view"""
        return obj.response[:100] + '...' if len(obj.response) > 100 else obj.response
    short_response.short_description = 'Response Preview'

    def has_add_permission(self, request):
        """Prevent manual addition of query logs"""
        return False

# Customize admin site
admin.site.site_header = 'University Chatbot Administration'
admin.site.site_title = 'Chatbot Admin Portal'
admin.site.index_title = 'Welcome to the Chatbot Administration Portal'
