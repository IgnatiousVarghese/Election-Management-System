from django.db import models


class Voter(models.Model):
    rollno = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name


class Candidate(models.Model):
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE)
    manifesto = models.TextField()

    def __str__(self):
        return self.voter.first_name


class Election_Coordinator(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)
