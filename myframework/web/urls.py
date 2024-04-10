from django.urls import path
from web import views
# from product.views import search, get_api_data, task_detail, task_list, create_post, task_delete, run_robot_command



urlpatterns = [
    path('', views.index, name="home"),
    # path('login/', views.loginPage, name="login"),
    # path('logout/', views.logoutUser, name="logout"),
    # path('testcases/', views.get_all_testcases),
    # path('testresult/', views.get_test_result),
    # path('<str:cycle_id>/', views.get_testresult_by_cycleid)
]