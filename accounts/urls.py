from django.urls import path

from .import views

# importing auth_views for password reset
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='product'),
    path('customers/<str:cust_id>/', views.customers, name='customer'),
    path('create_order/<str:pk>', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('login/', views.loginPage, name='login'),
    path('signup/', views.signupPage, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name='user_page'),
    path('account/', views.accountSettings, name="account"),

    #submit email form
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name="reset_password"),

    #Email Sent Success Message
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), 
        name='password_reset_done'),

    #Link to password reset form in email
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), 
        name="password_reset_confirm"),

    #password change success message
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
         name="password_reset_complete"),


]