from django.contrib.auth.backends import BaseBackend

from .models import User

class ODLBackend(BaseBackend):
    
    def authenticate(self, request, username, password):
        
        if username is None or password is None:
            return None
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
            
            if user.check_password(raw_password=password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None