from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Response, Subscription, Newsletter
from .forms import PostForm, ResponseForm, SubscriptionForm
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from .utils import send_status_change_notification, send_response_notification
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User

def post_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'ads/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        response_form = ResponseForm(request.POST)
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.post = post
            response.author = request.user
            response.save()
            send_response_notification(response)
            return redirect('post_detail', pk=post.pk)
    else:
        response_form = ResponseForm()

    context = {'post': post, 'response_form': response_form, 'responses': post.responses.all()}
    return render(request, 'ads/post_detail.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'ads/post_create.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden("Вы не являетесь автором этого объявления.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'ads/post_edit.html', {'form': form, 'post': post})

@login_required
def response_list(request):
    user_responses = Response.objects.filter(author=request.user)
    context = {'responses': user_responses}
    return render(request, 'ads/response_list.html', context)

@login_required
def change_response_status(request, pk, status):
    response = get_object_or_404(Response, pk=pk)
    if request.user != response.post.author:
        return HttpResponseForbidden("Вы не являетесь автором объявления.")

    if status not in ['accepted', 'rejected']:
        return HttpResponseBadRequest("Неверный статус отклика.")

    response.status = status
    response.save()
    send_status_change_notification(response)
    return redirect('response_list')

@login_required
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect('/')
    else:
        form = SubscriptionForm()
    return render(request, 'ads/subscribe.html', {'form': form})

@login_required
def send_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        subscriptions = Subscription.objects.filter(newsletter=newsletter)
        for subscription in subscriptions:
            subject = newsletter.subject
            message = render_to_string('ads/newsletter_email.html', {'newsletter': newsletter})
            from_email = 'maximssshepelev@yandex.ru'
            recipient_list = [subscription.user.email]
            send_mail(subject, message, from_email, recipient_list)
        newsletter.sent_at = timezone.now()
        newsletter.save()
        return redirect('/')

    return render(request, 'ads/send_newsletter.html', {'newsletter': newsletter})

def confirm_email(request, code):
    user = get_object_or_404(User, registration_code=code)
    user.is_active = True
    user.registration_code = ''
    user.save()
    return render(request, 'ads/email_confirmed.html')