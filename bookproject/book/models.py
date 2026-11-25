from django.db import models

# Create your models here.

class Book(models.Model):
    CATEGORY_CHOICES = (
        ("novel", "小説"),
        ("business", "ビジネス"),
        ("technology", "テクノロジー"),
        ("comic", "漫画"),
        ("other", "その他"),
    )

    title = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to="books/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Review(models.Model):
    # 本を削除すれば、紐づいているレビューも一緒に削除される。
    # レビューを削除しても、本は削除されない。
    # review.book → そのレビューに紐づく本（Bookオブジェクト）
    # book.reviews.all() → その本に紐づく全レビュー（QuerySet）
    # 逆方向の取得で使う reviews という名前は、related_nameで指定する。
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        # contentの最初の20字のみ返す
        return self.content[:20]
