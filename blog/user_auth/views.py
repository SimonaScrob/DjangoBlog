from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_auth.views import LoginView, LogoutView
from rest_auth.registration.views import RegisterView

from user_auth.models import User
from user_auth.permissions import IsAllowedToCRUDUsers
from user_auth.serializers import UserSerializer


class UserLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        response = self.logout(request)
        return self.finalize_response(request, response, *args, **kwargs)


# class UserPasswordResetAPIView(rest_auth_views.PasswordResetView):
#     serializer_class = UserPasswordResetSerializer


class UserLoginView(LoginView):
    authentication_classes = ()

    def login(self):
        super(UserLoginView, self).login()
        return self.get_response()

    def get_response(self):
        context = {
                   'data': UserSerializer(instance=self.user).data
                  }

        return Response(context, status=status.HTTP_200_OK)


class UserRegisterView(RegisterView):
    authentication_classes = ()


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAllowedToCRUDUsers, IsAuthenticated, )


user_login_view = UserLoginView.as_view()
user_logout_view = UserLogoutView.as_view()
# user_register_view = UserRegisterView.as_view()
# user_password_reset_view = UserPasswordResetAPIView.as_view()
