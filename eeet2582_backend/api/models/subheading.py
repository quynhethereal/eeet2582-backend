from django.db import models


class Subheading(models.Model):
    id = models.AutoField(primary_key=True)
    heading = models.ForeignKey('Heading', on_delete=models.CASCADE)
    content = models.TextField()
    type = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.content}"