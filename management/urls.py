from django.urls import path
from .views import ProjectDashboardView, ProjectDetailView, CompleteTaskView, AddMessageView, ProjectCreateView, AddMemberView, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('', ProjectDashboardView.as_view(), name='dashboard'),
    path('project/new/', ProjectCreateView.as_view(), name='create_project'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('task/<int:pk>/complete/', CompleteTaskView.as_view(), name='complete_task'),
    path('project/<int:pk>/add-task/', TaskCreateView.as_view(), name='add_task'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='edit_task'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_task'),
    path('project/<int:pk>/add-member/', AddMemberView.as_view(), name='add_member'),
    path('project/<int:pk>/message/', AddMessageView.as_view(), name='add_message'),
]