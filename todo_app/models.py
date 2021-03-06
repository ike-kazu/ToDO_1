from django.db import models

# https://zerofromlight.com/blogs/detail/11/
# https://blog.narito.ninja/detail/40
# Create your models here.

"""カテゴリー"""


class Category(models.Model):
    title = models.CharField('タイトル', max_length=20)

    def __str__(self):
        return self.title


"""
タイトル、日付テーブルとカテゴリーを紐づけるためのテーブル。
PROTECTは紐づいているデータが存在すれば消されない
"""


class ToDo(models.Model):
    title = models.CharField('タイトル', max_length=50)
    created_at = models.DateTimeField('日付', auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.title
