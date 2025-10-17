from django.db import models


class ScriptCategory(models.Model):
    category_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name