from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name="user-register"),
    path('account/', user_views.account, name="user-account"),
    #path('account/<str:username>', user_views.ClassView.as_view, name="user-account"), <-- Attemp to turn into class based view
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="user-login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="user-logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset/password_reset.html', 
        html_email_template_name='users/password_reset/password_reset_email.html',
        subject_template_name='users/password_reset/password_reset_email_subject.txt'
        ), 
        name="password_reset"),
    path('password-reset/sent/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset/password_reset_sent.html'), name="password_reset_done"),
    path('password-reset/confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset/password_reset_complete.html'), name="password_reset_complete"),
    path('', include('truckReviews.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)