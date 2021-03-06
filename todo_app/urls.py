from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:id>/delete/', views.delete, name='delete'),
    # path('todo/<str:category>/', views.todo_category, name='todo_category'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('category_list/', views.category_list, name='category_list'),
    path('user_data_input/', views.user_data_input, name='user_data_input'),
    path('user_data_confirm', views.user_data_confirm, name='user_data_confirm'),
    path('user_data_create', views.user_data_create, name='user_data_create'),
    # path('user_list', views.UserList.as_view(), name='user_list'),
    path('create_category_input', views.create_category_input, name='create_category_input'),
    path('create_category_confirm', views.create_category_confirm, name='create_category_confirm'),
    path('create_category_save', views.create_category_save, name='create_category_save'),
    # ToDoを作る
    path('create_todo_input', views.create_todo_input, name='create_todo_input'),
    path('create_todo_confirm', views.create_todo_confirm, name='create_todo_confirm'),
    path('create_todo_save', views.create_todo_save, name='create_todo_save'),
    path('todo_list/<int:pk>', views.todo_list, name='todo_list'),
]
