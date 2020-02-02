from rest_framework import generics,mixins,permissions
from comments.models import Comment
from .serializers import CommentListSerializer,CommentDetailSerializer,create_comment_serializer
from bookapp_api.permissions import IsOwnerOrReadOnly
from profiles.models import Profile

class CommentListAPIView(generics.ListAPIView):
    queryset=Comment.objects.parent()
    serializer_class=CommentListSerializer
    permission_classes=[permissions.AllowAny]
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
    

class CommentDetailAPIView(mixins.DestroyModelMixin,mixins.UpdateModelMixin,generics.RetrieveAPIView):
    queryset=Comment.objects.parent()
    serializer_class=CommentDetailSerializer
    permission_classes=[IsOwnerOrReadOnly]


    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.patch(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


class CommentCreateAPIView(generics.CreateAPIView):
    queryset=Comment.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        _id = self.request.GET.get("id")
        parent_id = self.request.GET.get("parent_id", None)
        print(self.request.user)
        return create_comment_serializer(
                model_type=model_type, 
                _id=_id, 
                parent_id=parent_id,
                user=Profile.objects.get(user=self.request.user)
                )



