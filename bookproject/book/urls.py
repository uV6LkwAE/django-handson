from django.urls import path

from .import views

app_name = "book"

urlpatterns = [
    # 残りのパスが空なら、views.indexを呼び出す
    # 今回の場合はどちらからも削られていない
    path("", views.index, name="index"),
    path("books", views.BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
]