from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import viewsets

from core import settings
from .forms import DoublePasswordRegisterForm, CustomAuthenticationForm
from .models import CustomUser
from .serializers import UserSerializer
from .utils import custom_get_success_url, login_as_demo_user


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class SignUpView(generic.CreateView):
    form_class = DoublePasswordRegisterForm
    # form_class = SinglePasswordRegisterForm
    template_name = 'users/signup.html'
    redirect_authenticated_user = True

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return custom_get_success_url(self.request)

    def form_valid(self, form):
        form.save()

        username = form.cleaned_data.get('username')

        if self.form_class == DoublePasswordRegisterForm:
            password = form.cleaned_data.get('password1')
        else:
            password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return custom_get_success_url(self.request)

    def get(self, request, *args, **kwargs):
        if request.GET.get('demo') and settings.IS_DEMONSTRATION_MODE:
            if login_as_demo_user(request):
                return HttpResponseRedirect(self.get_success_url())

        return super().get(request, *args, **kwargs)


class CustomLogoutView(LogoutView):
    def get_next_page(self):
        return custom_get_success_url(self.request)
