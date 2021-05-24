from django.urls import path
from . import views
urlpatterns = [
    path('searchMedicine',views.searchMedicine,name="searchMedicine"),
    path('filterMedicine',views.filterMedicine,name="filterMedicine"),
    path('placeOrder/<int:mid>',views.placeOrder,name="placeOrder"),
    path('yourOrders',views.yourOrder,name="yourOrder"),
    path('cancelOrder/<int:oid>',views.cancelOrder,name="cancelOrder")
]