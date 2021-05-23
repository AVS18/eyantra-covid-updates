from django.urls import path
from . import views
urlpatterns = [
    path('addMedicine',views.addMedicine,name="addMedicine"),
    path('yourMedicine',views.yourMedicine,name="yourMedicine"),
    path('updateMedicine/<int:mid>',views.updateMedicine,name="updateMedicine"),
    path('deleteMedicine/<int:mid>',views.deleteMedicine,name="deleteMedicine")
]