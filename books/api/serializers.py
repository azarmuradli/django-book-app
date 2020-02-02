from rest_framework import serializers
from books.models import Book
from comments.api.serializers import CommentListSerializer
from comments.models import Comment
from ratings.models import Rating
from rest_framework.reverse import reverse



class BookSerializer(serializers.ModelSerializer):
    author=serializers.SerializerMethodField()
    ratings=serializers.SerializerMethodField()
    class Meta:
        model=Book
        field=['id','author','title','image','ratings']

    def get_author(self,obj):
        return obj.author.user.username
    
    def get_ratings(self,obj):
        qs=Rating.objects.filter(book=obj)
        return qs.count()

    

class BookListSerializer(serializers.ModelSerializer):
    comments=serializers.SerializerMethodField()
    author=serializers.SerializerMethodField()
    ratings=serializers.SerializerMethodField()
    uri=serializers.SerializerMethodField()
    rating_desc=serializers.SerializerMethodField()
    comment_count=serializers.SerializerMethodField()
    class Meta:
        model=Book
        fields=['id','uri','author','title','comment_count','image','comments','ratings','rating_desc']

    def get_comments(self,obj):
        content_type=obj.get_content_type
        comments_qs=Comment.objects.filter_by_instance(obj)
        comments=CommentListSerializer(comments_qs,many=True).data
        return comments
    def get_author(self,obj):
        return obj.author.user.username
    
    def get_ratings(self,obj):
        qs=Rating.objects.filter(book=obj)
        return qs.count()

    def get_rating_desc(self,obj):
        qs=Rating.objects.filter(book=obj)
        return {
                "1star":qs.filter(star=1).count(),
                "2star":qs.filter(star=2).count(),
                "3star":qs.filter(star=3).count(),
                "4star":qs.filter(star=4).count(),
                "5star":qs.filter(star=5).count(),
            }
    def get_uri(self, obj):
        request = self.context.get('request')
        return reverse("books-api:detail", kwargs={"pk": obj.id},request=request)
    
    def get_comment_count(self,obj):
        content_type=obj.get_content_type
        comments_qs=Comment.objects.filter_by_instance(obj)
        return comments_qs.count()

class BookDetailSerializer(serializers.ModelSerializer):
    comments=serializers.SerializerMethodField()
    author=serializers.SerializerMethodField()
    ratings=serializers.SerializerMethodField()
    rating_desc=serializers.SerializerMethodField()
    average=serializers.SerializerMethodField()
    comment_count=serializers.SerializerMethodField()
    class Meta:
        model=Book
        fields=['id','author','title','comment_count','image','comments','ratings','rating_desc','average']
    
    def get_comments(self,obj):
        content_type=obj.get_content_type
        comments_qs=Comment.objects.filter_by_instance(obj)
        comments=CommentListSerializer(comments_qs,many=True).data
        return comments
    def get_author(self,obj):
        return obj.author.user.username
    
    def get_ratings(self,obj):
        qs=Rating.objects.filter(book=obj)
        return qs.count()

    def get_rating_desc(self,obj):
        qs=Rating.objects.filter(book=obj)
        return {
                "1star":qs.filter(star=1).count(),
                "2star":qs.filter(star=2).count(),
                "3star":qs.filter(star=3).count(),
                "4star":qs.filter(star=4).count(),
                "5star":qs.filter(star=5).count(),
            }
    def get_average(self,obj):
        qs=Rating.objects.filter(book=obj)
        total=0
        for one in qs:
            total+=one.star
        return total/qs.count()
    
    def get_comment_count(self,obj):
        content_type=obj.get_content_type
        comments_qs=Comment.objects.filter_by_instance(obj)
        return comments_qs.count()
