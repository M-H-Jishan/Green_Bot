from django.db import models
from django.utils import timezone

class Category(models.Model):
    """
    Categories for knowledge base entries
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:  # Only set created_at for new instances
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class KnowledgeBase(models.Model):
    """
    Enhanced model to store predefined FAQ data with categories and context
    """
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='required_for')
    related_questions = models.ManyToManyField('self', symmetrical=True, blank=True)
    source_url = models.URLField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.id:  # Only set created_at for new instances
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Knowledge Base"
        ordering = ['-updated_at']

class QueryLog(models.Model):
    """
    Model to log all chatbot interactions for analytics.
    """
    query = models.TextField()
    response = models.TextField(blank=True)
    source = models.CharField(max_length=50)  # KB, AI, DATA, DEFAULT, ERROR, etc.
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.query[:50]}..."

    class Meta:
        ordering = ['-timestamp']
