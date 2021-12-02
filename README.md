# Election-Management-System App

Django Election-Management-System App is a full featured voting app. You will have to be part of the college to use this app and to cast vote. Voter and Election_coordinator details should be populated in database before starting of web app. Once voted for a post he/she will not be able to cast vote for that post again. Only election coordinator can add or remove posts and candidates. Candidates can be choosen only from the existing voters. Once election is ended it shows the final result. Candidates can add or edit there manifesto before starting the election.
<br>
SQLite database is utilized for this application to strore the data of all voters, candidates, posts and other information. 


<h1>Getting Started</h1>
<p>These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.</p>

<h2>Prerequisites</h2>
<code>python== 3.5 or up and django==2.0 or up</code><br>

Following are the commands to install Django in a virtual environment if its already not installed:-<br>
<code>sudo apt install python3-venv</code><br>
<code>python3 -m venv dbms_project</code><br>
<code>source dbms_project/bin/activate</code><br>

<h2>Installing</h2>
To get the source code enter the following the command:-
<code>git clone https://github.com/IgnatiousVarghese/Election-Management-System.git</code><br><br>

<h2>To migrate the database open terminal in project directory and type</h2>
<br><code>cd election_site</code><br>
<code>python manage.py migrate</code>

<h2>Details on tables migrated </h2>
<p>
The above mentioned commands will create a database with table for <br>
<code>Voter</code>  - detail of all voters populated before start of web app,
<br>
<code>Candidates</code>     - data of voters contesting in the electioon for any post
<br>
<code>Election Coordinator</code>   - should contain a single election coordinator
<br>
<code>Manage_Candidate</code>   - contains timestamp on when candidate was added
<br>
<code>Manage_Post</code>   - contains timestamp on when Post was added
<br>

To create Election Coordinator enter the following command:-
<br>
```
pip install Faker
cd election_site
python manage.py shell
from election.models import Election_Coordinator
username = "REQUIRED_USERNAME"
password = "REQUIRED_PASSWORD"
ec = Election_Coordinator(username=username, password = password)
ec.save()
```

To seed random set Voters use seeder.py file
<br>

```
from seeder import *
seeder.seed_voter()
```

seed_votes() populates 50 voters to database


<h2> To run the program in local server use the following command </h2>
<code>python manage.py runserver</code>

<p>
Then go to <a>http://127.0.0.1:8000 </a>in your browser
</p>


