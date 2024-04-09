from django.contrib import admin

# Register your models here.
from .models import TestResults, AllTestCase, SccAwsResult, SccAzureResult, FcpAwsResult, FcpAzureResult, ServiceResult, CloudServiceType

admin.site.register(AllTestCase)
admin.site.register(TestResults)
admin.site.register(SccAwsResult)
admin.site.register(SccAzureResult)
admin.site.register(FcpAwsResult)
admin.site.register(FcpAzureResult)
admin.site.register(ServiceResult)
admin.site.register(CloudServiceType)