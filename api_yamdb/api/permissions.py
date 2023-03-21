from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        safe = request.method in permissions.SAFE_METHODS
        if request.user.is_authenticated:
            return safe or request.user.is_admin
        return safe


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == "GET"


class AdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsUserAnonModerAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return (request.user == obj.author)

        safe = request.method in permissions.SAFE_METHODS
        if request.user.is_authenticated:
            admin_or_author = (
                request.user.is_admin
                or request.user == obj.author
            )
            return safe or admin_or_author
        return safe


class IsAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
