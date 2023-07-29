from django.contrib import admin
from django.urls import path, include
from . import views
# Include the URLs of your app
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('my_app.urls')),
    path('',views.index,name='index'),
    path('tasks',views.index),

]
