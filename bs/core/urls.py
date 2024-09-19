from django.urls import path
from . import views
from .views import  SearchView, academie, accueille, bitcoin, contact, detailView, BlogListView, equipe, immobilier, informatique, laboratoire, production
urlpatterns = (

    # Général
    path('', accueille, name='accueille'),
    
    # Blog
    path('blog/', BlogListView.as_view(), name="blog"),
    path('detail/<slug:slug>', detailView, name='detailView'),
    path('blog/detail/<slug:slug>', detailView, name='detailView'),
    path('blog/search/', BlogListView.as_view(), name='search'),  
    path('blog/search/', SearchView.as_view(), name='result'),  
    path('cat/<int:id>/', views.ReadCat, name='blog-cat'),

    # Télécharegement des catalogues
    path('download_academie_file/<int:file_id>/', views.download_academie_file, name='download_academie_file'),
    path('download_bitcoin_file/<int:file_id>/', views.download_bitcoin_file, name='download_bitcoin_file'),
    path('download_info_file/<int:file_id>/', views.download_info_file, name='download_info_file'),
    path('download_labo_file/<int:file_id>/', views.download_labo_file, name='download_labo_file'),
    path('download_immobilier_file/<int:file_id>/', views.download_immobilier_file, name='download_immobilier_file'),
    path('download_production_file/<int:file_id>/', views.download_production_file, name='download_production_file'),

    # Service information
    path('bitcoin', bitcoin, name='bitcoin'),
    path('immobilier', immobilier, name='immobilier'),
    path('production', production, name='production'),
    path('laboratoire', laboratoire, name='laboratoire'),
    path('informatique', informatique, name='informatique'),
    path('academie', academie, name='academie'),

    # Correspondance
    path('equipe', equipe, name='equipe'),
    path('message', contact, name='message'),
)

# Test
# http://127.0.0.1:8000/blog/article/blog/detail/c-bon

# http://127.0.0.1:8000/blog/article/recherche?article=Cette
