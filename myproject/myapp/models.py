from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

class Application(models.Model):
    date = models.DateField(auto_now=True)
    positionTitle = models.CharField(max_length=100)
    companyName = models.CharField(max_length=100)
    jobCategory = models.CharField(max_length=50)
    coverLetter = models.CharField(max_length=5)
    discoveryMethod = models.CharField(max_length=15)
    interviewCount = models.SmallIntegerField(default=0)
    jobOffer = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
