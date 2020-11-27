from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, login_required, login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from shop.models import Product
from .forms import ProfileForm, CustomChangePasswordForm
from .models import Profile


def profiles(request):
    """Load Homepage via Profile Link"""
    profiles = Profile.objects.all().filter(user_id=request.user.id)
    product_list = Product.objects.order_by('-name')
    return render(request, 'profiles/index.html', {'profiles': profiles,'product_list': product_list},

                                                                        )


@login_required
def profile(request, profile_slug):
    """Load Profile"""
    profile = get_object_or_404(Profile, slug=profile_slug)
    return render(request, 'profiles/profile.html', {'profile': profile})


@login_required
def edit_profile(request, profile_slug):
    """Edit Profile Form"""
    profile = get_object_or_404(Profile, slug=profile_slug)
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "{} {}'s profile updated."
                             .format(form.cleaned_data["first_name"],
                                     form.cleaned_data["last_name"]))
            return HttpResponseRedirect(profile.get_absolute_url())
    return render(request, "profiles/edit-profile.html", {'form': form})


@login_required
def change_password(request, profile_slug):
    """Change Password Form"""
    if request.method == 'POST':
        form = CustomChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was '
                                      'successfully updated!')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomChangePasswordForm(request.user)
    return render(request, 'profiles/change-password.html', {
        'form': form
    })
