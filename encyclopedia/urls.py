from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.pageInfo, name="pageInfo"),
    path("search/", views.searchRes,name="searchRes"),
    path("new/",views.newEntry, name="newEntry"),
    path("verifyPage",views.verifyEntry,name="verifyEntry"),
    path("editPage/<str:title>",views.editPage,name="editPage"),
    path("editEntry",views.editEntry,name ="editEntry"),
    path("randomPage",views.randomPage,name = "randomPage")

]
