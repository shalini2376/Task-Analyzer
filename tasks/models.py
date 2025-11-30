from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)

    # When this task is due
    due_date = models.DateField()

     # How important is this task? 1 (low) to 10 (very high)
    importance = models.IntegerField(default=5) # Scale 1-10

    # How many hours you think it will take
    estimated_hours = models.IntegerField(default=1)

    # Simple JSON field to store dependency IDs [1, 2, 3]
    dependencies = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title