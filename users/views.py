from django.shortcuts import render, redirect
from .form import RegisterForm
from django.contrib import messages


# Create your views here.
def register(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '注册成功')
            return redirect('/')
    else:
        form = RegisterForm

    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})
