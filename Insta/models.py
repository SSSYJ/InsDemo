from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField
from django.contrib.auth.models import AbstractUser

# Create your models here.
class InsUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to = 'static/images/profile_pics',
        format = 'JPEG',
        options = {'quality': 100},
        blank = True,
        null = True,
    )
    
    def get_connections(self):
        connections = UserConnection.objects.filter(creator = self)
        return connections
    
    def get_followers(self):
        followers = UserConnection.objects.filter(following = self)
        return followers
    
    def is_followed_by(self, user):
        followers = UserConnections.objects.filter(following = self)
        return followers.filter(creator = user).exists()

    def get_absolute_url(self):
        return reverse("user_profile", args = [str(self.id)])


class Post(models.Model):
    author = models.ForeignKey(InsUser, on_delete = models.CASCADE, related_name = 'my_posts')
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG',
        options = {'quality': 100},
        blank = True,
        null = True,
    )

    def get_absolute_url(self):
        return reverse("post_detail", args = [str(self.id)])

    def get_like_count(self):
        return self.likes.count()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'likes')
    user = models.ForeignKey(InsUser, on_delete = models.CASCADE, related_name = 'likes')

    class Meta: 
        #every pair of (post, user) is unique, cannot duplicate {% endcomment %}
        unique_together = ("post", "user") 
        

    def __str__(self):
        return 'like:' + self.user.username + ' likes ' + self.post.title


class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable = False)
    creator = models.ForeignKey(InsUser, on_delete = models.CASCADE, related_name="creator_set")
    following = models.ForeignKey(InsUser, on_delete = models.CASCADE, related_name = "friend_Set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments')
    creator = models.ForeignKey(InsUser, on_delete = models.CASCADE)
    content = models.CharField(max_length=100)
    
    def __str__(self):
        return self.creator.username + ' comments on ' + self.post.title + ': ' + self.content