from django.db import models


class Caption(models.Model):
    id = models.AutoField(primary_key=True)
    user_document = models.ForeignKey('UserDocument', on_delete=models.CASCADE)
    document_paragraph = models.ForeignKey('DocumentParagraph', on_delete=models.CASCADE, null=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.content}"
