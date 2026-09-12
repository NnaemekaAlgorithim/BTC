"""
URL configuration for btc_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import include, path
from btc_backend.admin_site import btc_admin
import btc_backend.auth_admin  # registers Group on btc_admin
import users.admin              # registers User on btc_admin
import tasks.admin              # registers Task, UserTaskCompletion on btc_admin

urlpatterns = [
    path('admin/', btc_admin.urls),
    path('api/users/', include('users.urls')),
    path('api/tasks/', include('tasks.urls')),
]
