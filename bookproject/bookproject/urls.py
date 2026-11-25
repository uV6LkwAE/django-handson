from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # includeには何も取り除かず、book.urlsに渡す
    path('', include('book.urls')),
]

# DEBUG=Trueの場合のみ、メディアを配信する
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)