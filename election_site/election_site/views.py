from django.shortcuts import render, redirect
from election.utils import get_user_details
from election.models import *
from django.db.models import Count

def index(request):

    voter = get_user_details(request)
    if voter['is_authenticated'] == True:
        return redirect('election:home')
    
    context = {
        'voter' : voter,
    }

    return render(request, 'index.html', context)


# get_vote_count ==>>
# VOTE_COUNT = [  ##py list
#     {    ##py dict
#         'post' : <post>,
#         'winning_candidate' : [    ##py list
#             <each_candidate> , <vote_count>
#         ],
#         'votes_for_each_candidate' : [ ##py list
#             {    ##py dict
#               'candidate' :<candidate> , 
#               'vote_count' : <vote_count>
#             }
#         ]
#     },
# ]

def get_vote_count():
    VOTE_COUNT = []
    for post in Post.objects.all():
        post_deatils = {}
        post_deatils['post'] = post

        if not Candidate.objects.filter(post_applied = post).exists():
            post_deatils['winning_candidate'] = None
            post_deatils['reason'] = "No Candidate Competing"
            VOTE_COUNT.append(post_deatils)
            continue

        total_votes = Vote.objects.filter(post=post).count()
        vote_count = Vote.objects.filter(post=post).values(
            'candidate').annotate(
                no_of_votes=Count('candidate')).order_by('-no_of_votes')

        # VOTE_COUNT[post]['winner']
        post_deatils['winning_candidate'] = [
                Candidate.objects.get(id=vote_count.first()['candidate']),
                vote_count.first()['no_of_votes'],
            ]

        # VOTE_COUNT[post]['votes_for_each_candidate']
        
        votes_for_each_candidate = []
        for x in vote_count:
            candidate_id, count = x['candidate'], x['no_of_votes']
            candidate = Candidate.objects.get(id=candidate_id)
            cand_info = {
                'candidate': candidate,
                'vote_count': count
            }
            votes_for_each_candidate.append(cand_info)

        post_deatils['votes_for_each_candidate'] = votes_for_each_candidate

        VOTE_COUNT.append(post_deatils)

    return VOTE_COUNT


def result(request):
    result = get_vote_count()
    context = {
        'result': result,   
        # result --> VOTE_COUNT
    }
    return render(request, 'result.html', context = context)