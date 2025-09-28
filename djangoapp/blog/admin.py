from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeDateFilter
from .models import Category, Tag, Post, Comment, Newsletter

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def post_count(self, obj):
        count = obj.post_set.count()
        return format_html('<span style="font-weight: bold;">{}</span>', count)
    post_count.short_description = 'Posts'

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['name', 'color_preview', 'post_count']
    search_fields = ['name']
    
    def color_preview(self, obj):
        return format_html(
            '<span style="display: inline-block; width: 20px; height: 20px; '
            'background-color: {}; border-radius: 50%; border: 1px solid #ccc;"></span>',
            obj.color
        )
    color_preview.short_description = 'Cor'
    
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Posts'

class CommentInline(TabularInline):
    model = Comment
    extra = 0
    fields = ['author_name', 'content', 'is_approved', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = [
        'title', 
        'author', 
        'category', 
        'status_badge', 
        'priority_badge',
        'is_featured',
        'views', 
        'likes',
        'comment_count',
        'published_at'
    ]
    list_filter = [
        'status', 
        'priority',
        'is_featured',
        'category', 
        'tags',
        ('created_at', RangeDateFilter),
        ('published_at', RangeDateFilter),
    ]
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at', 'views', 'likes']
    inlines = [CommentInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Conteúdo', {
            'fields': ('content', 'excerpt', 'featured_image')
        }),
        ('Configurações', {
            'fields': ('status', 'priority', 'is_featured', 'tags')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ['collapse']
        }),
        ('Estatísticas', {
            'fields': ('views', 'likes', 'created_at', 'updated_at', 'published_at'),
            'classes': ['collapse']
        }),
    )
    
    actions = ['make_published', 'make_draft', 'make_featured']
    
    def status_badge(self, obj):
        colors = {
            'draft': '#6c757d',
            'published': '#28a745',
            'archived': '#ffc107'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 12px; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def priority_badge(self, obj):
        colors = {
            'low': '#17a2b8',
            'medium': '#ffc107',
            'high': '#fd7e14',
            'urgent': '#dc3545'
        }
        color = colors.get(obj.priority, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 12px; font-size: 11px;">{}</span>',
            color, obj.get_priority_display()
        )
    priority_badge.short_description = 'Prioridade'
    
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comentários'
    
    def make_published(self, request, queryset):
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} posts foram publicados.')
    make_published.short_description = 'Publicar posts selecionados'
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} posts foram movidos para rascunho.')
    make_draft.short_description = 'Mover para rascunho'
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} posts foram marcados como destaque.')
    make_featured.short_description = 'Marcar como destaque'

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ['author_name', 'post', 'content_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at', 'post__category']
    search_fields = ['author_name', 'author_email', 'content']
    readonly_fields = ['created_at']
    actions = ['approve_comments', 'reject_comments']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Conteúdo'
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comentários foram aprovados.')
    approve_comments.short_description = 'Aprovar comentários'
    
    def reject_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comentários foram rejeitados.')
    reject_comments.short_description = 'Rejeitar comentários'

@admin.register(Newsletter)
class NewsletterAdmin(ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at']
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} inscrições foram ativadas.')
    activate_subscriptions.short_description = 'Ativar inscrições'
    
    def deactivate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} inscrições foram desativadas.')
    deactivate_subscriptions.short_description = 'Desativar inscrições'
