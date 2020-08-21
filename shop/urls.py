from django.urls import path

from . import views


app_name = 'shop'

urlpatterns = [
    path('detail/<slug:slug>/<int:pk>', views.detail_view, name="detail"),
    path('category/<slug:slug>/', views.list_view, name='category_list'),
    path('', views.list_view, name='list'),
]
