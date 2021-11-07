from django.shortcuts import render, redirect
from election.utils import get_voter_details

def index(request):

    voter = get_voter_details(request)
    if voter['is_authenticated'] == True:
        return redirect('election:home')
    
    context = {
        'voter' : voter,
    }

    return render(request, 'index.html', context)

