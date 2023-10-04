from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . forms import LoginForm , MyPassChange


urlpatterns = [
    path('registrations/', views.UserRegiForm.as_view(), name="userRegiForm"),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html',authentication_form= LoginForm), name='login'),

    # change password
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='account/changepassword.html', form_class = MyPassChange, success_url = '/account/passwordchangedone/'), name='changepassword'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html', ), name='passwordchangedone'),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'login'), name='logout'),

        
    path('profile/', views.profile, name="profile")
]
