from django.db import models
from django.conf import settings

from django.db.models.signals import pre_save
from django.utils.text import slugify
# Create your models here.

class MessagePost(models.Model):
    title = models.CharField(max_length=50,null=False, blank=False)
    message = models.TextField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.author.username

def pre_save_message_post_receiver(sender, instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_message_post_receiver, sender=MessagePost)