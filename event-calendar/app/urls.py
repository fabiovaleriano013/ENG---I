from django.urls import path    
from .views import *


urlpatterns = [
    path("", index, name="index"),
    path('contato/', contato, name='contato'),
    path('contato/create/', create_contato, name='create_contato'),# type: ignore
    path('contato/update/<int:id>/', update_contato, name='update_contato'),# type: ignore
    path('contato/delete/<int:id>/', delete_contato, name='delete_contato'),# type: ignore
    
]