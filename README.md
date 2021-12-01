# Election-Management-System App

Django Election-Management-System App is a full featured voting app. You have to register in this app to show the polls and to vote. If you already voted you can not vote again. Only the owner of a poll can add poll , edit poll, update poll, delete poll , add choice, update choice, delete choice and end a poll. If a poll is ended it can not be voted. Ended poll only shows user the final result of the poll. There is a search option for polls. Also user can filter polls by name, publish date, and by number of voted. Pagination will work even after applying filter.

<h1>Getting Started</h1>
<p>These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.</p>

<h2>Prerequisites</h2>
<code>python== 3.5 or up and django==2.0 or up</code>

Following are the commands to install Django in a virtual environment if its already not installed:-
sudo apt install python3-venv
python3 -m venv dbms_project
source dbms_project/bin/activate

<h2>Installing</h2>
<pre>open terminal and type</pre>
<code>git clone https://github.com/IgnatiousVarghese/Election-Management-System.git</code><br><br>

<h4>or simply download using the url below</h4>
<code>https://github.com/IgnatiousVarghese/Election-Management-System.git</code><br>

<h2>To migrate the database open terminal in project directory and type</h2>
<code>cd election_site</code><br>
<code>python manage.py migrate</code>

<h2>To create Election Coordinator </h2>
<p>
The above mentioned commands will create a database with table for 
<code>Voter</code>
<code>Candidates</code>
<code>Election Coordinator</code>
<code>Election_Coordinator</code>
<code>Election_Coordinator</code>
The superuser created is NOT the Election Coordinator. EC has to be created by superuser in <code>Election_Coordinator</code> table
</p><br>
<code>python manage.py createsuperuser</code>

<h2>To Create some dummy text data for your app follow the step below:</h2>
<code>pip install faker</code>
<code>python manage.py shell</code>
<code>import seeder</code>
<code>seeder.seed_voter()</code>
<code>seeder.seed_posts_and_candidates()</code>
<code>seeder.seed_votes()</code>


<h2> To run the program in local server use the following command </h2>
<code>python manage.py runserver</code>

<p>Then go to http://127.0.0.1:8000 in your browser</p>

<h2>Project snapshot</h2>
<h3>Home page</h3>
<div align="center">
    <img src="https://user-images.githubusercontent.com/19981097/51409444-0e40a600-1b8c-11e9-9ab0-27d759db8973.jpg" width="100%"</img> 
</div>

<h3>Login Page</h3>
<div align="center">
    <img src="https://user-images.githubusercontent.com/19981097/51409509-36c8a000-1b8c-11e9-845a-65b49262aa53.png" width="100%"</img> 
</div>

<h2>Author</h2>
<blockquote>
  Ignatious Varghese<br>
  Email: ignatious@gmail.com
</blockquote>

<div align="center">
    <h3>========Thank You !!!=========</h3>
</div>
