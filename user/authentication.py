#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.contrib.auth.models import User


class EmailAuthBackend:
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, email=None, password=None):
        """
        Get user with his email
        """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Returns user
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
