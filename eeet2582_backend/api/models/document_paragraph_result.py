from django.db import models


class DocumentParagraphResult(models.Model):
    id = models.AutoField(primary_key=True)
    original_paragraph = models.ForeignKey('DocumentParagraph', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.content}"