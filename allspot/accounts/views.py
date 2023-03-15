from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.

def registerUser(request):
    if request.method =='POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            #password = form.cleaned_data['password']
            #user = form.save(commit=False)
            #user.set_password(password)
            #user.role = User.CUSTOMER
            #form.save()
            #return redirect('registerUser')

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name, last_name=last_name, username=username, email=email, phone_number=phone_number, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'A tua conta foi criada com sucesso.')

            return redirect('registerUser')
        else:
            print('Formulário mal preenchido.')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)

