from re import search
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, auth
import datetime

class register_table(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.CharField(max_length=100,null=True)
    contact_number = models.BigIntegerField(blank=True,null=True)
    profile_pic = models.ImageField(upload_to = 'profilepics',null=True,blank=True)
    Institute = models.CharField(max_length=1000,null=True)
    gender = models.CharField(max_length=250,blank=True,null=True)
    occupation = models.CharField(max_length=250,null=True)
    added_on =models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)
    place = models.CharField(max_length=1000,null=True)
    over = models.FloatField(default=2)
    darkmode = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = "Register Table"


class Post(models.Model):
    uname = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    post_title = models.CharField(max_length=200,null=True)
    author = models.CharField(max_length=200,null=True, blank=True)
    comp = models.CharField(max_length=200,null=True, blank=True)
    label1 = models.CharField(max_length=200,null=True, blank=True)
    inp1 = models.CharField(max_length=200,null=True, blank=True)
    label2 = models.CharField(max_length=200,null=True, blank=True)
    inp2 = models.CharField(max_length=200,null=True, blank=True)
    desc = models.TextField(null=True)
    category = models.CharField(max_length=50)
    place = models.CharField(max_length=1000, null=True)
    price = models.CharField(max_length=100, null=True)
    sha = models.CharField(max_length=100,null=True)
    likes = models.ManyToManyField(User,related_name='likes',blank=True)
    post_date = models.DateTimeField(auto_now_add=True,null=True)
    sell = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural = "Products"
    def num_likes(self):
        return self.likes.count()

class PostImage(models.Model):
    cover = models.ImageField(upload_to='covers',null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        #return f"{self.user}-{self.post}-{self.value}"
        return self.user

class Seainp(models.Model):
    inp = models.CharField(max_length=100000,null=True)
    users = models.ManyToManyField(User,related_name='users',blank=True)
    all = models.IntegerField(null=True)
    def __str__(self):
        return str(self.inp)
    def num_users(self):
        return self.users.count()

class Search(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    inp = models.CharField(max_length=100000,null=True)
    sea_date = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return str(self.inp)
    class Meta:
        verbose_name_plural = "Search"

class contact(models.Model):
    email = models.CharField(max_length=100,null=True)
    msg = models.TextField(null=True)
    ans = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural = "FAQs"

class feedback(models.Model):
    email = models.CharField(max_length=100,null=True)
    msg = models.TextField(null=True)
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural = "Feedback"