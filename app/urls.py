from django.urls import path,include, re_path
from . import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', views.redircte, name="redirect"),
    path('login/', views.user_login, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register_user/', views.register_user, name="register_user"),
    path('user/dashboard/', views.dashboard, name="dashboard"),
    path('user/data_upload/', views.upload_data, name="upload_data"),
    path('user/complain/<str:complain>/', views.complain_type, name="complain_type"),
    path('user/rating/', views.rating, name="rating"),
    path('user/trend/', views.trend, name="trend"),
    path('user/sub_type/<str:subtype>/', views.sub_type, name="sub_type"),
    path('user/train_wise_data/', views.train_wise_data, name="train_wise_data"),
    path('user/bottom_train_data_pie_chart/', views.bottom_train_data_pie, name="bottom_train_data_pie"),
    path('user/bottom_train_data_bar_chart/', views.bottom_train_data_bar, name="bottom_train_data_bar"),
    path('user/user_profile/', views.user_profile, name="user_profile"),
    path('user/change_password/change/', views.change_password, name="change_password"),
    path('user/all_complain_train/', views.all_complain_train, name="all_complain_train"),
    path('user/all_sub_complain_train/<str:subtype>/', views.all_sub_complain_train, name="all_sub_complain_train"),
    path('user/max_complain_train/', views.max_complain_train, name="max_complain_train"),
    path('user/min_complain_train/', views.min_complain_train, name="min_complain_coach"),
    path('user/max_complain_coach/', views.max_complain_coach, name="max_complain_coach"),
    path('user/min_complain_coach/', views.min_complain_coach, name="min_complain_coach"),
    path('user/mix_chart/', views.mix_chart, name="mix_chart"),
    path('user/show_staff_name/', views.show_staff_name, name="show_staff_name"),
    path('user/add_staff_name/', views.add_staff_name, name="add_staff_name"),
    path('user/staff_graph/', views.staff_graph, name="staff_graph"),
    path('user/add_train_cat/', views.add_train_cat, name="add_train_cat"),
    path('user/add_staff_csv/', views.add_staff_csv, name="add_staff_csv"),

]
