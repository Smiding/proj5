from django.urls import path
from .views import user_register, user_login, TaskListCreateView, TaskDetailView, CategoryListCreateView, CategoryDetailView, TasksCreatedByUser, get_user_categories, delete_user, user_detail

urlpatterns = [
    path('register/', user_register, name='user-register'),
    path('login/', user_login, name='user-login'),

    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('tasks/user/<int:user_id>/', TasksCreatedByUser.as_view(), name='tasks_created_by_user'),
    path('categories/user/<int:user_id>/', get_user_categories, name='user_categories'),
    path('delete_user/<int:user_id>/', delete_user, name='user-delete'),
    path('user/<int:user_id>/', user_detail, name='user-delete'),
]
