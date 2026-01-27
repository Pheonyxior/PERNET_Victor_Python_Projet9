from django.db import models
from django.core import validators
from PIL import Image
from authentication.models import User

class Ticket(models.Model):
    IMAGE_MAX_SIZE = (300, 300)

    title = models.fields.CharField(max_length=128)
    description = models.fields.TextField(max_length=2048,
                                          blank=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.fields.DateTimeField(auto_now_add=True)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()

class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    # rating = models.PositiveSmallIntegerField(
    #     validators=[validators.MinValueValidator(0), validators.MaxValueValidator(5)])
    rating = models.SmallIntegerField(choices=[(i, i) for i in range(6)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    headline = models.fields.CharField(max_length=128)
    body = models.fields.TextField(max_length=8192, blank=True)
    time_created = models.fields.DateTimeField(auto_now_add=True)

class UserFollows(models.Model):
    user = models.ForeignKey(to=User,
                             on_delete=models.CASCADE,
                             related_name='following')
    followed_user = models.ForeignKey(to=User,
                                      on_delete=models.CASCADE,
                                      related_name='followed_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )
        verbose_name_plural = "users followed"

    def __str__(self) -> str:
        return "followed user of " + str(self.user) + ": " \
            + str(self.followed_user)

class UserBlocks(models.Model):
    user = models.ForeignKey(to=User,
                             on_delete=models.CASCADE,
                             related_name='blocking')
    blocked_user = models.ForeignKey(to=User,
                                      on_delete=models.CASCADE,
                                      related_name='blocked_by')

    class Meta:
        unique_together = ('user', 'blocked_user', )
        verbose_name_plural = "users blocked"

    def __str__(self) -> str:
        return "blocked user of " + str(self.user) + ": " \
            + str(self.blocked_user)