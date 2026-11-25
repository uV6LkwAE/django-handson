from django.urls import path

from .import views

app_name = "book"

urlpatterns = [
    # 残りのパスが空なら、views.indexを呼び出す
    # 今回の場合はどちらからも削られていない
    path("accounts/signup/", views.SignupView.as_view(), name="signup"),
    path("books/<int:book_pk>/reviews/create/", views.ReviewCreateView.as_view(), name="review_create"),
    path("", views.index, name="index"),
    path("books", views.BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("books/create/", views.BookCreateView.as_view(), name="book_create"),
    path("books/<int:pk>/update/", views.BookUpdateView.as_view(), name="book_update"),
    path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book_delete"),
]