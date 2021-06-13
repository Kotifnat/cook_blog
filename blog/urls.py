from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/<slug:post_slug>', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/', views.PostListView.as_view(), name='post_list'),
    path('', views.home),
]
