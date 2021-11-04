from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    date_of_birth = models.DateField(default=timezone.now)
    bio = models.TextField()
    location = models.CharField(max_length=30, blank=True)
    slug = models.SlugField(db_index=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + '->' + self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog-user', kwargs={'pk': self.pk, 'slug': self.slug})
