from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task, Message


class ProjectDashboardView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'management/dashboard.html'
    context_object_name = 'projects'

    def get_queryset(self):
        
        return Project.objects.filter(assignment__user=self.request.user)

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        
        for project in context['projects']:
            project.mi_rol_actual = project.get_user_role(self.request.user)
            
        return context
    

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'management/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        # Seguridad: Solo permite ver proyectos donde el usuario tiene asignación
        return Project.objects.filter(assignment__user=self.request.user)
    
class CompleteTaskView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        project = task.project
        
        # VERIFICAR PERMISOS
        # Obtenemos el rol del usuario en ESTE proyecto
        user_role = project.get_user_role(request.user)
        is_admin = (user_role and user_role.can_edit)
        is_assigned = (task.assigned_to == request.user)

        # Solo guardamos si es admin o si es su tarea asignada
        if is_admin or is_assigned:
            task.status = 'DONE'
            task.save()
        
        
        return redirect('project_detail', pk=project.id)
    

class AddMessageView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        content = request.POST.get('content')
        
        if content:
            Message.objects.create(
                project=project,
                user=request.user,
                content=content
            )
        
        return redirect('project_detail', pk=pk)