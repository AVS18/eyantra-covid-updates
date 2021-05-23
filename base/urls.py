from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('contact',views.contact,name="contact"),
    path('login',views.login,name="login"),
    path('validateOtp',views.validateOtp,name="validateOtp"),
    path('setNewPassword',views.setNewPassword,name="setNewPassword"),
    path('changePassword',views.changePassword,name="changePassword"),
    path('logout',views.logout,name="logout"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('cowinSlot',views.cowinSlot,name="cowinSlot"),
    path('getSlotDay',views.getSlotDay,name="getSlotDay"),
    path('getSlotWithDistrict',views.getSlotWithDistrict,name="getSlotWithDistrict"),
    path('notify',views.notify,name="notify")
]