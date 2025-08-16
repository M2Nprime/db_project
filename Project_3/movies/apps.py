# (محتوای صحیح و کامل برای movies/apps.py)
from django.apps import AppConfig

class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    def ready(self):
        # این خط کد حیاتی، سیگنال‌ها را به جنگو معرفی می‌کند
        import movies.signals