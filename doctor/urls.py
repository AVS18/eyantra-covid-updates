from django.urls import path
from . import views
urlpatterns = [
    path('searchMedicine',views.searchMedicine,name="searchMedicine"),
    path('filterMedicine',views.filterMedicine,name="filterMedicine"),
    path('placeOrder/<int:mid>',views.placeOrder,name="placeOrder"),
    path('yourOrders',views.yourOrder,name="yourOrder"),
    path('cancelOrder/<int:oid>',views.cancelOrder,name="cancelOrder"),
    path('addDoctorProfile',views.addDoctorProfile,name="addDoctorProfile"),
    path('viewAppointment',views.viewAppointment,name="viewAppointment"),
    path('openAppointment/<int:aid>',views.openAppointment,name="openAppointment"),
    path('closeAppointment/<int:aid>',views.closeAppointment,name="closeAppointment"),
    path('viewConsultation/<int:cid>',views.viewConsultation,name="viewConsultation"),
    path('editConsultation/<int:cid>',views.editConsultation,name="editConsultation"),
    path('addMedicine',views.addMedicine,name="addMedicine"),
    path('rejectAppointment/<int:aid>',views.rejectAppointment,name="closeAppointment"),
    path('addTips',views.addTips,name="addTips")
]