from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from .utils import get_user_details
from .models import *
from .forms import AddCandidateForm, AddPost
from datetime import datetime


def home(request):
    USER = get_user_details(request)
    if USER['is_authenticated'] == False:
        return HttpResponse("you are not supposed to be here LOL get lost!!!!!!")

    elif(USER['account_type'] == 'Voter'):
        return voter_home(request, USER)

    elif USER['account_type'] == 'Candidate':
        return candidate_home(request, USER)

    elif USER['account_type'] == 'Election_Coordinator':
        return election_coordinator_home(request, USER)

    return HttpResponse("you are not supposed to be here LOL get lost!!!!!!")


def voter_home(request, voter):
    context = {
        'user': voter,
        'posts': Post.objects.all(),
        'candidates': Candidate.objects.all(),
    }

    return render(request, 'voter/home.html', context)


def view_post(request, idpost):
    voter = get_user_details(request)
    try:
        post = Post.objects.get(pk=idpost)
        candidates = Candidate.objects.filter(post_applied=post)
    except:
        return HttpResponse("Post not present")

    info = {
        post: voter['my_votes_info'][post]
    }
    context = {
        'user': voter,
        'info': info,
    }
    return render(request, 'voter/view_post.html', context)


def vote(request, idpost, idcandidate):
    voter = get_user_details(request)
    if voter['is_authenticated'] and (voter['account_type'] == 'Voter') and request.method == 'POST':
        try:
            candidate = Candidate.objects.get(voter_id=idcandidate)
            post = Post.objects.get(pk=idpost)
            already_voted = Vote.objects.filter(
                voter=voter['voter']).filter(post=post)
            if already_voted.exists():
                already_voted[0].delete()
            voter_vote = Vote(voter=voter['voter'],
                              candidate=candidate, post=post)
            print(voter_vote)
            voter_vote.save()
        except:
            return HttpResponse("Some problem with Database\n plz contact admin.")

    return redirect('election:view_post', idpost)


def candidate_home(request, candidate):
    post = candidate['candidate'].post_applied
    context = {
        'user': candidate,
        'candidate': candidate['candidate'],
        'post': post,
    }
    return render(request, 'candidate/home.html', context)


def edit_manifesto(request):
    if request.method == 'POST':
        user = get_user_details(request)
        if user['is_authenticated'] and user['is_candidate']:
            candidate = user['candidate']
            manifesto = request.POST.get('manifesto')
            print(f" ******************{manifesto}*************** ")
            candidate.manifesto = manifesto
            candidate.save()
            return redirect('election:home')
    return redirect('election:home')


def election_coordinator_home(request, election_coordinator_info):
    ec = election_coordinator_info['election_cordinator']
    context = {
        'user': election_coordinator_info,
        'ec': ec,
    }
    return render(request, 'election_coordinator/home.html', context)


def start_election(request):
    error = []
    if request.method == 'POST':
        ec_info = get_user_details(request)
        if ec_info['is_authenticated'] and ec_info['is_election_coordinator']:
            ec = ec_info['election_cordinator']
            if ec.start_time == None:
                ec.start_time = datetime.now()
                ec.save()
                return redirect('election:home')
            else:
                error.append(
                    'start-time already set & election already started')
        else:
            error.append("user isn't authenticated")
    else:
        error.append("invalid request")

    context = {
        'error': error,
        'back': 'election:home',
    }
    return render(request, 'error.html', context=context)


def end_election(request):
    error = []
    if request.method == 'POST':
        ec_info = get_user_details(request)
        if ec_info['is_authenticated'] and ec_info['is_election_coordinator']:
            ec = ec_info['election_cordinator']
            if ec.end_time == None:
                ec.end_time = datetime.now()
                ec.save()
                return redirect('election:home')
            else:
                error.append('end-time already set & election already started')
        else:
            error.append("user isn't authenticated")
    else:
        error.append("invalid request")

    context = {
        'error': error,
        'back': 'election:home',
    }
    return render(request, 'error.html', context=context)


def add_candidate(request):
    user_info = get_user_details(request)
    form = AddCandidateForm()
    if request.method == 'POST':
        if user_info['is_authenticated'] and user_info['is_election_coordinator']:
            ec = user_info['election_cordinator']
            form = AddCandidateForm(request.POST)
            if form.is_valid():
                rollno = form.cleaned_data['rollno']
                post_id = form.cleaned_data['post_applied']
                manifesto = form.cleaned_data['manifesto']
                if Voter.objects.filter(rollno=rollno).exists() and not Candidate.objects.filter(voter__rollno=rollno).exists():
                    try:
                        voter = Voter.objects.get(rollno=rollno)
                        post = Post.objects.get(id=post_id)
                        new_cand = Candidate(
                            voter=voter, manifesto=manifesto, post_applied=post)
                        new_cand.save()
                        messages.success(request, "New candidate added!!")
                        return redirect('election:home')
                    except:
                        messages.error(request, "rollno or post invalid")
                        return redirect('election:home')
                else:
                    messages.error(
                        request, "this voter is already a candidate")
            else:
                messages.error(request, "form not valid")
        else:
            messages.error(request, "user not authenticated")
    context = {
        'user': user_info,
        'form': form
    }
    return render(request, 'election_coordinator/add-candidate.html', context=context)


def add_post(request):
    user_info = get_user_details(request)
    form = AddPost()
    if request.method == 'POST':
        if user_info['is_authenticated'] and user_info['is_election_coordinator']:
            ec = user_info['election_cordinator']
            form = AddPost(request.POST)
            if form.is_valid():
                post_name = form.cleaned_data['post_name']
                desc = form.cleaned_data['desc']
                try:
                    post = Post(post_name = post_name, desc = desc)
                    post.save()
                    messages.success(request, "New POST added!!")
                    return redirect('election:home')
                except:                        
                    messages.error(request, "post already exists or invalid")
                    return redirect('election:home')
            else:
                messages.error(request, "form not valid")
        else:
            messages.error(request, "user not authenticated")
    context = {
        'user': user_info,
        'form': form
    }
    return render(request, 'election_coordinator/add-post.html', context)
    


