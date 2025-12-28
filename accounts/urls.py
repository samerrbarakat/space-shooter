from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView , LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path("register/",views.register, name="register"),
    path("login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('password_change/', PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='landing'), name='password_change_done'),
    # For now it takes you to landing page, but later it will take you to dashboard page.
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

