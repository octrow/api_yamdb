from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reviews"


# Если прописать тут verbose_name то можно русифицировать раздел в админке.
