from election.models import *
import datetime
import random
import time
from faker import Faker
fake = Faker()


def seed_voter(num_entries=50, overwrite=False):
    """
    Creates num_entries worth a new voters
    """
    if overwrite:
        print("Overwriting Users")
        Voter.objects.all().delete()
    count = 0
    for i in range(num_entries):
        first_name = fake.first_name()
        last_name = fake.last_name()
        v = Voter(
            rollno=f"V{count}",
            first_name=first_name,
            last_name=last_name,
            email=first_name + "." + last_name + "@fakermail.com",
            password="1234"
        )
        v.save()
        count += 1
        percent_complete = count / num_entries * 100
        print(
            "Adding {} new Voters: {:.2f}%".format(
                num_entries, percent_complete),
            end='\r',
            flush=True
        )
    print()

def seed_posts_and_candidates(num_entries=3, overwrite=False):
    """
    Creates num_entries worth a new voters
    """
    if overwrite:
        print("Overwriting Users")
        Post.objects.all().delete()
    count = 0
    c_count = 0
    # c_count -> count of new candidates created
    for i in range(num_entries):
        post_name = fake.job()
        p = Post(
            post_name=post_name, 
            desc = fake.paragraph(2),
        )
        p.save()
        x = random.randint(2,4)
        for j in range(x):
            v = Voter(
                rollno = f"C{c_count}",
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                email= f"c{c_count}" + "@fakermail.com",
                password="1234"                
            )
            v.save()
            c_count += 1
            c = Candidate(
                voter = v,
                manifesto = fake.paragraph(7),
                post_applied = p,
            )
            c.save()

        count += 1
        percent_complete = count / num_entries * 100
        print(
            "Adding {} new Posts: {:.2f}%".format(
                num_entries, percent_complete),
            end='\r',
            flush=True
        )
    print()

def seed_votes():
    Vote.objects.all().delete()
    voters = Voter.objects.all()
    posts = Post.objects.all()
    for post in posts:
        candidates = Candidate.objects.filter(post_applied=post)
        nota = 0
        for v in voters:
            i = random.randint(0, len(candidates))
            if i:
                c = candidates[i-1]
                vote = Vote(
                    voter = v,
                    candidate = c,
                    post = post,
                )
                vote.save()
            else:
                print(f"{v.rollno} not voting in {post.post_name}")
                nota+=1
        print(f"nota for {post.post_name} is {nota}")
