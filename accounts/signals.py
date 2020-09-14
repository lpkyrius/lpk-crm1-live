from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Customer

'''
Signals são chamados nas funções de criação e de atualização dos Users
Assim, criam automaticamente o Customer quando um User se registra
bem como atualizam as informações quando ele atualiza seus dados de user
'''

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            name=instance.username,
            )
        print('Profile created!')

post_save.connect(customer_profile, sender=User)
