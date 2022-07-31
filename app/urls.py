from django.urls import path,include
from . import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', views.redircte, name="redirect"),
    path('user/fill_data/', views.fill_data, name="fill_data"),
    path('login/', views.user_login, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register_user/', views.register_user, name="register_user"),
    path('user/dashboard/', views.dashboard, name="dashboard"),
    path('user/data_upload/', views.upload_data, name="upload_data"),
    path('user/complain/<str:complain>/', views.complain_type, name="complain_type"),
    path('user/rating/', views.rating, name="rating"),
    # path('register_individual/', views.register_individual, name="register_individual"),
    # path('user/forget_password/', views.forget_password, name="forget_password"),
    # path('user/user_detail/user_profile/', views.user_detail, name="user_detail"),
    # path('user/user_detail/user_profile/edit/', views.edit_profile, name="user_detail"),
    # path('user/premium_purchase/', views.premium_purchase, name="premium_purchase"),
    # path('user/paymentstatus/', views.paymentstatus, name="paymentstatus"),
    # path('user/voltage_data/', views.voltage_data, name="voltage_data"),
    # path('user/voltage_chart/', views.voltage_chart, name="voltage_chart"),
    # path('user/voltage_chart/search_by_month/<int:month_num>/<int:year>/', views.voltage_search_by_month, name="voltage_data_month")
]
