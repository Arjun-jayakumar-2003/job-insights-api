from django.db import models

class JobQuery(models.Model):
    role = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class JobInsight(models.Model):
    query = models.ForeignKey(JobQuery, on_delete=models.CASCADE)
    total_jobs = models.IntegerField()
    top_skills = models.JSONField()
    top_locations = models.JSONField()
    average_salary = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)