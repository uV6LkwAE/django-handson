from django.urls import path

from .import views

app_name = "book"

urlpatterns = [
    # 残りのパスが空なら、views.indexを呼び出す
    # 今回の場合はどちらからも削られていない
    path("", views.index, name="index"),
]