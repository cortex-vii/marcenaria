from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up

@receiver(user_signed_up)
def make_user_staff(sender, **kwargs):
    """
    Signal para tornar o usuário membro da equipe (staff) automaticamente
    quando ele se cadastra via allauth
    """
    user = kwargs['user']
    user.is_staff = True
    user.save()
    print(f"Usuário {user.email} foi definido como staff automaticamente")

@receiver(post_save, sender=User)
def ensure_staff_status(sender, instance, created, **kwargs):
    """
    Signal adicional para garantir que novos usuários sejam staff
    (backup para outros métodos de criação de usuário)
    """
    if created and not instance.is_superuser:
        if not instance.is_staff:
            instance.is_staff = True
            instance.save()
            print(f"Usuário {instance.email or instance.username} foi definido como staff")