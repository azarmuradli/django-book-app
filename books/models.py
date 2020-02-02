from django.db import models
from django.conf import settings
from comments.models import Comment
from categories.models import Category
from django.contrib.contenttypes.models import ContentType


User=settings.AUTH_USER_MODEL


class Book(models.Model):
    author          = models.ForeignKey('profiles.Profile',default=1,on_delete=models.CASCADE)
    title           = models.CharField(max_length=100)
    description     = models.CharField(max_length=1000)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    publish_date    = models.DateTimeField(auto_now_add=True,null=True)
    image           = models.ImageField(default=1,upload_to='media/')


    def __str__(self):
        return self.title
    @property
    def comments(self):
        instance=self
        qs=Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance=self
        content_type=ContentType.objects.get_for_model(instance.__class__)
        return content_type

