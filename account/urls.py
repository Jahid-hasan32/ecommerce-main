from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . forms import LoginForm , MyPassChange, MyPassResetForm, MySetPassForm


urlpatterns = [
    path('registrations/', views.UserRegiForm.as_view(), name="userRegiForm"),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html',authentication_form= LoginForm), name='login'),

    # change password
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='account/changepassword.html', form_class = MyPassChange, success_url = '/account/passwordchangedone/'), name='changepassword'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html', ), name='passwordchangedone'),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'login'), name='logout'),
    
    #reset password.
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'account/password_reset.html', form_class = MyPassResetForm, ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'account/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html', form_class = MySetPassForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'account/password_reset_complete.html'), name='password_reset_complete'),
    
        
    path('profile/', views.profile, name="profile")
]
