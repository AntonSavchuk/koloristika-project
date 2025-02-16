from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewsletterForm
# from .tasks import send_newsletter_task
from .models import Newsletter

@login_required
def create_newsletter(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save()
            return redirect('newsletter:preview_newsletter', newsletter_id=newsletter.id)
    else:
        form = NewsletterForm()

    return render(request, 'newsletter/create_newsletter.html', {'form': form})

@login_required
def preview_newsletter(request, newsletter_id):
    newsletter = Newsletter.objects.get(id=newsletter_id)
    return render(request, 'newsletter/newsletter_preview.html', {'newsletter': newsletter})

@login_required
def edit_newsletter(request, newsletter_id):
    ...
