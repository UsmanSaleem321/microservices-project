from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    """
    Custom permission to allow only customers (non-sellers) to access a view.
    """
    def has_permission(self, request, view):
        user = request.user 
        if not user:
            return False  # Deny if user data is missing
        return not user.get("is_seller", True)  # Allow if `is_seller` is False

from rest_framework.permissions import BasePermission

class IsSeller(BasePermission):
    """
    Custom permission to allow only sellers to add, delete, or edit products.
    """

    def has_permission(self, request, view):
        # Assume `is_seller` is passed in the request data or available in the user object
        user = request.data.get("user")  # Adjust this to your implementation
        if not user:
            return False  # Deny if user data is missing
        return user.get("is_seller", False)  # Allow if `is_seller` is True
