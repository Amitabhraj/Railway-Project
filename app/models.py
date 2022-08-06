from django.db import models,migrations
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.



class Main_Data_Upload(models.Model):
    unique_id = models.FloatField(default=None, null=True, blank=True)
    sl_no = models.FloatField(default=None, null=True, blank=True)
    reference_no = models.FloatField(default=None, null=True, blank=True)
    registration_date = models.DateTimeField(default=None,null=True, blank=True)
    closing_date = models.DateTimeField(default=None,null=True, blank=True)
    disposal_time = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    mode = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    train_station = models.FloatField(null=True, blank=True)
    channel = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    Type = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    coach_number = models.FloatField(null=True, blank=True)
    rake_number = models.FloatField(null=True, blank=True)
    staff_name = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    problem_type = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    sub_type = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    commodity = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    zone = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    div = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    dept = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    breach = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    rating = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    status = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    complaint_discription = models.TextField(default=None, max_length=100000000, null=True, blank=True)
    remark = models.TextField(default=None, max_length=100000000, null=True, blank=True)
    number_of_time_forwarded = models.FloatField( default=None, null=True, blank=True)
    pnr_utc_number = models.CharField(max_length=100000000,default=None, null=True, blank=True)
    coach_type = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    coach_number_no = models.CharField(max_length=100000000,default=None, null=True, blank=True)
    feedback_remark = models.TextField(max_length=100000000, default=None, null=True, blank=True)
    upcoming_station = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    mobile_number_or_email = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    physical_coach_number = models.FloatField(default=None, null=True, blank=True)






    def __str__(self):
        return str(self.coach_number)





class PhoneNumber(models.Model):
    mobile_number = models.IntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return str(self.mobile_number)





class CsvFile(models.Model):
    csv_data = models.FileField(upload_to="data/railway/", null=True, blank=True)


    def __str__(self):
        return str(self.csv_data)




