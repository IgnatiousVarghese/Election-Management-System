from django.db import models

class Voter(models.Model):
    rollno = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    otp = models.IntegerField(default = 0)

    def __str__(self):
        return self.first_name

class Candidate(models.Model):
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE)
    password = models.CharField(max_length = 30)
    manifetso = models.TextField()

    def __str__(self):
        return self.voter.first_name 

class Election_Cordinator(models.Model):
    username = models.CharField(max_length = 30, unique=True)
    password = models.CharField(max_length = 30)
