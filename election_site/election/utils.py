from django.db.models.aggregates import Count
from .models import *

# this function returns a python dictionary with
# each post mapped with the vote of current voter for this particular post
# if not voted has None value


def vote_detail(voter):
    votes = Vote.objects.filter(voter=voter)
    detail = {}
    # type: Dict{Post:Candidate}
    posts = Post.objects.all()
    for p in posts:
        detail[p] = None
        p_vote = votes.filter(post=p)
        if p_vote.exists():
            detail[p] = p_vote[0]

    return detail

# this function returns a python dictionary with
# each post mapped with all a tuple that contains
# 1. candidates applied for it,
# 2. boolean value whether voter voted for that candidate


def my_votes_info(voter):
    votes = Vote.objects.filter(voter=voter)
    detail = {}
    # type: Dict{Post:Candidate}
    posts = Post.objects.all()
    for p in posts:
        detail[p] = []
        candidates = Candidate.objects.filter(post_applied=p)
        for c in candidates:
            if votes.filter(candidate=c).exists():
                detail[p].append((c, True))
            else:
                detail[p].append((c, False))

    return detail

# this function returns a python dictionary with
# that contains all neccessary info on the user that is logged in.


def get_user_details(request):
    USER = {
        'is_authenticated': True,
        'is_candidate': False,
        'is_election_coordinator': False,
        'account_type': None,
        'username': None,
    }
    if request.session.has_key('voter'):
        USER['account_type'] = 'Voter'
        rollno = request.session['voter']
        USER['username'] = rollno
        try:
            v = Voter.objects.get(rollno=rollno)
            USER['voter'] = v
            USER['my_votes'] = vote_detail(v)
            USER['my_votes_info'] = my_votes_info(v)
        except:
            USER['is_authenticated'] = False
            return USER

    elif request.session.has_key('candidate'):
        USER['account_type'] = 'Candidate'
        USER['is_candidate'] = True
        rollno = request.session['candidate']
        USER['username'] = rollno

        try:
            c = Candidate.objects.get(voter__rollno=rollno)
            USER['candidate'] = c
        except:
            USER['is_authenticated'] = False
            return USER

    elif request.session.has_key('election_cordinator'):
        USER['account_type'] = 'Election_Coordinator'
        USER['is_election_coordinator'] = True
        username = request.session['election_cordinator']
        USER['username'] = username
        try:
            ec = Election_Coordinator.objects.get(username=username)
            USER['election_cordinator'] = ec
        except:
            USER['is_authenticated'] = False
            return USER

    else:
        USER['is_authenticated'] = False

    return USER


#
# return stats of vote (count of how many voted)
# during election
#
def get_vote_stat():
    voter_vote_count = Vote.objects.values(
        'voter').annotate(vote_count=Count('voter'))
    # <QuerySet [{'voter': , 'vote_count': }]>
    total_voters = Voter.objects.all().count()
    total_voters_voted = voter_vote_count.count()
    vote_stat = {
        'voter_vote_count': voter_vote_count,
        'total_voters': total_voters,
        'total_voters_voted': total_voters_voted,
    }
    return vote_stat

