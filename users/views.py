from django.shortcuts import render
from allauth.account.views import LoginView
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    return render(request, "account/profile.html")

class CustomLoginVew(LoginView):
    def form_valid(self, form):
        remember = self.request.POST.get("remember", False)
        if remember:
            self.request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)
    

