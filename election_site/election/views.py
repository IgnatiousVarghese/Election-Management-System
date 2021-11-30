from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from .utils import get_user_details, get_vote_stat
from .models import *
from .forms import AddCandidateForm, AddPost, SearchForm
from datetime import datetime


def home(request):
    USER = get_user_details(request)
    if USER['is_authenticated'] == False:
        return redirect('/')

    elif(USER['account_type'] == 'Voter'):
        return voter_home(request, USER)

    elif USER['account_type'] == 'Candidate':
        return candidate_home(request, USER)

    elif USER['account_type'] == 'Election_Coordinator':
        return election_coordinator_home(request, USER)

    return HttpResponse("ERROR!!!!!!")


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
                voter=voter['voter']).filter(post=post
                                             )
            if not already_voted.exists():
                voter_vote = Vote(voter=voter['voter'],
                                  candidate=candidate, post=post)
                print(voter_vote)
                voter_vote.save()
            else:
                messages.error(request, "You Have already voted on this post")
        except:
            return HttpResponse("Some problem with Database\n Please contact admin.")

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
            messages.success(request, "Your Manifesto has been updated.")
            return redirect('election:home')
    return redirect('election:home')


def election_coordinator_home(request, election_coordinator_info):
    ec = election_coordinator_info['election_cordinator']
    context = {
        'user': election_coordinator_info,
        'ec': ec,
        'vote_stat': get_vote_stat()
    }
    return render(request, 'election_coordinator/home.html', context)


def start_election(request):
    if request.method == 'POST':
        ec_info = get_user_details(request)
        if ec_info['is_authenticated'] and ec_info['is_election_coordinator']:
            ec = ec_info['election_cordinator']
            if ec.start_time == None:

                posts = Post.objects.all()
                for post in posts:
                    if Candidate.objects.filter(post_applied = post).count() <2:
                        messages.error(request, f"Less than two candidates in {post.post_name}")
                        return redirect('election:home')

                ec.start_time = datetime.now()
                x = ec.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                print(f"*********\n\n\n{x}\n\n\n******")
                ec.save()
                messages.success(request, f"Election have officially began. time : {ec.start_time}")
                return redirect('election:home')
            else:
                messages.error(request , "Election has already been started")
                
        else:
            messages.error("User isn't authenticated")
    else:
        messages.error("Invalid request")

    return redirect('election:home')

def end_election(request):
    if request.method == 'POST':
        ec_info = get_user_details(request)
        if ec_info['is_authenticated'] and ec_info['is_election_coordinator']:
            ec = ec_info['election_cordinator']
            if ec.start_time is not None:
                if ec.end_time == None:
                    ec.end_time = datetime.now()
                    end_time = ec.end_time.strftime("%m/%d/%Y, %H:%M:%S")
                    ec.save()
                    messages.success(request, f"Election has offiaclly Ended. time : {end_time}")
                    return redirect('result')
                else:
                    messages.error('Election already ended.')
            else:
                messages.error("Election Not started.\n Please start it to end it.")
        else:
            messages.error("User isn't authenticated or not an EC")
    else:
        messages.error("Invalid request")

    return redirect('election:home')

def add_candidate(request):
    user_info = get_user_details(request)
    if not user_info['is_authenticated'] or not user_info['is_election_coordinator']:
        messages.error(request, "user not authenticated")
        return redirect('index')
    form = AddCandidateForm()
    if request.method == 'POST':
        ec = user_info['election_cordinator']
        form = AddCandidateForm(request.POST)
        if form.is_valid():
            rollno = form.cleaned_data['rollno']
            post = form.cleaned_data['post_applied']
            manifesto = form.cleaned_data['manifesto']
            if Voter.objects.filter(rollno=rollno).exists() and not Candidate.objects.filter(voter__rollno=rollno).exists():
                try:
                    voter = Voter.objects.get(rollno=rollno)
                    new_cand = Candidate(
                        voter=voter, manifesto=manifesto, post_applied=post)
                    new_cand.save()
                    m_cand = Manage_Candidate(
                        candidate=new_cand,
                        ec = ec,
                    )
                    m_cand.save()
                    messages.success(request, "New candidate added!")
                    return redirect('election:home')
                except:
                    messages.error(request, "Rollno or post invalid OR voter already candidate")
                    return redirect('election:home')
            elif Voter.objects.filter(rollno=rollno).exists()==False:
                messages.error(
                    request, "This is not a valid voter")
            else :
                messages.error(
                    request, "This voter is already a candidate")
        else:
            messages.error(request, "Form not valid")

    context = {
        'user': user_info,
        'form': form
    }
    return render(request, 'election_coordinator/add-candidate.html', context=context)

