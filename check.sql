CREATE TABLE "account_voter" 
("rollno" integer NOT NULL PRIMARY KEY, 
"first_name" varchar(30) NOT NULL, 
"last_name" varchar(30) NOT NULL, 
"email" varchar(254) NOT NULL UNIQUE, 
"otp" integer NOT NULL)

CREATE TABLE "account_election_cordinator" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "username" varchar(30) NOT NULL UNIQUE, 
"password" varchar(30) NOT NULL)

CREATE TABLE "account_candidate" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"password" varchar(30) NOT NULL, 
"manifetso" text NOT NULL, 
"voter_id" integer NOT NULL UNIQUE REFERENCES 
"account_voter" ("rollno") DEFERRABLE INITIALLY DEFERRED)