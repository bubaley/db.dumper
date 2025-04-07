from air_drf_relation.fields import AirRelatedField
from air_drf_relation.serializers import AirModelSerializer
from core.utils.crypto_field import CryptoField

from .models import Config, DatabaseConnection, S3Connection, SSHConnection


class CryptoSerializer(AirModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for el in instance._meta.fields:
            if isinstance(el, CryptoField):
                data.pop(el.name, None)
        return data


class SSHConnectionSerializer(CryptoSerializer):
    class Meta:
        model = SSHConnection
        fields = ('id', 'name', 'host', 'username', 'port', 'password', 'private_key', 'passphrase', 'type')


class S3ConnectionSerializer(CryptoSerializer):
    class Meta:
        model = S3Connection
        fields = ('id', 'name', 'bucket', 'url', 'region', 'access_key', 'secret_key', 'root')


class DatabaseConnectionSerializer(CryptoSerializer):
    class Meta:
        model = DatabaseConnection
        fields = ('id', 'type', 'db', 'host', 'port', 'user', 'password')
        extra_kwargs = {
            'user': {'required': False},
            'password': {'required': False},
            'host': {'required': False},
            'port': {'required': False},
        }


class ConfigSerializer(AirModelSerializer):
    ssh_connection = AirRelatedField(SSHConnectionSerializer)
    s3_connection = AirRelatedField(S3ConnectionSerializer)
    database_connection = DatabaseConnectionSerializer()

    class Meta:
        model = Config
        fields = (
            'id',
            'name',
            'key',
            'max_versions',
            'database_connection',
            'ssh_connection',
            's3_connection',
            'auto_build',
        )
        action_read_only_fields = {'update': ('key',)}

    def update_or_create(self, instance, validated_data):
        db = validated_data.pop('database_connection', None)
        database_connection = instance.database_connection if instance else DatabaseConnection()
        for key, value in db.items():
            setattr(database_connection, key, value)
        database_connection.save()
        validated_data['database_connection'] = database_connection
        return super().update_or_create(instance, validated_data)


class ConfigSimpleSerializer(AirModelSerializer):
    class Meta:
        model = Config
        fields = ('id', 'name', 'key')
