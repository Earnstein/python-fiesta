from django.urls import path
from . import views
from accounts import views as acct_views


urlpatterns = [
    path("profile/", views.profileView, name="vendorProfile"),
    path("", acct_views.httpVendorDashboard, name="vendorDashboard"),

    # CATEGORIES URLS
    path("menu/", views.menuView, name="menu"),
    path("menu/category/<int:pk>/", views.getCategory, name="getCategory"),
    path("menu/category/create/", views.createCategory, name="createCategory"),
    path("menu/category/update/<int:pk>/", views.updateCategory, name="updateCategory"),
    path("menu/category/delete/<int:pk>/", views.deleteCategory, name="deleteCategory"),
]
