from django.contrib import admin

from .models import Product, Category, Slider, SubCategory, Review, Cluster


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(SubCategory, SubCategoryAdmin)


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created', 'updated']
#     list_filter = ['available', 'created', 'updated', 'category']
#     list_editable = ['price', 'stock', 'available']
#     prepopulated_fields = {'slug': ('name',)}
#

admin.site.register(Product)


class SliderAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'description']


admin.site.register(Slider, SliderAdmin)


# for recommendation part

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('product', 'rating', 'comment', 'user_name', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']


class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']


admin.site.register(Review, ReviewAdmin)
admin.site.register(Cluster, ClusterAdmin)


