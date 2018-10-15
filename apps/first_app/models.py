# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
# Create your models here.
class UserManager(models.Manager):
	def sign_up_validator(self, postData):
		errors = {}
		if len(postData['firstname']) < 2:
			errors["firstname"] = "First name should be at least 2 characters"
		elif not re.match('[A-Za-z]+', postData['firstname']):
			errors['firstname'] = "First name may only contain letters."
		if len(postData['firstname']) < 2:
			errors["firstname"] = "First name should be at least 2 characters"
		elif not re.match('[A-Za-z]+', postData['firstname']):
			errors['firstname'] = "First name may only contain letters."
		if len(postData['lastname']) < 2:
			errors["lastname"] = "lastname name should be at least 2 characters"
		elif not re.match('[A-Za-z]+', postData['lastname']):
			errors['lastname'] = "lastname name may only contain letters."
		if len(postData['lastname']) < 2:
			errors["lastname"] = "lastname name should be at least 2 characters"
		elif not re.match('[A-Za-z]+', postData['lastname']):
			errors['lastname'] = "lastname name may only contain letters."
		if len(postData['password']) < 1:
			errors['email'] = "Please enter your email."
		elif User.objects.filter(email=postData['email']):
			errors['email'] = "Email is already taken."
		elif not re.match('[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+)*@[A-Za-z0-9-]+(.[A-Za-z0-9]+)*(.[A-Za-z]{2,})',postData['email']):
			errors['email'] = "Incorrect Email Format."
		if len(postData['password']) < 4:
			errors['password']= "Password must be longer than 4 characters"
		elif postData['pw_confirm'] != postData['password'] :
			errors['password']= "Password is not match"
		return errors
	def log_in_validator(self, postData):
		errors = {}
		if len(postData['email']) < 4:
			errors['email'] = "Please Enter Your Email"
		elif not User.objects.filter(email = postData['email']):
			errors['email_not_found'] = "Your email and password does not match."
		if len(postData['password']) < 1:
			errors['password'] = "Please enter your password"
		elif not bcrypt.checkpw(postData['password'].encode(), User.objects.get(email=postData['email']).password.encode()):
			errors['password'] = "Please enter the correct email or password."
		return errors

class WishManager(models.Manager):
	def wish_validator(self, postData):
		errors = {}
		if len(postData['item']) < 3:
			errors['item'] = "A wish must contain more than 3 characters."
		if len(postData['description']) < 3:
			errors['description'] = "Description must contain more than 3 characters."
		# if postData['rating'] > 5:
		# 	errors['rating'] = "You cannot rate a book above five"
		return errors

class User(models.Model):
	firstname = models.CharField(max_length = 36 , unique = True)
	lastname = models.CharField(max_length = 36 , unique = True)
	email = models.CharField(max_length = 100, unique = True)
	password = models.CharField(max_length = 36)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Wish(models.Model):
	item = models.TextField(max_length = 50)
	description = models.TextField(max_length = 500)
	user = models.ForeignKey(User, related_name = "reviews")
	granted = models.BooleanField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = WishManager()

class Like(models.Model):
	wish = models.ForeignKey(Wish, related_name = "likes")
	user = models.ForeignKey(User, related_name = "likes")
	created_at = models.DateTimeField(auto_now_add = True)