from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, ListView

from apps.forms import SignUpForm, LoginForm, ProfileUpdateForm, CustomPasswordChangeForm
from apps.models import CustomUser


class IndexView(View):
    def get(self, request):
        return render(request, 'apps/index.html')


class ProfileView(View):
    def get(self, request):
        return render(request, 'apps/users/profile-page.html')



class UserPostsView(View):
    def get(self, request):
        return render(request, 'apps/user_posts_page.html')


class SignupView(CreateView):
    template_name = 'apps/auth/signup_page.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('profile_page')
    form_class = SignUpForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile_page')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Account created successfully!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class LoginView(FormView):
    template_name = 'apps/auth/login_page.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index_page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.user)
        messages.success(self.request, 'Successfully logged in!')

        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return redirect(next_url)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Login failed. Please check your credentials.')
        return super().form_invalid(form)


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
        return redirect('index_page')

    def post(self, request):
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
        return redirect('index_page')


class ProfileUpdateView(LoginRequiredMixin, FormView):
    template_name = 'apps/users/profile-page.html'
    form_class = ProfileUpdateForm

    def get_form(self, form_class=None):
        return self.form_class(instance=self.request.user, **self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if 'update_profile' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile_page')
            else:
                print("Form is not valid. Errors:", form.errors.as_json())
                messages.error(request, 'Please correct the errors below.')

        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('profile_page')
            else:
                messages.error(request, 'Please correct the password errors.')

        return render(request, self.template_name, {'form': form, 'password_form': password_form})

class UserListView(LoginRequiredMixin, ListView):
    queryset = CustomUser.objects.all()
    template_name = 'apps/users/users_list_page.html'
    context_object_name = 'users'

    def get_queryset(self):
        return CustomUser.objects.all()[:10]