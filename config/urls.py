"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from items.views import ItemsViewSet
from members.views import MembersViewSet
from orders.views import OrdersViewSet

router = DefaultRouter()
router.register(r'items', ItemsViewSet, basename='items')
router.register(r'members', MembersViewSet, basename='members')
router.register(r'orders', OrdersViewSet, basename='orders')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
