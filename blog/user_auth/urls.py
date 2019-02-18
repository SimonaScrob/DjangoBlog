from django.conf.urls import url
from django.urls import include

from user_auth import views

urlpatterns = [
    url(r'^login/$', views.user_login_view, name='login'),
    url(r'^logout/$', views.user_logout_view, name='logout'),
    # url(r'^password/reset/$', views.user_password_reset_view, name='password-reset')
    # url(r'^password/reset/email/$', HomePageView.as_view(), name='password-reset-url'),
    # url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
    #     name='password-reset-confirm')
    # url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^registration/', include('rest_auth.registration.urls')),
    # url(r'^registration/', views.user_register_view, name='register'),

]