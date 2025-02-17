from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import NewsletterForm
# from .tasks import send_newsletter_task
from .models import Newsletter

@login_required
def create_newsletter(request):
    if not request.user.is_superuser:
        return redirect('main:index')

    if request.method == "POST":
        form = NewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            newsletter = form.save(commit=False)


            if not newsletter.font_size:
                newsletter.font_size = 16
            
            if not newsletter.text_color:
                newsletter.text_color = "#000000"

            newsletter = form.save()
            print(f"Newsletter {newsletter.id} saved successfully!")
            return redirect('newsletter:newsletter_list')
        else:
            print("Form is not valid:", form.errors) 
    else:
        form = NewsletterForm()

    return render(request, 'newsletter/create_newsletter.html', {'form': form})

@login_required
def preview_newsletter(request, newsletter_id):
    newsletter = Newsletter.objects.get(id=newsletter_id)
    return render(request, 'newsletter/newsletter_preview.html', {'newsletter': newsletter})

@login_required
def edit_newsletter(request, newsletter_id):
    if not request.user.is_superuser:
        return redirect('main:index')

    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    if request.method == "POST":
        form = NewsletterForm(request.POST, request.FILES, instance=newsletter)
        if form.is_valid():
            form.save()
            return redirect('newsletter:preview_newsletter', newsletter_id=newsletter.id)
    else:
        form = NewsletterForm(instance=newsletter)

    context = {
        'form': form,
        'newsletter': newsletter,
    }

    return render(request, 'newsletter/edit_newsletter.html', context)

@login_required
def delete_newsletter(request, newsletter_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Доступ запрещен'}, status=403)

    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    if request.method == "POST":
        newsletter.delete()
        return JsonResponse({'success': True, 'message': 'Рассылка удалена!'})

    return JsonResponse({'error': 'Неверный метод'}, status=400)

@login_required
def newsletter_list(request):
    if not request.user.is_superuser:
        return redirect('main:index')
    
    newsletters = Newsletter.objects.all().order_by('-created_at')
    context = {
        'newsletters': newsletters
    }
    return render(request, 'newsletter/newsletter_list.html', context)