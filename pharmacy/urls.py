from django.urls import path
from . import views
urlpatterns = [
    path('addMedicine',views.addMedicine,name="addMedicine"),
    path('yourMedicine',views.yourMedicine,name="yourMedicine"),
    path('updateMedicine/<int:mid>',views.updateMedicine,name="updateMedicine"),
    path('deleteMedicine/<int:mid>',views.deleteMedicine,name="deleteMedicine"),
    path('acceptOrder/<int:oid>',views.acceptOrder,name="acceptOrder"),
    path('rejectOrder/<int:oid>',views.rejectOrder,name="rejectOrder"),
    path('shipment/<int:oid>',views.shipment,name="shipment"),
    path('yourOrders',views.yourOrders,name="yourOrders")
]