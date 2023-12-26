from django.db import models


class DocumentParagraph(models.Model):
    id = models.AutoField(primary_key=True)
    user_document = models.ForeignKey('UserDocument', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.content}"