from django.http import HttpResponseForbidden
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden(
                    "You are not authorized to access this page."
                )

            if request.user.role not in allowed_roles:
                return HttpResponseForbidden(
                    "You do not have permission to perform this action."
                )

            # Add user information to the request (optional)
            request.user_info = {
                "username": request.user.username,
                "role": request.user.role,
            }

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
