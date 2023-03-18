from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied



# Restringir o vendedor de ter acesso à página dos clientes

def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restringir o cliente de ter acesso à página dos vendedores
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'O utilizador já têm a conta iniciada.')
        return redirect('dashboard')
    elif request.method =='POST':
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
            email = form.cleaned_data['email']
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

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'O utilizador já têm a conta iniciada.')
        return redirect('dashboard')
    elif request.method == 'POST':
        # Store the data and create user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST)
        # se o form tiver ficheiros o código é o seguinte:
        #v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name, last_name=last_name, username=username, email=email, phone_number=phone_number, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'A tua conta foi registada com sucesso. Por favor aguarde pela sua aprovação.')
            return redirect('registerVendor')
        else:
            print('Formulário é inválido')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'O utilizador já têm a conta iniciada.')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login efetuado com sucesso.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Os dados foram mal inseridos.')
            return redirect('login')
        
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


def logout(request):
    auth.logout(request)
    messages.info(request, 'Saíste da conta com sucesso.')
    return redirect('login')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custoDashboard(request):
    return render (request, 'accounts/custoDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render (request, 'accounts/vendorDashboard.html')

