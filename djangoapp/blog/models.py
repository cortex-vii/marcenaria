from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Descrição")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nome")
    color = models.CharField(max_length=7, default="#007bff", verbose_name="Cor")
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['name']

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Arquivado'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Categoria")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    content = models.TextField(verbose_name="Conteúdo")
    excerpt = models.TextField(max_length=300, blank=True, verbose_name="Resumo")
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True, verbose_name="Imagem destacada")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Status")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Prioridade")
    views = models.PositiveIntegerField(default=0, verbose_name="Visualizações")
    likes = models.PositiveIntegerField(default=0, verbose_name="Curtidas")
    is_featured = models.BooleanField(default=False, verbose_name="Destaque")
    meta_title = models.CharField(max_length=60, blank=True, verbose_name="Meta Título")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta Descrição")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Publicado em")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Post")
    author_name = models.CharField(max_length=100, verbose_name="Nome")
    author_email = models.EmailField(verbose_name="Email")
    content = models.TextField(verbose_name="Comentário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    is_approved = models.BooleanField(default=False, verbose_name="Aprovado")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Comentário pai")

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['-created_at']

    def __str__(self):
        return f'Comentário de {self.author_name} em {self.post.title}'

class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=100, blank=True, verbose_name="Nome")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Inscrito em")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email
