from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import BookForm, ReviewForm, SignupForm
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


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    extra_context = {"page_title": "本の編集"}

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "本を更新しました。")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "入力内容を確認してください。", extra_tags="danger")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("book:book_detail", kwargs={"pk": self.object.pk})


class BookDeleteView(DeleteView):
    model = Book
    # クラス定義時はURL設定の読み込みが完了していない可能性があるため、
    # reverse_lazyで、URLの文字列が必要になるまで解決を遅らせる。
    # BookUpdateView.get_success_urlのようにメソッド内ならreverseを使う。
    success_url = reverse_lazy("book:book_list")


class ReviewCreateView(LoginRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = "book/review_form.html"

    def get_context_data(self, **kwargs):
        # テンプレートに渡す変数の辞書を作る。親からformなどの標準の変数を受け取る。
        context = super().get_context_data(**kwargs)
        # self.kwargsはURLから受け取った値。book_pkで投稿対象の本を検索する。
        # 見つからなければ404。見つかればテンプレートで {{ book.title }} などを使える。
        context["book"] = get_object_or_404(Book, pk=self.kwargs["book_pk"])
        return context

    def form_valid(self, form):
        # 入力の検証に成功したときに呼ばれる。form.instanceは保存予定のReview。
        # URLで指定された本をレビューに紐づける。この代入だけではDBには保存されない。
        form.instance.book = get_object_or_404(Book, pk=self.kwargs["book_pk"])
        # リクエストしてきたユーザーをセットする
        form.instance.author = self.request.user
        # 親の処理でレビューを保存し、get_success_url()へのリダイレクトを作る。
        # 保存したReviewはself.objectに入る。
        response = super().form_valid(form)
        # 今回のリクエストに成功通知を登録し、移動先の画面で表示できるようにする。
        messages.success(self.request, "レビューを投稿しました。")
        return response

    def form_invalid(self, form):
        # 検証に失敗したときに呼ばれる。失敗通知を登録する。
        messages.error(self.request, "入力内容を確認してください。", extra_tags="danger")
        # 保存せず、入力値とエラーを保持したフォームで同じ画面を再表示する。
        # このときもget_context_data()で投稿対象の本をテンプレートに渡す。
        return super().form_invalid(form)

    def get_success_url(self):
        # 保存したレビューのbook_id（紐づく本の主キー）から、本の詳細画面のURLを作る。
        return reverse("book:book_detail", kwargs={"pk": self.object.book_id})


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("book/login")