from django.db import models
from django.conf import settings
from books.models import Book
from django.db.models.signals import post_save
from django.dispatch import receiver

User=settings.AUTH_USER_MODEL


class Profile(models.Model):
    user                = models.OneToOneField(User,on_delete=models.CASCADE)
    image               = models.ImageField(upload_to='media/profiles/',blank=True,null=True)
    # favorite_cate       = models.ForeignKey('categories.Category',on_delete=models.CASCADE,null=True,blank=True)
    followers           = models.ManyToManyField('self',related_name='isfollowing', symmetrical=False,null=True,blank=True)
    book_list           = models.ManyToManyField(Book,related_name='book_list',null=True,blank=True)
    wish_list           = models.ManyToManyField(Book,related_name='wish_list',null=True,blank=True)
    currently_reading   = models.ManyToManyField(Book,related_name='currently_reading',null=True,blank=True)
    created             = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.user.username


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
            

