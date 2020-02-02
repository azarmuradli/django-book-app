from django.db import models
from comments.models import Comment
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator 

User=settings.AUTH_USER_MODEL


   
class Like(models.Model):
    comment    = models.ForeignKey(Comment,on_delete=models.CASCADE)
    user    = models.ForeignKey('profiles.Profile',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
