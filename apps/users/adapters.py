from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
import re


class UCAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False


class UCSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, account):
        return True if re.match(r".+[@\.]p?uc\.cl", user_email(account.user)) else False

    def populate_user(self, request, sociallogin, data):
        user = sociallogin.user
        user.email = data.get("email")
        user.username = user.email.split("@")[0]
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        return user
