from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'title', 'created_at']
    list_filter = ['rating', 'created_at', 'product']
    search_fields = ['title', 'comment', 'user__username', 'product__name']
    readonly_fields = ['created_at', 'updated_at']

