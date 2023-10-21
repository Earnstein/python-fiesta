from django.urls import path
from . import views

urlpatterns = [
    path('addTask/', views.httpAddTask, name="addTask"),
    path('mark_as_done/<int:id>/', views.mark_As_Done, name='mark_as_done'),
    path('mark_as_undone/<int:id>/', views.mark_As_Undone, name='mark_as_undone'),
     path('edit_task/<int:id>/', views.edit_task, name='edit_task'),
    path('delete_todo/<int:id>/', views.delete_Todo, name='delete_todo'),
]
