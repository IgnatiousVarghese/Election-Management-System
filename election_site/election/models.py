from django.db import models


class Post(models.Model):
    post_name = models.CharField(max_length=45, unique=True)
    desc = models.TextField()

    def __str__(self):
        return self.post_name


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
    post_applied = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.voter.first_name


class Election_Coordinator(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)

    start_time = models.DateTimeField(null = True, default=None)
    end_time = models.DateTimeField(null = True, default=None)


class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('voter', 'post'), )

    def __str__(self):
        return f"voter : {self.voter}\nPost : {self.post}\ncandidate : {self.candidate}"
