from django.contrib.auth import authenticate, logout, login


class ApplicationService(object):
    @classmethod
    def authenticate(cls, request, username, password):
        user = authenticate(username=username, password=password)

        if user is None:
            raise Exception('The username and password were incorrect.')
        elif not user.is_active:
            raise Exception('Your account has been disabled.')

        # login(request, user)
