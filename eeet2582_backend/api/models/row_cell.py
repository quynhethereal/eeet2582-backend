from django.db import models

class RowCell(models.Model):
    id = models.AutoField(primary_key=True)
    user_document = models.ForeignKey('UserDocument', on_delete=models.CASCADE)
    document_table = models.ForeignKey('DocumentTable', on_delete=models.CASCADE)
    table_row = models.ForeignKey('TableRow', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.content}"
    