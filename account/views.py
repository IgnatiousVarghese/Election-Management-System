from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from election.settings import EMAIL_HOST_USER
from .models import *
from .forms import *
import random


def get_password(request):
    context={}
    form = password_change()
    if request.method == 'POST':
        form = password_change(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = random.randint(1, 10000)
            voters = Voter.objects.filter(email=email)
            if len(voters) < 1:
                context['error'] = "email not in database"
                context['form'] = form
                return render(request, 'account/get_password.html', context)
            voter = voters[0]
            voter.password = password
            voter.save()

            subject = 'Password Changed'
            message = 'new password is {0}'.format(password)
            recepient = str(email)
            send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                [recepient],
                fail_silently=False
            )
        else:
            context['error'] = "input invalid"
    else:
        context['form'] = form
        return render(request, 'account/get_password.html', context)
    return redirect('login')


def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_type = form.cleaned_data['login_type']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if login_type == '1':
                voter = Voter.objects.filter(pk=username)
                if len(voter) < 1:
                    return HttpResponse("Voter not found")

                if password == voter[0].password:
                    request.session['voter'] = username
                    request.session.set_expiry(300)
                    return redirect('home')
                else:
                    return HttpResponse(" password incorrect")

            if login_type == '2':
                voter = Voter.objects.filter(pk=username)
                if len(voter) < 1:
                    return HttpResponse("Voter not found")
                candidate = Candidate.objects.filter(pk=username)
                if len(candidate) < 1:
                    return HttpResponse("candidate not found")

                if password == candidate[0].voter.password:
                    request.session['candidate'] = username
                    request.session.set_expiry(300)
                    return redirect('home')
                else:
                    return HttpResponse(" password incorrect")

            if login_type == '3':
                cordinators = Election_Coordinator.objects.filter(
                    username=username)
                if len(cordinators) < 1:
                    return HttpResponse("cordinators not found")

                if password == cordinators[0].password:
                    request.session['election_cordinator'] = username
                    request.session.set_expiry(300)
                    return redirect('home')
                else:
                    return HttpResponse(" password incorrect")

        else:
            return HttpResponse(request)

    context = {
        'form': form
    }
    return render(request, 'account/login.html', context=context)


def logout(request):
    if request.method == "GET":
        if request.session.has_key('voter'):
            del request.session['voter']
        if request.session.has_key('candidate'):
            del request.session['candidate']
        if request.session.has_key('election_cordinator'):
            del request.session['election_cordinator']
    return redirect('home')
