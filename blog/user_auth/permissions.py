from rest_framework.permissions import BasePermission


class IsAllowedToCRUDComments(BasePermission):

    def has_permission(self, request, view):
        # print(view.action)
        if view.action in ['create', 'destroy', 'update', 'partial_update']:
            return request.user.is_admin or request.user.is_simple_user
        return True


class IsAllowedToCRUDUsers(BasePermission):

    def has_permission(self, request, view):
        # print(request.user.role, request.user.role == "M")
        return request.user.is_admin or request.user.is_manager
        # return True

