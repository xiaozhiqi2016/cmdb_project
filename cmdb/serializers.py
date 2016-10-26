#_*_coding:utf-8_*_
from myuser.models import UserProfile
from cmdb import models
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'name', 'email','is_staff')


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        depth=2
        fields = ('url','name','sn','asset_type','create_date','manufactory')


class ManufactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        # depth=2
        fields = ('url','manufactory','support_num','memo')

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Server
        fields = ('url','os_type','os_distribution','os_release','create_date','update_date')