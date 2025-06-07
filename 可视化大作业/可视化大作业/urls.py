"""
URL configuration for 可视化大作业 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from homestay import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('area_count/', views.area_count, name='area_count'),
    path('fav_consume_relation/', views.fav_consume_relation, name='fav_consume_relation'),
    path('price_distribution/', views.price_distribution, name='price_distribution'),
    path('booking_trend/', views.booking_trend, name='booking_trend'),
    path('room_type_proportion/', views.room_type_proportion, name='room_type_proportion'),
    path('multi_dimension/', views.multi_dimension_analysis, name='multi_dimension'),
    path('geo_distribution/', views.geo_distribution, name='geo_distribution'),
    
    # API路由
    path('api/area_count/', views.api_area_count, name='api_area_count'),
    path('api/price_distribution/', views.api_price_distribution, name='api_price_distribution'),
    path('api/room_type/', views.api_room_type, name='api_room_type'),
    path('api/tag_count/', views.api_tag_count, name='api_tag_count'),
]
