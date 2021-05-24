from django.urls import path
from . import views
urlpatterns = [
    path('searchMedicine',views.searchMedicine,name="searchMedicine"),
    path('filterMedicine',views.filterMedicine,name="filterMedicine"),
    path('placeOrder/<int:mid>',views.placeOrder,name="placeOrder"),
    path('yourOrders',views.yourOrder,name="yourOrder"),
    path('cancelOrder/<int:oid>',views.cancelOrder,name="cancelOrder"),
    path('MedicalReport',views.yourMedicalReport,name="MedicalReport"),
    path('attachReport',views.attachReport,name="attachReport"),
    path('viewDoctor',views.viewDoctor,name="viewDoctor"),
    path('bookAppointment/<int:did>',views.bookAppointment,name="bookAppointment"),
    path('viewAppointment',views.viewAppointment,name="viewAppointment"),
    path('viewConsultation/<int:cid>',views.viewConsultation,name="viewConsultation"),
    path('yourBill',views.yourBill,name="yourBill")
]