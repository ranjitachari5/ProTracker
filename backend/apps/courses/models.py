from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.utils import timezone
# Create your models here.
validators=[MinLengthValidator(6)]

min_max_for_progress=[MinValueValidator(0),MaxValueValidator(100)]
choices=[("Youtube", "Youtube"), ("Udemy", "Udemy"),("Coursera","Coursera"),]
progress_choice=[("not_started","Not Started"),("in_progress","In Progress"),("completed","Completed"),]
class Course(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(validators=validators,max_length=60,null=False)
    description=models.TextField(max_length=200,blank=True)
    platform=models.CharField(max_length=8,choices=choices)
    course_url=models.URLField(null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    progress=models.IntegerField(default=0,validators=min_max_for_progress)
    status=models.CharField(max_length=20,choices=progress_choice,default="not_started")
    completed_at = models.DateTimeField(null=True, blank=True)
    def update_status(self):
        if(self.progress==0):
            self.status="not_started"
        elif self.progress>0 and self.progress<100:
            self.status="in_progress"
        else:
            self.status="completed"
    def save(self, *args, **kwargs):
        self.update_status()

        if self.status == "completed":
            if self.pk:
                previous = Course.objects.filter(pk=self.pk).values(
                "status", "completed_at"
            ).first()

            if previous and previous["status"] != "completed":
                self.completed_at = timezone.now()
            elif previous:
                self.completed_at = previous["completed_at"]
            else:
             self.completed_at = timezone.now()
        else:
            self.completed_at = None

        super().save(*args, **kwargs)



