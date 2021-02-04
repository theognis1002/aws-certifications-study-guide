from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class LoginMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(
                request,
                "This feature requires you to be logged in. If you do not have an account, please sign up!",
                extra_tags="info",
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)