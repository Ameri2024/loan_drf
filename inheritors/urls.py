from django.urls import path
from . import views

app_name = 'inheritors'

urlpatterns = [
    path('', views.ManageInheritors.as_view(), name='inherit'),
    path('create/', views.CreateInheritor.as_view(), name='inherit-create'),
    path('update/<int:id>/', views.UpdateInheritorsView.as_view(), name='update_inherit'),
    path('delete/<int:id>/', views.DeleteInheritorsView.as_view(), name='delete_inherit'),
]
