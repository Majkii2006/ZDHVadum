from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("person/", views.person, name="person"),
    path("schedule/", views.schedule, name="schedule"),
    path("schedule/add", views.add_schedule, name="add_schedule"),
    path("schedule/<int:id>/delete", views.delete_schedule, name="delete_schedule"),
    path("docs/", views.docs, name="docs"),
    path("outlines/", views.outlines, name="outlines"),
    path("outlines/add", views.add_outline, name="add_outline"),
    path("outlines/<int:id>/download", views.download_outline, name="download_outline"),
    path("outlines/<int:id>/show", views.show_outline, name="show_outline"),
    path("outlines/<int:id>/delete", views.delete_outline, name="delete_outline"),
    path('payments/', views.payments, name="payments"),
    path('payments/<int:id>/installment', views.installment, name="installment"),
    path('payments/<int:id>/entire_amount', views.entire_amount, name="entire_amount"),
    path("person/cadre", views.cadre, name="cadre"),
    path("person/cadre/add", views.add_cadre, name="add_cadre"),
    path("person/cadre/<int:id>/edit", views.edit_cadre, name="edit_cadre"),
    path("person/cadre/<int:id>/delete", views.delete_cadre, name="delete_cadre"),
    path("person/participants", views.participants, name="participants"),
    path("person/participants/add", views.add_participant, name="add_participant"),
    path("person/participants/<int:id>/edit", views.edit_participant, name="edit_participant"),
    path("person/participants/<int:id>/delete", views.delete_participant, name="delete_participant")
    
]