from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse
from .utils import get_user_details
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
			try:
				send_mail(
					subject,
					message,
					EMAIL_HOST_USER,
					[recepient],
					fail_silently=False
				)				
				messages.success(request, f"New password send to {email}.")
			except:
				messages.error(request, f"New password unable to send to {email}. Plz Contact EC.")
		else:
			messages.error(request, "input invalid")
	else:
		context['form'] = form
		context['user'] = get_user_details(request)
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

			election_time = Election_Coordinator.objects.values('start_time','end_time').first()
			start_time =election_time['start_time']
			end_time =election_time['end_time']

			if login_type == '1':
				if start_time and not end_time:
					# checking whether election is currently  ongoing or not
					rollno = username
					try:
						voter = Voter.objects.get(pk=rollno)

						if password == voter.password:
							request.session['voter'] = rollno
							request.session['is_authenticated'] = True
							request.session.set_expiry(30000)
											
							return redirect('election:home')
						else:
							messages.error(request, "Password incorrect")
					except:
						messages.error(request, "Voter not found in Database")
				elif start_time and end_time:
					messages.success(request, "Election Over. No need to login")
					return redirect('result')
				else:
					messages.error(request, "Election NOT started yet")
					return redirect('index')

			elif login_type == '2':
				if not start_time:
					# login for candidate only available before election start.
					rollno = username
					try:
						candidate = Candidate.objects.get(voter__rollno=rollno)

						if password == candidate.voter.password:
							request.session['candidate'] = rollno
							request.session['is_authenticated'] = True
							request.session.set_expiry(300)
							
							return redirect('election:home')
						else:
							messages.error(request, "Password incorrect")
					except:
						messages.error(request, "Candidate not found in Database")
				else:
					messages.error(request, "Election Started, So can't edit your manifesto")

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
		'user' : get_user_details(request),
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


