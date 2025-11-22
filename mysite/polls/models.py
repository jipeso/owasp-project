from django.db import models

# Create your models here.

class Poll(models.Model):
  question = models.CharField(max_length=200)
  creator = models.CharField(max_length=20)

  def __str__(self):
    return self.question
  
class Choice(models.Model):
  poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
  text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)

class Vote(models.Model):
  user = models.CharField(max_length=20)
  choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
