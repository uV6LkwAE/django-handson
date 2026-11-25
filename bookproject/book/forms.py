from django import forms

from .models import Book, Review


class BookForm(forms.ModelForm):
    class Meta:
        # モデルの指定
        model = Book
        # 入力させたいフィールド
        fields = ["title", "category", "caption", "image"]
        # 画面に表示する各フィールドのラベル
        labels = {
            "title": "タイトル",
            "category": "カテゴリー",
            "caption": "キャプション",
            "image": "画像",
        }
        # 入力部品の種類とHTML属性（CSSクラスなど）を指定
        # form.as_pなどでの描画時に反映され、テンプレート側の記述を減らす目的
        # 作成・編集で別のテンプレートを使っても、form.as_pで同じ定義から入力欄を生成できる。
        # ラベルやCSSクラスの変更をここにまとめ、各テンプレートでの手書き・修正を減らす。
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "caption": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content"]
        labels = {"content": "レビュー本文"}
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }