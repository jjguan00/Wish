# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
from .models import User, Wish, Like
from django.contrib import messages
import bcrypt

def index(request):
	return render(request, "index.html")

def signups(request):
	if request.method == "POST":
		errors = User.objects.sign_up_validator(request.POST)
		if len(errors):
			for tag,value in errors.iteritems():
				messages.error(request, value,extra_tags=tag)
				print(tag,value)
			return redirect('/')
		else:
			hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			User.objects.create(firstname = request.POST['firstname'], lastname = request.POST['lastname'], email = request.POST['email'], password= hash1)
			print("Created User.")
			return redirect('/')
	else:
		return redirect("/")
	return redirect('/')

def logins(request):
	if request.method == "POST":
		errors = User.objects.log_in_validator(request.POST)
		if len(errors):
			for tag, value in errors.iteritems():
				messages.error(request, value, extra_tags = tag)
				print(tag, value)
			return redirect('/')
		else:
			user = User.objects.get(email = request.POST['email'])
			request.session['user'] = user.id
			return redirect('/wishes')
	else:
		return redirect('/')

def wishes(request):
	if request.session['user']:
		user = User.objects.get(id = request.session['user'])
		wishes = Wish.objects.filter(user = user).filter(granted = False).order_by("-created_at")
		grantedWishes = Wish.objects.filter(granted = True).order_by("-created_at")
		like = Like.objects.filter()
		context = {
			'user' : user,
			'wishes': wishes,
			'grantedWishes':grantedWishes,
			'like': like
		}
		return render(request, "main.html", context)
	else:
		return redirect("/")

def new(request):
	if request.session['user']:
		user = User.objects.get(id = request.session['user'])
		context = {
			'user' : user
		}
		return render(request, "new.html", context)
	else:
		return redirect("/")

def makeWish(request):
	if request.session['user']:
		errors = Wish.objects.wish_validator(request.POST)
		if len(errors):
			for tag,value in errors.iteritems():
				messages.error(request, value,extra_tags=tag)
				print(tag,value)
			return redirect('/new')
		else:
			user = User.objects.get(id = request.session['user'])
			wish = Wish.objects.create(item = request.POST['item'], description = request.POST['description'], granted= False, user=user)
			print("Successfully created reviews and books.")
			return redirect("/wishes")
	else:
		return redirect("/")

def remove(request, number):
	if request.session['user']:
		wish = Wish.objects.get(id = number)
		user = User.objects.get(id = request.session['user'])
		if wish.user == user:
			wish.delete()
			return redirect("/wishes")
		else:
			return redirect("/wishes")
	else:
		return redirect("/")

def edit(request, number):
	if request.session['user']:
		wish = Wish.objects.get(id = number)
		user = User.objects.get(id = request.session['user'])
		context = {
			'wish' :wish
		}	
		if wish.user == user:
			return render(request, "edit.html", context)
		else:
			return redirect("/wishes")
	else:
		return redirect("/")

def editWish(request, number):
	if request.session['user']:
		errors = Wish.objects.wish_validator(request.POST)
		user = User.objects.get(id = request.session['user'])
		if len(errors):
			for tag,value in errors.iteritems():
				messages.error(request, value,extra_tags=tag)
				print(tag,value)
			return redirect('/edit/' + number)
		wish = Wish.objects.get(id = number)
		if wish.user == user:
			wish.item = request.POST['item']
			wish.description = request.POST['description']
			wish.save()
			return redirect("/wishes")
		else:
			return redirect("/edit/" + number)
	else:
		return redirect("/")

def grantWish(request, number):
	if request.session['user']:
		wish = Wish.objects.get(id = number)
		user = User.objects.get(id = request.session['user'])
		context = {
			'wish' :wish
		}	
		if wish.user == user:
			wish.granted = True
			wish.save()
			return redirect("/wishes")
		else:
			return redirect("/wishes")
	else:
		return redirect("/")

def stats(request):
	if request.session['user']:
		user = User.objects.get(id = request.session['user'])
		totalGrantedWishes = Wish.objects.filter()
		grantedWishes = Wish.objects.filter(user = user).filter(granted = True).order_by("-created_at")
		pendingWishes = Wish.objects.filter(user = user).filter(granted = False).order_by("-created_at")
		context = {
			'user': user,
			'totalGrantedWishes': totalGrantedWishes,
			'grantedWishes': grantedWishes,
			'pendingWishes': pendingWishes
		}
		return render(request, 'stats.html', context)
	else:
		return redirect("/")

def like(request, number):
	if request.session['user']:
		wish = Wish.objects.get(id = number)
		user = User.objects.get(id = request.session['user'])
		like = Like.objects.create(wish = wish, user = user)
		return redirect("/wishes")
	else:
		return redirect("/")

def logOut(request):
	request.session['user'] = None
	return redirect("/")