from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_category', null=False, blank=True)
    category_name = models.CharField(max_length=100, null=False, blank=False)
    test = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f'{self.category_name}'


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='question_category', null=False, blank=True)
    question = models.CharField(max_length=225, null=False, blank=False)
    test = models.CharField(max_length=225, null=False, blank=False)

    def __str__(self):
        return f'{self.question}'
