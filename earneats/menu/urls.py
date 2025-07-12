from django.urls import path
from menu import views

urlpatterns = [
        # CATEGORIES URLS
    path("", views.menuView, name="menu"),
    path("category/<slug:slug>/", views.getCategory, name="getCategory"),
    path("category/create/", views.createCategory, name="createCategory"),
    path("category/update/<int:pk>/", views.updateCategory, name="updateCategory"),
    path("category/delete/<int:pk>/", views.deleteCategory, name="deleteCategory"),

    # FOOD URLS
    path("category/food/create/", views.createFood, name="createFood"),
    path("category/food/update/<int:pk>/", views.updateFood, name="updateFood"), 
    path("category/food/delete/<int:pk>/", views.deleteFood, name="deleteFood"),
]
