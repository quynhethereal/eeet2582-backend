from django.db import models
from eeet2582_backend.api.models.user_model import User


class UserDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_title = models.OneToOneField('DocumentTitle', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_title}"
