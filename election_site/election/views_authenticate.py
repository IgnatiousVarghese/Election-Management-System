from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from election_site.settings import EMAIL_HOST_USER
from .models import *
from .forms import *
import random


def get_password(request):
	context = {}
	form = password_change()
	if request.method == 'POST':
		form = password_change(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = random.randint(1, 10000)
			voters = Voter.objects.filter(email=email)
			if len(voters) < 1:
				messages.error(request, "Voter not Database")
				context['form'] = form
				return render(request, 'account/get_password.html', context)
			voter = voters[0]
			voter.password = password
			try:
				voter.save()
				messages.success(request, f"Password of {voter.rollno} changed.")
			except:
				messages.error(request, "Password unable to change.")

			subject = 'Password Changed'
			message = 'New password is {0}'.format(password)
			recepient = str(email)
			send_mail(
				subject,
				message,
				EMAIL_HOST_USER,
				[recepient],
				fail_silently=False
			)
		else:
			messages.error(request, "input invalid")
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
				rollno = username
				try:
					voter = Voter.objects.get(pk=rollno)

					if password == voter.password:
						request.session['voter'] = rollno
						request.session['is_authenticated'] = True
						request.session.set_expiry(30000)
						messages.success(request, "successfully logged in as Voter")				
						return redirect('election:home')
					else:
						messages.error(request, "Password incorrect")
				except:
					messages.error(request, "Voter not found in Database")

			elif login_type == '2':
				rollno = username
				try:
					candidate = Candidate.objects.get(voter__rollno=rollno)

					if password == candidate.voter.password:
						request.session['candidate'] = rollno
						request.session['is_authenticated'] = True
						request.session.set_expiry(300)
						messages.success(request, "successfully logged in as Candidate")
						return redirect('election:home')
					else:
						messages.error(request, "Password incorrect")
				except:
					messages.error(request, "Candidate not found in Database")

			elif login_type == '3':
				try:
					ec = Election_Coordinator.objects.get(
						username=username
						)
					print(username)
					if password == ec.password:
						request.session['election_cordinator'] = username
						request.session['is_authenticated'] = True
						request.session.set_expiry(300)
						messages.success(request, "successfully logged in as EC")
						return redirect('election:home')
					else:
						messages.error(request, "Password incorrect")
				except:
					messages.error(request, "EC not found in Database")
			
			else:
				messages.error(request, "Login type not accepted")

		else:
			messages.error(request, "Form input not valid")

	context = {
		'form': form
	}
	return render(request, 'account/login.html', context=context)


def logout(request):
	if request.method == "GET":
		if request.session.has_key('is_authenticated'):
			del request.session['is_authenticated']
		if request.session.has_key('voter'):
			del request.session['voter']
		if request.session.has_key('candidate'):
			del request.session['candidate']
		if request.session.has_key('election_cordinator'):
			del request.session['election_cordinator']
		
	return redirect('index')


