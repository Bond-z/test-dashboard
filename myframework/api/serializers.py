from rest_framework import serializers
from base.models import Item, AllTestCase, TestResults, SccAwsResult, SccAzureResult, FcpAwsResult, FcpAzureResult, ReleaseStat, ServiceResult, CloudServiceType, ReleaseVersion


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class TestcaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllTestCase
        fields = '__all__'

class TestresultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResults
        fields = '__all__'

class SccAwsResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SccAwsResult
        fields = '__all__'

class SccAzureResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SccAzureResult
        fields = '__all__'

class FcpAwsResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcpAwsResult
        fields = '__all__'

class FcpAzureResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcpAzureResult
        fields = '__all__'

class ReleaseStatResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseStat
        fields = '__all__'

class CloudServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudServiceType
        fields = ('name', 'pass_count', 'fail_count')

class ServiceResultSerializer(serializers.ModelSerializer):
    service_types = CloudServiceTypeSerializer(many=True)
    
    class Meta:
        model = ServiceResult
        fields = ('iteration', 'version', 'service_types')

    def create(self, validated_data):
        service_types_data = validated_data.pop('service_types')
        service_result = ServiceResult.objects.create(**validated_data)
        for service_type_data in service_types_data:
            CloudServiceType.objects.create(service_result=service_result, **service_type_data)
        return service_result
    
class ReleaseVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseVersion
        fields = '__all__'