from django.db import models
from users.models import Profile
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField


class Blog(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(db_index=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog-post', kwargs={'pk': self.pk, 'slug': self.slug})


class Comment(models.Model):
    user_to_comment = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment_to_post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = RichTextField(blank=True, null=True)
    date_commented = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user_to_comment.user.username + '->' + self.comment_to_post.title


class UserViews(models.Model):
    viewer = models.CharField(max_length=150)
    viewee = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.viewer + ' to ' + self.viewee.user.username


class BlogViews(models.Model):
    viewer = models.CharField(max_length=150)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.viewer + ' to ' + self.blog.title


class PostScore(models.Model):
    pass
