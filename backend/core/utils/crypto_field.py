from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

crypto_key = getattr(settings, 'CRYPTO_FIELD_KEY', None)
if crypto_key is None:
    raise ImproperlyConfigured('CRYPTO_FIELD_KEY must be set in settings')

cipher_suite = Fernet(crypto_key)


class CryptoField(models.TextField):
    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            value = value.encode()
        encrypted_value = cipher_suite.encrypt(value)
        return encrypted_value.decode()

    @staticmethod
    def from_db_value(value, *args, **kwargs):
        if value is None:
            return value
        try:
            decrypted_value = cipher_suite.decrypt(value.encode())
            return decrypted_value.decode()
        except InvalidToken:
            raise ValueError('Invalid CRYPTO_FIELD_KEY')

    def to_python(self, value):
        if value is None or isinstance(value, str):
            return value
        try:
            decrypted_value = cipher_suite.decrypt(value.encode())
            return decrypted_value.decode()
        except InvalidToken:
            raise ValueError('Cannot decrypt value.')
