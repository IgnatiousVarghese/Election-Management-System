from django.shortcuts import render

def home(request):
    is_logged_in = True
    login_type = None
    context = { }
    if request.session.has_key('voter'):
        login_type = 'Voter'
        context['username'] = request.session['voter']
    elif request.session.has_key('candidate'):
        login_type = 'Candidate'
        context['username'] = request.session['candidate']
    elif request.session.has_key('election_cordinator'):
        login_type = 'Election Coordinator'
        context['username'] = request.session['election_cordinator']
    else:
        is_logged_in = False

    context.update({
        'is_logged_in': is_logged_in,
        'login_type': login_type,
    })

    return render(request, 'home.html', context)
