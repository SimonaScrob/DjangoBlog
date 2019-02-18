from rest_framework import serializers

from user_auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("pk", "first_name", "last_name", "username", "email")


# class UserPasswordResetSerializer(PasswordResetSerializer):
#     password_reset_form_class = UserPasswordResetForm
#
#     def validate_email(self, value):
#         if not User.objects.filter(email=value).first() and \
#                 not User.objects.filter(email=lower(value)).first():
#             raise serializers.ValidationError('No registered user found on %s' % value)
#         if not User.objects.filter(email=value).first():
#             value = lower(value)
#         return super(UserPasswordResetSerializer, self).validate_email(value)
#
#
# class UserPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
#     def save(self):
#         return self.set_password_form.save()
