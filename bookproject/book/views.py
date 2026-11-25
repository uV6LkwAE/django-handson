from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .forms import BookForm
from .models import Book

# Create your views here.

def index(request):
    return HttpResponse("Hello")

class BookListView(ListView):
    model = Book
    context_object_name = "books"

class BookDetailView(DetailView):
    model = Book

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    # 追加でpage_titleをコンテキストとして渡す
    # 新規作成も編集も、共通のbook_form.htmlを使っているため、動的にタイトルを切り替える
    extra_context = {"page_title": "本の新規作成"}

    # CreateViewがPOSTデータ・ファイルからBookFormを作り、is_valid()で検証する。
    # 検証OKならform_valid(form)、NGならform_invalid(form)を自動で呼ぶ。
    def form_valid(self, form):
        # formは検証済みのBookForm。入力値やファイル、整形済みのcleaned_dataを持つ。
        # 親の処理でDBに保存し、詳細画面へのリダイレクトレスポンスを作る。
        response = super().form_valid(form)
        # self.requestは今回のHTTPリクエスト。成功通知を紐づけ、移動先で表示できるようにする。
        # このメッセージはテンプレートで表示する。
        messages.success(self.request, "本を登録しました")
        # 保存後に作ったレスポンスを返し、ブラウザを移動させる。
        return response

    def form_invalid(self, form):
        # formは検証に失敗したBookForm。入力値と、各項目のエラーを保持している。
        # 画面に表示する失敗通知を登録。dangerはBootstrapの警告色用の追加タグ。
        messages.error(self.request, "入力内容を確認してください。", extra_tags="danger")
        # DBには保存せず、入力値・エラーを持つformで入力画面を再表示する。
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("book:book_detail", kwargs={"pk": self.object.pk})

