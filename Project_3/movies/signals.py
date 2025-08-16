from django.db.models.signals import post_save, pre_delete # pre_delete را اضافه کنید
from django.dispatch import receiver
from .models import Movie

@receiver(post_save, sender=Movie)
def movie_saved_handler(sender, instance, created, **kwargs):
    if created:
        print(f"\n>>> SIGNAL DETECTED: A new movie was created: '{instance.title}'")

@receiver(pre_delete, sender=Movie)
def movie_about_to_be_deleted_handler(sender, instance, **kwargs):
    """
    This function will be called automatically right before a Movie object is deleted.
    """
    print(f"\n>>> SIGNAL DETECTED (pre_delete): About to delete the movie: '{instance.title}'")