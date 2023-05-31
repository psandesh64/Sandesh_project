"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import home,todo,todoedit,tododelete,handlelogin,handlelogout,handlesignup,image_page,image_del_page

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('todo/',todo,name='todo'),
    path('login/',handlelogin,name='login'),
    path('logout/',handlelogout,name='logout'),
    path('signup/',handlesignup,name='signup'),
    path('todoedit/<str:id>/',todoedit,name='todoedit'),
    path('tododelete/<str:id>/',tododelete,name='tododelete'),
    path('images/',image_page,name='images'),
    path('imagedel/',image_del_page,name='imagedel'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
