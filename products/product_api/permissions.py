from rest_framework.permissions import BasePermission

class IsSeller(BasePermission):
    

    def has_permission(self, request, view):
        # Assume `is_seller` is passed in the request data or available in the user object
        user = request.user  # Adjust this to your implementation
        if not user:
            return False  # Deny if user data is missing
        return user.get("is_seller", False)  # Allow if `is_seller` is True

class IsCustomer(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user 
        if not user:
            return False  # Deny if user data is missing
        return not user.get("is_seller", True)  # Allow if `is_seller` is False