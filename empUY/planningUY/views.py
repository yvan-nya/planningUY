#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from .token import generatorToken
from empUY import settings

def home(request):
    return render(request, 'planningUY/index.html')

#============================== AUTHENTIFICATION SYSTEM ===========================================
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if User.objects.filter(username=username):
            messages.success(request,'Ce nom d utilisateur existe déjà')
            return redirect('register')
        if User.objects.filter(email=email):
            messages.success(request,'Un utilisateur possède déjà cet email')
            return redirect('register')
        if not username.isalnum():
            messages.success(request, 'Le nom d utilisateur doit être alphanumérique')
            return redirect('register')
        if password != password1:
            messages.success(request,'Attention! Les veillez entrez des mots de passe identiques!')
            return redirect('register')

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.is_active = False

        my_user.save()
     
        # Email de bienvenu
        subject = "Bienvenu sur EmploiUY"
        message = "Bienvenu "+ my_user.first_name +" \n Nous sommes heureux de vous avoir parmi nous\n\n EmploiUY\n\n@www.facsciences-uy1.cm"
        from_email = settings.EMAIL_HOST_USER
        to_email = my_user.email
        mail = send_mail(subject, message, from_email, [to_email], fail_silently=False)

        # Email de confirmation
        current_site = get_current_site(request)
        conf_subject = "Confirmation de l'adresse email sur EmploiUY"
        conf_message = render_to_string("emailconfirm.html", {
            "name":my_user.first_name,
            "domain":current_site,
            "uid":urlsafe_base64_encode(force_bytes(my_user.pk)),
            "token":generatorToken.make_token(my_user)
            })
        email = send_mail(
            conf_subject,
            conf_message,
            from_email,
            [to_email]
        )

        messages.success(request, f'Salut {username}, votre compte a été créé avec succès, Un email de confirmation vous a été envoyé!')
        return redirect('login')
    return render(request, 'planningUY/register.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f"Votre compte a été activé avec succès, Connecter Vous à présent")
        return redirect('login')
    else:
        messages.success(request, f"Activation échoué! Veillez réessayer plus tard!")
        return redirect('home')


def loginU(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            firstname = user.first_name
            return render(request, 'planningUY/base.html', {'firstname':firstname})
        else:
            messages.success(request, f'Entrez vos données correctement!')
            return redirect('login')
    return render(request, 'planningUY/login.html')

def logoutU(request):
    logout(request)
    messages.success(request, f'Vous avez été déconnecté avec success')
    return redirect('home')

#=========================================================================================================