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