from .models import Post, Comment, Category, Tag, Newsletter

def dashboard_stats(request):
    """Context processor para fornecer dados do dashboard"""
    if request.path.startswith('/admin/'):
        try:
            total_posts = Post.objects.count()
            published_posts = Post.objects.filter(status='published').count()
            draft_posts = Post.objects.filter(status='draft').count()
            archived_posts = Post.objects.filter(status='archived').count()
            pending_comments = Comment.objects.filter(is_approved=False).count()
            newsletter_subscribers = Newsletter.objects.filter(is_active=True).count()
            recent_posts = Post.objects.select_related('category').order_by('-created_at')[:5]
            
            return {
                'total_posts': total_posts,
                'published_posts': published_posts,
                'draft_posts': draft_posts,
                'archived_posts': archived_posts,
                'pending_comments': pending_comments,
                'newsletter_subscribers': newsletter_subscribers,
                'recent_posts': recent_posts,
            }
        except:
            # Se as tabelas não existirem ainda, retorna valores padrão
            return {
                'total_posts': 0,
                'published_posts': 0,
                'draft_posts': 0,
                'archived_posts': 0,
                'pending_comments': 0,
                'newsletter_subscribers': 0,
                'recent_posts': [],
            }
    return {}