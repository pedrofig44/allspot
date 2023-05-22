
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from vendor.models import Vendor


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
        return redirect('custoDashboard')
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

            # Send verification email
            mail_subject = 'Por favor ative a sua conta.'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'A tua conta foi criada com sucesso. Por favor verifique o seu e-mail e ative a sua conta.')

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
        return redirect('vendorDashboard')
    elif request.method == 'POST':
        # Store the data and create user
        form = UserForm(request.POST)
        # v_form = VendorForm(request.POST)
        # se o form tiver ficheiros o código é o seguinte:
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
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
            # Send verification email
            mail_subject = 'Por favor ative a sua conta.'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'A tua conta foi registada com sucesso. Por favor aguarde pela sua aprovação.')
            return redirect('registerVendor')
        else:
            print('Formulário é inválido')
            print(form.errors)
            print(v_form)
            
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'A sua conta está ativada. Bem-Vindo.')
        return redirect('myAccount')
    else:
        messages.error(request, 'O link de ativação é inválido.')
        return redirect('myAccount')

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
    vendor = Vendor.objects.get(user=request.user)
    context = {
        'vendor': vendor,
    }
    return render (request, 'accounts/vendorDashboard.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            #send reset password email
            mail_subject = 'Reinicia a sua password.'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Um link para reiniciar a sua password foi enviado para o seu email.')
            return redirect('login')
        else:
            messages.error(request, 'O mail não corresponde a uma conta.')
            return redirect('login')

    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    # validate the user by the decoding token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Por favor reinicie a sua password.')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired.')
        return redirect('myAccount')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password foi alterada com sucesso.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords não são iguais.')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')


