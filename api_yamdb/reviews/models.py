from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    text = models.TextField()
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='rewiews')
    # title = models.ForeignKey(
    #     Title, on_delete=models.CASCADE, related_name='titles')
    score = models.PositiveIntegerField(default=5,
                                        validators=[MinValueValidator(1),
                                                    MaxValueValidator(10)])

    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
