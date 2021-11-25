from django.shortcuts import render, redirect
from django.contrib import messages
from election.utils import get_user_details
from election.models import *
from django.db.models import Count


def index(request):

    voter = get_user_details(request)
    if voter['is_authenticated'] == True:
        return redirect('election:home')

    context = {
        'user': voter,
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
#         ],
#         'candidate_names' : [<candidate_names>],
#         'candidate_vote_counts' : [candidate_vote_counts
# s],
#     },
# ]

def get_vote_count():
    VOTE_COUNT = []
    total_voters = Voter.objects.all().count()
    for post in Post.objects.all():
        post_details = {}
        post_details['post'] = post
        post_details['candidate_names'] = []
        post_details['candidate_vote_counts'] = []

        if not Candidate.objects.filter(post_applied=post).exists():
            post_details['winning_candidate'] = None
            post_details['reason'] = "No Candidate Competing"
            VOTE_COUNT.append(post_details)
            continue

        total_votes = Vote.objects.filter(post=post).count()
        vote_count = Vote.objects.filter(post=post).values(
            'candidate').annotate(
                no_of_votes=Count('candidate')).order_by('-no_of_votes')

        post_details['winning_candidate'] = [
            Candidate.objects.get(id=vote_count.first()['candidate']),
            vote_count.first()['no_of_votes'],
        ]

        votes_for_each_candidate = []
        for x in vote_count:
            candidate_id, count = x['candidate'], x['no_of_votes']
            candidate = Candidate.objects.get(id=candidate_id)
            cand_info = {
                'candidate': candidate,
                'vote_count': count
            }
            votes_for_each_candidate.append(cand_info)
            post_details['candidate_names'].append(
                str(candidate.voter.first_name + candidate.voter.last_name)
            )
            post_details['candidate_vote_counts'].append(count)

        # details of votes not cast
        votes_for_each_candidate.append({
            'candidate': None,
            'vote_count': total_voters - total_votes,
        })
        post_details['candidate_names'].append('None')
        post_details['candidate_vote_counts'].append(
            total_voters - total_votes)

        post_details['votes_for_each_candidate'] = votes_for_each_candidate

        VOTE_COUNT.append(post_details)

    return VOTE_COUNT


def result(request):
    election_time = Election_Coordinator.objects.values(
        'start_time', 'end_time').first()
    start_time = election_time['start_time']
    end_time = election_time['end_time']

    if start_time and end_time:
        result = get_vote_count()
        posts = Post.objects.all()
        post_id = []
        for post in posts:
            post_id.append(str(post.id))

        all_candidate_names = []
        all_candidate_vote_counts = []
        for x in result:
            all_candidate_names.append(x['candidate_names'])
            all_candidate_vote_counts.append(
                x['candidate_vote_counts']
            )

        context = {
            'result': result,
            # result --> VOTE_COUNT
            'user': get_user_details(request),
            'post_id': post_id,
            'all_candidate_names': all_candidate_names,
            'all_candidate_vote_counts': all_candidate_vote_counts,
        }
        return render(request, 'result.html', context=context)
    
    elif start_time:
        messages.error(request, "Election currently ONGOING. Visit after it ends.")
        return redirect('index')
    
    else:
        messages.success(request, "Election NOT started")
        return redirect('index')
