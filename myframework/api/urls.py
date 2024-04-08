from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('add/', views.addItem),
    path('delete/<int:pk>/', views.deleteItem),
    path('testcases/', views.getTestcases),
    path('add-testcase/', views.addTestcases),
    path('update-testcase/<int:pk>/', views.updateTestcases),
    path('add-testresult/', views.addTestresult),
    path('scc-aws-result/', views.addSccAwsResult),
    path('update-scc-aws-result/<str:pk>/', views.updateSccAwsTestresult),
    path('scc-azure-result/', views.addSccAzureResult),
    path('update-scc-azure-result/<str:pk>/', views.updateSccAzureTestresult),
    path('fcp-aws-result/', views.addFcpAwsResult),
    path('update-fcp-aws-result/<str:pk>/', views.updateFcpAwsTestresult),
    path('fcp-azure-result/', views.addFcpAzureResult),
    path('update-fcp-azure-result/<str:pk>/', views.updateFcpAzureTestresult),
    path('get-scc-aws-result/', views.getSccAwsResult),
    path('update-scc-aws-result/<str:pk>/', views.updateSccAwsTestresult),
    path('get-scc-aws/<str:pk>/result/', views.getSccAwsResult_by_cycle),
    path('get-scc-azure-result/', views.getSccAzureResult),
    path('get-scc-azure/<str:pk>/result/', views.getSccAzureResult_by_cycle),
    path('get-fcp-aws-result/', views.getFcpAwsResult),
    path('get-fcp-aws/<str:pk>/result/', views.getFcpAwsResult_by_cycle),
    path('get-fcp-azure-result/', views.getFcpAzureResult),
    path('get-fcp-azure/<str:pk>/result/', views.getFcpAzureResult_by_cycle),
    path('testresults/', views.getTestRunResult),
    path('add-release-testresult/', views.addSummarizeInRelease),
    path('add-release-testresult/<int:pk>/', views.updateTestresultInRelease),
    path('get-release-testresult/', views.getResultFromAllRelease),
    path('add-daily-testresult/', views.addDailyTestResult),
    path('get-daily-testresult/', views.ServiceResultListView),
    path('daily-testresult/create/', views.create_service_result),
    path('release-tag/create/', views.create_release_tag),
    path('get-release-tag/', views.getReleaseTag),
    path('update-release-tag/<str:pk>/', views.updateReleaseTag),
]