from django.db import models

# Create your models here.
class Queries(models.Model):
    Username = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    query = models.TextField()
    
class Login(models.Model):
    username = models.CharField(max_length=122)
    psw = models.CharField(max_length=20)
    
class Signup(models.Model):
    username = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    psw = models.CharField(max_length=20)
    
class QnA(models.Model):
    pdf=models.FileField(upload_to='pdf/',null=True,blank=False)