from core.utils.crypto_field import CryptoField
from django.db import models


class SSHConnection(models.Model):
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    port = models.IntegerField(default=22)
    password = CryptoField(null=True)
    private_key = CryptoField(null=True)
    passphrase = CryptoField(null=True)


class S3Connection(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=16)
    bucket = models.CharField(max_length=128)
    access_key = CryptoField(null=True)
    secret_key = CryptoField(null=True)
    root = models.CharField(max_length=255, null=True)


class DatabaseConnection(models.Model):
    class Type(models.Choices):
        POSTGRES = 'postgres'

    type = models.CharField(max_length=32, choices=Type.choices)
    db = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    user = CryptoField()
    password = CryptoField()


class Config(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=64, unique=True)
    ssh_connection = models.ForeignKey('SSHConnection', on_delete=models.SET_NULL, null=True, related_name='configs')
    s3_connection = models.ForeignKey('S3Connection', on_delete=models.SET_NULL, null=True, related_name='configs')
    database_connection = models.OneToOneField('DatabaseConnection', on_delete=models.CASCADE, related_name='configs')
    max_versions = models.IntegerField(default=3)