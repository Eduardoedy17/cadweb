from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categoria/', views.categoria, name="categoria"),
    path('categoria/form/', views.form_categoria, name="form_categoria"),
    path('categoria/editar/<int:id>/', views.editar_categoria, name="editar_categoria"),
    path('categoria/excluir/<int:id>/', views.excluir_categoria, name="excluir_categoria"),
]