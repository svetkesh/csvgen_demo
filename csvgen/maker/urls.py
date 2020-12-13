from django.urls import path

from . import views

urlpatterns = [
    path('schema/', views.SchemaListView.as_view()),
    path('', views.SchemaListView.as_view(), name='schema_list'),

    path('schema/<int:pk>', views.SchemaDetailView.as_view(), name='schema_detail'),
    path('schema/new/', views.CreateSchemaView.as_view(), name='schema_new'),
    path('schema/<int:pk>/edit/', views.SchemaUpdateView.as_view(), name='schema_edit'),
    path('schema/<int:pk>/remove/', views.SchemaDeleteView.as_view(), name='schema_remove'),

    path('schema/<int:pk>/column/', views.add_column_to_schema, name='add_column_to_schema'),

    path('column/<int:pk>/edit/', views.column_edit, name='column_edit'),
    path('column/<int:pk>/remove/', views.column_remove, name='column_remove'),

    path("tasks/<task_id>/", views.get_status, name="get_status"),
    path("tasks/", views.run_task, name="run_task"),
]
