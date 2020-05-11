from django.urls import path
from wiki.views import PageListView, PageDetailView,PageCreateView


urlpatterns = [
    path('', PageListView.as_view(), name='wiki-list-page'),
    path('create/', PageCreateView.as_view(), name='create'),
    path('page/<str:slug>/', PageDetailView.as_view(), name='wiki-details-page'),
]
