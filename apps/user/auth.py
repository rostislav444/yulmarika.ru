from apps.user.models import CustomUser
from apps.security.models import LoginLog
from django.db.models import Q


class UserAuthentication(object):
    def authenticate(self, request, username=None, password=None):
        result = None
        try:     user = CustomUser.objects.get(email=username)
        except : user = None
        if user:
            if user.check_password(password): 
                result = user
        login = LoginLog(username = str(username))
        login.result = True if result else False
        login.save(request)
        return result


    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
