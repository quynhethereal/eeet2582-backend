# Generated by Django 5.0 on 2023-12-26 06:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentParagraph',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DocumentTitle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.TextField(max_length=500, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_subscription_id', models.CharField(max_length=255, unique=True)),
                ('stripe_customer_id', models.CharField(max_length=255, unique=True)),
                ('plan_name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('price', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='eeet2582_backend.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('document_title', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.documenttitle')),
            ],
        ),
        migrations.CreateModel(
            name='ListParagraph',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('document_paragraph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.documentparagraph')),
                ('user_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.userdocument')),
            ],
        ),
        migrations.CreateModel(
            name='Heading',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('document_paragraph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.documentparagraph')),
                ('user_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.userdocument')),
            ],
        ),
        migrations.CreateModel(
            name='EndNote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('user_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.userdocument')),
            ],
        ),
        migrations.AddField(
            model_name='documentparagraph',
            name='user_document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eeet2582_backend.userdocument'),
        ),
    ]