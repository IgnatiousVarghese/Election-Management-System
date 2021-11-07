from .models import *

def vote_detail(voter):
    votes = Vote.objects.filter(voter = voter)
    detail = {}             ### type: Dict{Post:Candidate}
    posts = Post.objects.all()
    for p in posts:
        detail[p] = None
        p_vote = votes.filter(post = p)
        if p_vote.exists():
            detail[p] = p_vote[0]

    return detail
    
def all_voter_election_info(voter):
    votes = Vote.objects.filter(voter = voter)
    detail = {}             ### type: Dict{Post:Candidate}
    posts = Post.objects.all()
    for p in posts:
        detail[p] = []
        candidates = Candidate.objects.filter(post_applied = p)
        for c in candidates:
            if votes.filter(candidate = c).exists():
                detail[p].append((c,True))
            else:
                detail[p].append((c,False))

    return detail

def get_voter_details(request):
    USER = {
        'is_authenticated': True,
        'is_candidate': False,
        'is_election_coordinator': False,
        'account_type' : None,
        'username' : None,
    }
    if request.session.has_key('voter'):
        USER['account_type'] = 'Voter'
        rollno = request.session['voter']
        USER['username'] = rollno
        try:
            v = Voter.objects.get(rollno=rollno)
            USER['voter'] = v
            USER['votes'] = vote_detail(v)
            USER['all_voter_election_info'] = all_voter_election_info(v)
        except:
            USER['is_authenticated'] = False
            return USER

    elif request.session.has_key('candidate'):
        USER['account_type'] = 'Candidate'
        USER['is_candidate'] = True
        rollno = request.session['candidate']
        USER['username'] = rollno
		
        try:
            c = Candidate.objects.get(pk=rollno)
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
