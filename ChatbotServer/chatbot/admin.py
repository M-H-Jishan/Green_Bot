from django.contrib import admin
from .models import KnowledgeBase, Category, QueryLog

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('name',)

@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('question', 'short_answer', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('question', 'answer')
    autocomplete_fields = ('category',)
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
        return obj.answer[:100] + '...' if len(obj.answer) > 100 else obj.answer
    short_answer.short_description = 'Answer Preview'

@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('query', 'short_response', 'source', 'success', 'timestamp')
    list_filter = ('source', 'success', 'timestamp')
    search_fields = ('query', 'response', 'error_message')
    readonly_fields = ('query', 'response', 'source', 'success', 'error_message', 'timestamp')
    ordering = ('-timestamp',)

    def short_response(self, obj):
        return obj.response[:100] + '...' if len(obj.response) > 100 else obj.response
    short_response.short_description = 'Response Preview'

    def has_add_permission(self, request):
        return False

admin.site.site_header = 'Green Bot Administration'
admin.site.site_title = 'Green Bot Admin Portal'
admin.site.index_title = 'Welcome to the Green Bot Administration Portal'
