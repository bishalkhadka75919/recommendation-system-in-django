from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
from shop.models import Product, Review
from django.contrib import messages

from django.db.models import Case, When
from .recommendation import Myrecommend
import numpy as np
import pandas as pd


# for recommendation
def recommend(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    df = pd.DataFrame(list(Review.objects.all().values()))
    nu = df.user_name.unique().shape[0]
    current_user_id = request.user_id
    # # if new user not rated any movie
    # if user_name > nu:
    #     product = Product.objects.get(id=15)
    #     q = Review(user=request.user, product=product, rating=0)
    #     q.save()

    print("Current user id: ", current_user_id)
    prediction_matrix, Ymean = Myrecommend()
    my_predictions = prediction_matrix[:, current_user_id - 1] + Ymean.flatten()
    pred_idxs_sorted = np.argsort(my_predictions)
    pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
    pred_idxs_sorted = pred_idxs_sorted + 1
    print(pred_idxs_sorted)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
    movie_list = list(Product.objects.filter(id__in=pred_idxs_sorted, ).order_by(preserved)[:10])
    return render(request, 'web/recommend.html', {'movie_list': movie_list})
