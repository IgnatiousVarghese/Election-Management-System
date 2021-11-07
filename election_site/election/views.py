from django.shortcuts import redirect, render, HttpResponse
from .utils import get_voter_details
from .models import *

def home(request):
    USER = get_voter_details(request)
    if(USER['account_type'] == 'Voter'):
        return voter_home(request, USER)
    return HttpResponse("you are not supposed to be here LOL get lost!!!!!!")


def voter_home(request, voter):
    context = {
        'voter' : voter,
        'posts' : Post.objects.all(),
        'candidates' : Candidate.objects.all(),
    }

    return render(request, 'voter/home.html', context)

def view_post(request, idpost):
    voter = get_voter_details(request)
    try:
        post = Post.objects.get(pk = idpost)
        candidates = Candidate.objects.filter(post_applied = post)
    except:
        return HttpResponse("Post not present")
    
    info = {
        post : voter['all_voter_election_info'][post]
    }
    context ={
        'voter' : voter,
        'info' : info,
    }
    return render(request, 'voter/view_post.html', context)

def vote(request, idpost, idcandidate):
    voter = get_voter_details(request)
    if voter['is_authenticated'] and (voter['account_type'] == 'Voter') and request.method == 'POST':
        try:
            candidate = Candidate.objects.get(voter_id = idcandidate)
            post = Post.objects.get(pk = idpost)
            already_voted = Vote.objects.filter(voter = voter['voter']).filter(post=post)
            if already_voted.exists():
                already_voted[0].delete()
            voter_vote = Vote(voter = voter['voter'], candidate = candidate, post = post)
            print(voter_vote)
            voter_vote.save()
        except:
            return HttpResponse("Some problem with Database\n plz contact admin.")
    
    return redirect('election:view_post', idpost)

