from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class LoginMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            register_url = reverse_lazy("register")
            messages.info(
                request,
                f"This feature requires you to be logged in. If you do not have an account, please sign up <a class='text-info' href='{register_url}'>HERE</a>.",
                extra_tags="info",
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
