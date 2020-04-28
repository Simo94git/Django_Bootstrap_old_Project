from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from accounts.forms import Form_di_Registrazione

# Create your views here.

def registrazioneView(request):
    if request.method == 'POST':
        form = Form_di_Registrazione(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            User.objects.create_user(username=username, email=email, password=password )
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")

    else:
        form = Form_di_Registrazione()

    context = {"form": form}
    return render(request, "registrazione.html", context)
