from django.contrib.auth.models import User
from django.shortcuts import render

# from shop.models import Product, Review

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import numpy as np
import pandas as pd
import scipy as sp
import pymysql
from sklearn.neighbors import NearestNeighbors
from django.contrib.auth.decorators import login_required

from shop.models import Product, Review
from . import contentbased as cb


def recommendation(request):
    connection = pymysql.connect("localhost", "root", "", "allbachelorshop")
    products = pd.read_sql_query("SELECT * from shop_product", connection)
    ratings = pd.read_sql_query("SELECT * from shop_review", connection)

    create_date = lambda val: val[-5:-1] if val[-1] == ')' else np.nan

    product_ratings = ratings.groupby('product_id')['rating']
    print(product_ratings)
    avg_ratings = product_ratings.mean()
    num_ratings = product_ratings.count()
    last_rating = ratings.groupby('product_id').max()['pub_date']

    rating_count_df = pd.DataFrame({'avg_rating': avg_ratings, 'num_ratings': num_ratings})
    rating_count_df = rating_count_df.join(last_rating)

    product_recs = products.set_index('id').join(rating_count_df)

    ranked_product = product_recs.sort_values(['avg_rating', 'num_ratings', 'pub_date'], ascending=False)

    # ranked_product = ranked_product[ranked_product['num_ratings'] > 4]
    # print(ranked_product)

    context = {
        "object_list": ranked_product[:15],
        "title": "List"}

    return render(request, "tfidf/recommendation.html", context)


def detail(request, id):
    connection = pymysql.connect("localhost", "root", "", "allbachelorshop")
    ds = pd.read_sql_query("SELECT * from shop_product", connection)

    detail = Review.objects.select_related('product')
    results = cb.getFrames(ds)
    content = cb.recommend(item_id=id, num=6, results=results)
    print(detail)
    context = {
        "detail": detail,
        "content": content,
    }

    return render(request, "tfidf/detail.html", context)


def post_list(request):
    userId = request.user.id
    userName = request.user.username
    queryset = Review.objects.select_related('product')

    paginator = Paginator(queryset, 6)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:

        queryset = paginator.page(1)
    except EmptyPage:

        queryset = paginator.page(paginator.num_pages)

    context = {
        "user_id": userId,
        "user_name": userName,
        "object_list": queryset,
        "title": "List"}
    return render(request, "tfidf/home.html", context)


def get_suggestions(request):
    num_reviews = Review.objects.count()
    all_user_names = list(map(lambda x: x.username, User.objects.only("username")))
    all_product_ids = set(map(lambda x: x.product.id, Review.objects.only("product")))
    num_users = len(list(all_user_names))
    print(num_users)
    productRatings_m = sp.sparse.dok_matrix((num_users, max(all_product_ids) + 1), dtype=np.float32)
    for i in range(num_users):  # each user corresponds to a row, in the order of all_user_names
        user_reviews = Review.objects.filter(user_name=all_user_names[i])
        for user_review in user_reviews:
            productRatings_m[i, user_review.product.id] = user_review.rating

        productRatings = productRatings_m.transpose()

        coo = productRatings.tocoo(copy=False)
    df = pd.DataFrame({'products': coo.row, 'users': coo.col, 'rating': coo.data})[
        ['products', 'users', 'rating']].sort_values(['products', 'users']).reset_index(drop=True)

    mo = df.pivot_table(index=['products'], columns=['users'], values='rating')
    mo.fillna(3, inplace=True)
    model_knn = NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=7)
    model_knn.fit(mo.values)
    distances, indices = model_knn.kneighbors((mo.iloc[14, :]).values.reshape(1, -1), return_distance=True)
    print(distances, indices)
    print(Product.objects.all())
    username= request.user.username
    print(username)
    context = list(map(lambda x: Product.objects.get(id=indices.flatten()[x]), range(0, len(distances.flatten()))))
    return render(request, 'tfidf/cosinesim.html', {'username': request.user.username,'context': context})
