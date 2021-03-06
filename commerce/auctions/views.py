from django.contrib.auth import authenticate, login, logout
from django import forms
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Bid, Comment

# pylint: disable=E1101

class CreateListingForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea())
    startingBid = forms.DecimalField(decimal_places=2)
    category = forms.CharField(required=False)
    imageUrl = forms.CharField(required=False)

def index(request):
    return render(request, "auctions/index.html", {
        "listItems": AuctionListing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def createListing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = AuctionListing(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                startingBid=form.cleaned_data["startingBid"],
                category=form.cleaned_data["category"],
                imageUrl=form.cleaned_data["imageUrl"])
            listing.save()
            return render(request, "auctions/create_listing.html", {
                "message": "Listing successfully created!",
                "form": CreateListingForm()
            })
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form,
                "message": "Invalid form. Please try again."
            })
    else:
        return render(request, "auctions/create_listing.html", {
            "form": CreateListingForm()
        })


def watchlist(request):
    return render(request, "auctions/watchlist.html")

def categories(request):
    return render(request, "auctions/categories.html")

def viewListing(request, listingId):
    listing = AuctionListing.objects.get(id=listingId)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })