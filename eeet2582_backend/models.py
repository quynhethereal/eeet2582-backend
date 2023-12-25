from django.db import models


# old user database model
# class User(models.Model):
#     # Add your additional fields here
#     # For example:
#     provider = models.TextField(max_length=500, blank=True)
#     provider_id = models.TextField(max_length=500, blank=True) # user id
#     name = models.TextField(max_length=500, blank=True)
#     email = models.TextField(max_length=500, blank=True)
#     subscriptionId = models.TextField(max_length=500, blank=True)
#     picture = models.TextField(max_length=500, blank=True)
#     is_active = models.BooleanField(default=True)


class DocumentTitle(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class UserDocument(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_title = models.OneToOneField('DocumentTitle', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_title}"


class DocumentParagraph(models.Model):
    id = models.AutoField(primary_key=True)
    user_document = models.ForeignKey('UserDocument', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.content}"


class Heading(models.Model):
    id = models.AutoField(primary_key=True)
    user_document = models.ForeignKey('UserDocument', on_delete=models.CASCADE)
    document_paragraph = models.ForeignKey('DocumentParagraph', on_delete=models.CASCADE, null=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.content}"


class EndNote(models.Model):
    id = models.AutoField(primary_key=True)
    user_document = models.ForeignKey('UserDocument', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.content}"


class ListParagraph(models.Model):
    id = models.AutoField(primary_key=True)
    user_document = models.ForeignKey('UserDocument', on_delete=models.CASCADE)
    document_paragraph = models.ForeignKey('DocumentParagraph', on_delete=models.CASCADE, null=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.content}"

class DocumentTable(models.Model):
    id = models.AutoField(primary_key=True)
    user_document = models.ForeignKey('UserDocument', on_delete=models.CASCADE)
    document_paragraph = models.ForeignKey('DocumentParagraph', on_delete=models.CASCADE, null=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.content}"

class TableRow(models.Model):
    id = models.AutoField(primary_key=True)
    user_document = models.ForeignKey('UserDocument', on_delete=models.CASCADE)
    document_table = models.ForeignKey('DocumentTable', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.content}"
    
class RowCell(models.Model):
    id = models.AutoField(primary_key=True)
    user_document = models.ForeignKey('UserDocument', on_delete=models.CASCADE)
    document_table = models.ForeignKey('DocumentTable', on_delete=models.CASCADE)
    table_row = models.ForeignKey('TableRow', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.content}"