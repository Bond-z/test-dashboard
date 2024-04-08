from django.db import models
# from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=200)
    create = models.DateTimeField(auto_now_add=True)

class TestRun(models.Model):
    testcaseid = models.CharField(max_length=100)
    usecase = models.CharField(max_length=400)
    testresult = models.CharField(max_length=50)
    create = models.DateTimeField(auto_now_add=True)

class AllTestCase(models.Model):
    testcaseid = models.CharField(max_length=50)
    usecase = models.CharField(max_length=400)

    def __str__(self):
        return self.testcaseid + "|" + self.usecase


class TestResults(models.Model):
    cycleid = models.CharField(max_length=10)
    testcaseid = models.CharField(max_length=50)
    usecase = models.CharField(max_length=400)
    result = models.CharField(max_length=10)
    remark = models.CharField(max_length=200, null=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cycleid + "|" +self.testcaseid + "|" +self.usecase + "|" +self.result

class SccAwsResult(models.Model):
    cycleid = models.CharField(max_length=10)
    pass_amt = models.CharField(max_length=50)
    fail_amt = models.CharField(max_length=50)
    percent_pass = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cycleid + "|" +self.pass_amt + "|" +self.fail_amt

class SccAzureResult(models.Model):
    cycleid = models.CharField(max_length=10)
    pass_amt = models.CharField(max_length=50)
    fail_amt = models.CharField(max_length=50)
    percent_pass = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cycleid + "|" +self.pass_amt + "|" +self.fail_amt

class FcpAwsResult(models.Model):
    cycleid = models.CharField(max_length=10)
    pass_amt = models.CharField(max_length=50)
    fail_amt = models.CharField(max_length=50)
    percent_pass = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cycleid + "|" +self.pass_amt + "|" +self.fail_amt

class FcpAzureResult(models.Model):
    cycleid = models.CharField(max_length=10)
    pass_amt = models.CharField(max_length=50)
    fail_amt = models.CharField(max_length=50)
    percent_pass = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cycleid + "|" +self.pass_amt + "|" +self.fail_amt

#sum all service type
class ReleaseStat(models.Model):
    cycleid = models.CharField(max_length=10)
    service_typ = models.CharField(max_length=10)
    cloud_provider = models.CharField(max_length=10)
    pass_amt = models.CharField(max_length=50)
    fail_amt = models.CharField(max_length=400)
    create = models.DateTimeField(auto_now_add=True)

class ServiceResult(models.Model):
    iteration = models.CharField(max_length=100)
    version = models.CharField(max_length=100)

    def __str__(self):
        return str(self.iteration) + "|" + str(self.version)

class CloudServiceType(models.Model):
    service_result = models.ForeignKey(ServiceResult, related_name='service_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pass_count = models.IntegerField(default=0)
    fail_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.service_result) + "|" +self.name + "|" + str(+self.pass_count) + "|" + str(self.fail_count)
    
class ReleaseVersion(models.Model):
    version = models.CharField(max_length=10)
    cycleid = models.CharField(max_length=10, default=None)
    title = models.CharField(max_length=500)
    stories = models.CharField(max_length=5000)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.version + "|" +self.title + "|" +self.cycleid + "|" +self.stories