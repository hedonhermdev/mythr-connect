from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


#       User profile.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    about = models.CharField(max_length=140, null=True)
    birthdate = models.DateField(null=True)
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, **kwargs):
    instance.profile.save()


#       Post model.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=140, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post('{self.title}, {self.author}')"

#       Comment model.
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    date_published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment('{self.content}', '{self.post}', '{self.author}')"
