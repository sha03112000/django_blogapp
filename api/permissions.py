
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

# class StaticTokenPermission(BasePermission):
#     STATIC_ACCESS_TOKEN = "static_token"

#     def has_permission(self, request, view):
#         token = request.headers.get('X-STATIC-TOKEN')
#         if token == self.STATIC_ACCESS_TOKEN:
#             return True
#         raise PermissionDenied("Invalid or missing static token.")

class StaticTokenPermission(BasePermission):
    STATIC_ACCESS_TOKEN = "static_token"

    def has_permission(self, request, view):
        token = request.headers.get('X-STATIC-TOKEN')
        return token == self.STATIC_ACCESS_TOKEN