def add_post(request):
    user_info = get_user_details(request)
    if not user_info['is_authenticated'] or not user_info['is_election_coordinator']:
        messages.error(request, "user not authenticated")
        return redirect('index')
    form = AddPost()
    if request.method == 'POST':
        ec = user_info['election_cordinator']
        form = AddPost(request.POST)
        if form.is_valid():
            post_name = form.cleaned_data['post_name']
            desc = form.cleaned_data['desc']
            try:
                post = Post(post_name=post_name, desc=desc)
                post.save()
                mang_post = Manage_Post(
                    post = post, 
                    ec = ec,
                )
                mang_post.save()
                messages.success(request, "New POST added!")
                return redirect('election:home')
            except:
                messages.error(request, "Post already exists or invalid")
                return redirect('election:home')
        else:
            messages.error(request, "Form not valid")
    context = {
        'user': user_info,
        'form': form
    }
    return render(request, 'election_coordinator/add-post.html', context)

def search_candidate(request):
    user_info = get_user_details(request)
    form = SearchForm()
    if not user_info['is_authenticated'] or not user_info['is_election_coordinator']:
        messages.error(request, "User not authenticated or not an EC")
        return redirect('index')

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            rollno = form.cleaned_data['username']
            try:
                candidate = Candidate.objects.get(voter__rollno=rollno)
                mang_cand = Manage_Candidate.objects.get(candidate=candidate)
                messages.success(request, "Candidate Found")
                context = {
                    'user': user_info,
                    'form': form,
                    'candidate': candidate,
                    'mang_cand': mang_cand,
                }
                return render(request, 'election_coordinator/search-candidate.html', context)
            except:
                messages.error(request, "Candidate Not found")
        else:
            messages.error(request, "Input invalid")
    candidates = []
    for c in Candidate.objects.all():
        candidates.append({
            'candidate' : c,
            'form' : SearchForm(initial = {
                'username' : c.voter.rollno,
            })
        })
    context = {
        'user': user_info,
        'form': form,
        'candidates' : candidates,
    }
    return render(request, 'election_coordinator/search-candidate.html', context)

def del_candidate(request):
    user_info = get_user_details(request)
    
    if not user_info['is_authenticated'] or not user_info['is_election_coordinator']:
        messages.error(request, "user not authenticated")
        return redirect('index')

    if request.method == 'POST':
        rollno = request.POST['rollno']
        try:
            candidate = Candidate.objects.get(voter__rollno=rollno)
            candidate.delete()
            messages.success(request, "Candidate successfully deleted")
        except:
            messages.error(request, "Candidate could't be deleted")

    return redirect('election:home')

def search_post(request):
    user_info = get_user_details(request)
    if not user_info['is_authenticated'] or not user_info['is_election_coordinator']:
        messages.error(request, "user not authenticated")
        return redirect('index')

    if request.method == 'POST':
        post_name = request.POST['post_name']
        if post_name:
            try:
                
                post = Post.objects.get(post_name=post_name)
                mang_post = Manage_Post.objects.get(post =post)
                messages.success(request, "Post Found")
                context = {
                    'user': user_info,
                    'post': post,
                    'mang_post': mang_post
                }
                return render(request, 'election_coordinator/search-post.html', context)
            except:
                messages.error(request, "Post Not found")
        else:
            messages.error(request, "Input invalid")
    
    posts = []
    for post in Post.objects.all():
        posts.append({
            'post': post,
            'form': SearchForm(initial = {
                'username' : post.post_name,
            })
        })
    context = {
        'user': user_info,
        'posts' : posts,
        'form' : SearchForm()
    }
    return render(request, 'election_coordinator/search-post.html', context)

def del_post(request):
    user_info = get_user_details(request)
    
    if not user_info['is_authenticated'] or not user_info['is_election_coordinator']:
        messages.error(request, "user not authenticated")
        return redirect('index')

    if request.method == 'POST':
        post_id = request.POST['post_id']
        try:
            post = Post.objects.get(id = post_id)
            post.delete()
            messages.success(request, "Post successfully deleted")
        except:
            messages.error(request, "Post could't be deleted")
    return redirect('election:home')
