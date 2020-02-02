
from django.contrib import admin
from django.urls import path,include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/books/',include(('books.api.urls','books-api'),namespace='book-api')),
    path('api/comments/',include(('comments.api.urls','comment-api'),namespace='comment-api')),
    path('api/ratings/',include(('ratings.api.urls','ratings-api'),namespace='ratings-api')),
    path('api/likes/',include(('likes.api.urls','likes-api'),namespace='likes-api')),
    path('api/auth/',include(('accounts.api.urls','accounts-api'),namespace='accounts-api')),
    path('api/profiles/',include(('profiles.api.urls','profiles-api'),namespace='profiles-api'))
]

if settings.DEBUG:
    # test mode
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
