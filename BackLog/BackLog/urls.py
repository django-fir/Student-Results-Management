"""BackLog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
admin.site.site_header = "Student Results Management"
admin.site.site_title = "Student Results Management Admin"
urlpatterns = [
    path('admin/', admin.site.urls),
    # path("", views.index),
    path("home/<key>", views.home),
    path("gen/", views.original_data),
    path("search/<key>", views.get_student_details),
    path("query/<key>", views.search_query),
    path("searchstudent/", views.search),
    # path("result/<branch>/<code>/<api>/<headders>", views.get_results),
    path("result/<branch>/<code>/", views.get_results),
    # path("result/<branch>/<code>/<api>/", views.get_results),
    path("stu/", views.add_students),
    path("chat/", views.chat_bot),
    path("chat1/", views.result_insights),
    path("grafh/", views.graph_student),
    path("wsearch/", views.wasup_search),
    path("wget/", views.wasup_info),

]
