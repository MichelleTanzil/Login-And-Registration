from django.db import models
from datetime import date, datetime
import re

# Create your models here.


class UserManager(models.Manager):
    def validator(self, post_data):
        today = date.today()
        age = today.year - datetime.strptime(post_data['birthday'], '%Y-%m-%d').year - ((today.month, today.day) < (datetime.strptime(post_data['birthday'], '%Y-%m-%d').month,datetime.strptime(post_data['birthday'], '%Y-%m-%d').day))
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        LETTER_REGEX = re.compile(r'^[a-zA-Z]*$')
        if not LETTER_REGEX.match(post_data['first_name']) or len(post_data['first_name']) < 2 :
            errors['first_name'] = "The first name field is required and should be at least 2 characters long."
        if not LETTER_REGEX.match(post_data['last_name']) or len(post_data['last_name']) < 2:
            errors['last_name'] = "The last name field is required and should be at least 2 characters long."
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = ("Invalid email address or email!")
        if User.objects.filter(email = post_data['email']).exists():
            errors['email'] = ("Email already exists, try logging in.")
        if len(post_data['password']) < 8 or len(post_data['password']) == 0:
            errors['password'] = "The password field is required and should be at least 8 characters long."
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = "Your passwords do not match, try again!"
        if len(post_data['birthday']) == 0:
            errors['birthday'] = "Your birthday should be a valid date."
        if datetime.strptime(post_data['birthday'], '%Y-%m-%d') > datetime.today():
            errors['birthday'] = "Your birthday should be in the past"
        if age < 13:
            errors['birthday'] = "You should be 13 years old or older"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    birthday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"<User Object: {self.id} {self.first_name} {self.last_name}>"
