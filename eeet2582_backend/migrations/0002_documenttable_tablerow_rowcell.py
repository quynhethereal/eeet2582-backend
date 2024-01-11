# Generated by Django 4.2.8 on 2023-12-26 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eeet2582_backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('document_paragraph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.documentparagraph')),
                ('user_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.userdocument')),
            ],
        ),
        migrations.CreateModel(
            name='TableRow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('document_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.documenttable')),
                ('user_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.userdocument')),
            ],
        ),
        migrations.CreateModel(
            name='RowCell',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('document_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.documenttable')),
                ('table_row', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.tablerow')),
                ('user_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.userdocument')),
            ],
        ),
    ]