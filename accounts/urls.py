from django.urls import path, include

from django.contrib.auth import views as auth_views # "as auth_views" para serparar das views originais

from . import views

from dash_apps.finished_apps import simpleexample
from dash_apps.finished_apps import mapdash01
from dash_apps.finished_apps import bardash01
from dash_apps.finished_apps import linedash01
from dash_apps.finished_apps import printdashjs
from dash_apps.finished_apps import raddash01

urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('user/', views.userPage, name='user-page'),

    path('account/', views.accountSettings, name='account'),

    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
        name="reset_password"),

    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
    name="password_reset_confirm"), #<uidb64> segurança /<token> para verificar se a senha é válida

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_complete"),

    path('result_assess_html/', views.assessview, name='result_assess_html'),

    path('painel/', views.painel, name='painel'),

    path('django_plotly_dash/', include('django_plotly_dash.urls')),

    path('export_pdf/', views.export_pdf, name='export_pdf'),

]

'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''
