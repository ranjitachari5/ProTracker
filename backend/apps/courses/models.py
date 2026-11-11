from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
# Create your models here.
validators=[MinLengthValidator(6)]
choices=[("Youtube", "Youtube"), ("Udemy", "Udemy"),("Coursera","Coursera"),]
class Course(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(validators=validators,max_length=60,null=False)
    description=models.TextField(max_length=200,blank=True)
    platform=models.CharField(max_length=8,choices=choices)
    course_url=models.URLField(null=False)
    created_at=models.DateTimeField(auto_now_add=True)
