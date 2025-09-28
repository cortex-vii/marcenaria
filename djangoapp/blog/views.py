from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Post, Comment, Category, Tag, Newsletter

@staff_member_required
def admin_dashboard(request):
    # Estatísticas gerais
    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(status='published').count()
    draft_posts = Post.objects.filter(status='draft').count()
    total_comments = Comment.objects.count()
    pending_comments = Comment.objects.filter(is_approved=False).count()
    total_categories = Category.objects.count()
    total_tags = Tag.objects.count()
    newsletter_subscribers = Newsletter.objects.filter(is_active=True).count()
    
    # Estatísticas dos últimos 30 dias
    last_30_days = timezone.now() - timedelta(days=30)
    recent_posts = Post.objects.filter(created_at__gte=last_30_days).count()
    recent_comments = Comment.objects.filter(created_at__gte=last_30_days).count()
    recent_subscribers = Newsletter.objects.filter(subscribed_at__gte=last_30_days).count()
    
    # Posts mais populares (por visualizações)
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]
    
    # Categorias com mais posts
    top_categories = Category.objects.annotate(
        post_count=Count('post')
    ).order_by('-post_count')[:5]
    
    # Posts por status para gráfico
    posts_by_status = [
        {'status': 'Publicados', 'count': published_posts, 'color': '#28a745'},
        {'status': 'Rascunho', 'count': draft_posts, 'color': '#6c757d'},
        {'status': 'Arquivados', 'count': Post.objects.filter(status='archived').count(), 'color': '#ffc107'},
    ]
    
    # Posts por prioridade
    posts_by_priority = Post.objects.values('priority').annotate(count=Count('id')).order_by('priority')
    
    # Atividade recente - últimos 10 posts
    recent_activity = Post.objects.select_related('author', 'category').order_by('-created_at')[:10]
    
    # Comentários recentes não aprovados
    pending_comments_list = Comment.objects.select_related('post').filter(
        is_approved=False
    ).order_by('-created_at')[:5]
    
    context = {
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'total_comments': total_comments,
        'pending_comments': pending_comments,
        'total_categories': total_categories,
        'total_tags': total_tags,
        'newsletter_subscribers': newsletter_subscribers,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'recent_subscribers': recent_subscribers,
        'popular_posts': popular_posts,
        'top_categories': top_categories,
        'posts_by_status': posts_by_status,
        'posts_by_priority': posts_by_priority,
        'recent_activity': recent_activity,
        'pending_comments_list': pending_comments_list,
    }
    
    return render(request, 'admin/dashboard.html', context)
