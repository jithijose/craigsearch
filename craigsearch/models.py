from django.db import models

# Create your models here.
class Search(models.Model):
    search_text = models.CharField(max_length=100)
    search_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.search_text