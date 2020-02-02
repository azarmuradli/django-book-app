from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

User=settings.AUTH_USER_MODEL

class CommentManager(models.Manager):
    def parent(self):
        qs=self.filter(parent=None)
        return qs

    
    def filter_by_instance(self,instance):
        content_type=ContentType.objects.get_for_model(instance.__class__)
        obj_id=instance.id
        qs=self.filter(content_type=content_type,object_id=obj_id).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, _id, content, user, parent_obj=None):
            model_qs = ContentType.objects.filter(model=model_type)
            if model_qs.exists():
                SomeModel = model_qs.first().model_class()
                obj_qs = SomeModel.objects.filter(id=_id)
                if obj_qs.exists() and obj_qs.count() == 1:
                    instance = self.model()
                    instance.content = content
                    instance.user = user
                    instance.content_type = model_qs.first()
                    instance.object_id = obj_qs.first().id
                    if parent_obj:
                        instance.parent = parent_obj
                    instance.save()
                    return instance
            return None

class Comment(models.Model):
    user=models.ForeignKey('profiles.Profile',on_delete=models.CASCADE)
    content=models.CharField(max_length=2000)
    published_date=models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent=models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)

    objects=CommentManager()

    def __str__(self):
        return self.content
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self)
    
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True