from django.urls import path
from .views import login_view, logout_view, password_reset_view, otp_verify_view, resend_otp_view, new_password_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', password_reset_view, name='password_reset'),
    path('otp-verify/', otp_verify_view, name='otp_verify'),  # Gunakan ini
    path('resend-otp/', resend_otp_view, name='resend_otp'),
    path('new-password/', new_password_view, name='new_password'),

]
