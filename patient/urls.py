from django.urls import path
from . import views
urlpatterns = [
    path('searchMedicine',views.searchMedicine,name="searchMedicine"),
    path('filterMedicine',views.filterMedicine,name="filterMedicine")
]