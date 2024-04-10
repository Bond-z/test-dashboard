from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from base.models import Item, AllTestCase, TestResults, SccAwsResult, SccAzureResult, FcpAwsResult, FcpAzureResult, ReleaseStat, ReleaseVersion
from .serializers import ItemSerializer, TestcaseSerializer, TestresultsSerializer, SccAwsResultSerializer, SccAzureResultSerializer, FcpAwsResultSerializer, FcpAzureResultSerializer, ReleaseStatResultSerializer, ServiceResultSerializer, ReleaseVersionSerializer

@api_view(['GET'])
def getData(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addItem(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteItem(request, pk):
    instance = Item.objects.get(id=pk)
    instance.delete()

    return Response("Item successfully delete!")

@api_view(['POST'])
def addTestcases(request):
    serializer = TestcaseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def getTestcases(request):
    items = AllTestCase.objects.all()
    serializer = TestcaseSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def updateTestcases(request,pk):
    item = AllTestCase.objects.get(id=pk)
    serializer = TestcaseSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteTestcase(request, pk):
    instance = AllTestCase.objects.get(id=pk)
    instance.delete()

    return Response("Test case successfully delete!")

# @api_view(['POST'])
# def createTestCycle(request):
#     serializer = TestcycleSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# @api_view(['GET'])
# def getTestCycle(request):
#     items = TestCycle.objects.all()
#     serializer = TestcycleSerializer(items, many=True)
#     return Response(serializer.data)

@api_view(['POST'])
def addTestresult(request):
    # cycleid = TestResult.objects.get(id=pk)
    serializer = TestresultsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def getTestRunResult(request):
    # instance = TestResult.objects.get(id=pk)
    items = TestResults.objects.all()
    serializer = TestresultsSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def updateTestresult(request,pk):
    item = TestResults.objects.get(id=pk)
    serializer = TestresultsSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def addSccAwsResult(request):
    serializer = SccAwsResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def updateSccAwsTestresult(request,pk):
    item = SccAwsResult.objects.get(id=pk)
    serializer = SccAwsResultSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteSccAwsTestresult(request,pk):
    item = SccAwsResult.objects.get(id=pk)
    serializer = SccAwsResultSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.delete()
    return Response(serializer.data)

@api_view(['POST'])
def addSccAzureResult(request):
    serializer = SccAzureResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def updateSccAzureTestresult(request,pk):
    item = SccAzureResult.objects.get(id=pk)
    serializer = SccAzureResultSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def addFcpAwsResult(request):
    serializer = FcpAwsResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def updateFcpAwsTestresult(request,pk):
    item = FcpAwsResult.objects.get(id=pk)
    serializer = FcpAwsResultSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def addFcpAzureResult(request):
    serializer = FcpAzureResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def updateFcpAzureTestresult(request,pk):
    item = FcpAzureResult.objects.get(id=pk)
    serializer = FcpAzureResultSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def getSccAwsResult(request):
    items = SccAwsResult.objects.all()
    serializer = SccAwsResultSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSccAwsResult_by_cycle(request, pk):
    item = SccAwsResult.objects.filter(cycleid=pk.upper())
    serializer = SccAwsResultSerializer(item, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSccAzureResult(request):
    items = SccAzureResult.objects.all()
    serializer = SccAwsResultSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSccAzureResult_by_cycle(request, pk):
    item = SccAzureResult.objects.filter(cycleid=pk.upper())
    serializer = SccAzureResultSerializer(item, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getFcpAwsResult(request):
    items = FcpAwsResult.objects.all()
    serializer = FcpAwsResultSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getFcpAwsResult_by_cycle(request, pk):
    item = FcpAwsResult.objects.filter(cycleid=pk.upper())
    serializer = FcpAwsResultSerializer(item, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getFcpAzureResult(request):
    items = FcpAzureResult.objects.all()
    serializer = FcpAzureResultSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getFcpAzureResult_by_cycle(request, pk):
    item = FcpAzureResult.objects.filter(cycleid=pk.upper())
    serializer = FcpAzureResultSerializer(item, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addSummarizeInRelease(request):
    serializer = ReleaseStatResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def updateTestresultInRelease(request,pk):
    item = ReleaseStat.objects.get(id=pk)
    serializer = ReleaseStatResultSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def getResultFromAllRelease(request):
    items = ReleaseStat.objects.all()
    serializer = ReleaseStatResultSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ServiceResultListView(request):
    queryset = DailyTestResults.objects.all()
    serializer_class = DailyTestResultsSerializer(queryset, many=True)
    return Response(serializer_class.data)

@api_view(['POST'])
def addDailyTestResult(request):
    serializer = DailyTestResultsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def create_service_result(request):
    if request.method == 'POST':
        serializer = ServiceResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def create_release_tag(request):
    if request.method == 'POST':
        serializer = ReleaseVersionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getReleaseTag(request):
    items = ReleaseVersion.objects.all()
    serializer = ReleaseVersionSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def updateReleaseTag(request,pk):
    item = ReleaseVersion.objects.get(id=pk)
    serializer = ReleaseVersionSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)