from django.db import models
from books.models import Book
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator 

User=settings.AUTH_USER_MODEL


   
class Rating(models.Model):
    book    = models.ForeignKey(Book,on_delete=models.CASCADE)
    user    = models.ForeignKey('profiles.Profile',on_delete=models.CASCADE)
    star    = models.IntegerField(default=5,validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return str(self.star)

    
    

