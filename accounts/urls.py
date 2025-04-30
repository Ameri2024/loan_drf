from django.urls import path, re_path
from . import views
from .view.jwt import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'accounts'

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    # # your existing views...
    path('register/', views.RegisterUserAPIView.as_view(), name='register_api'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change/password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('user/list', views.UsersList.as_view(), name='users_list'),
    re_path(r'^details/(?P<national_code>[0-9]{10})/$', views.UserDetailsView.as_view(), name='detail'),
    re_path(r'^update/(?P<national_code>[0-9]{10})/$', views.UpdateUserView.as_view(), name='update_user'),
    re_path(r'^delete/(?P<national_code>[0-9]{10})/$', views.DeleteUserView.as_view(), name='delete_user'),



]



