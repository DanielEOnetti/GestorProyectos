from django.urls import path
from .views import ProjectDashboardView, ProjectDetailView, CompleteTaskView, AddMessageView 

urlpatterns = [
    path('', ProjectDashboardView.as_view(), name='dashboard'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('task/<int:pk>/complete/', CompleteTaskView.as_view(), name='complete_task'),
    
    
    path('project/<int:pk>/message/', AddMessageView.as_view(), name='add_message'),
]