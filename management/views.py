from django.views.generic import ListView, DetailView, View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task, Message, Role, Assignment
from .forms import ProjectForm, AddMemberForm, TaskForm


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
        # Añadir .distinct() al final es la clave
        return Project.objects.filter(assignment__user=self.request.user).distinct()
    
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
    

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  
    template_name = 'registration/signup.html'



class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'management/project_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # 1. Guardamos el proyecto primero (se guarda en self.object)
        response = super().form_valid(form)

        # 2. Buscamos (o creamos por seguridad) el rol de 'Admin'
        admin_role, _ = Role.objects.get_or_create(
            name='Admin', 
            defaults={'can_edit': True}
        )

        # 3. Asignamos al usuario actual como Admin de este nuevo proyecto
        Assignment.objects.create(
            user=self.request.user,
            project=self.object,
            role=admin_role
        )

        return response



class AddMemberView(LoginRequiredMixin, CreateView):
    model = Assignment
    form_class = AddMemberForm
    template_name = 'management/add_member.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project_id'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        
        # SEGURIDAD: Verificar que quien hace la petición es Admin del proyecto
        user_role = project.get_user_role(self.request.user)
        if not user_role or not user_role.can_edit:
            # Si no es admin, no le dejamos añadir a nadie (podrías redirigir a una página de error)
            return redirect('project_detail', pk=project.id)

        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['pk']})
    

# CREAR TAREA
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'management/task_form.html'

    def get_form_kwargs(self):
        # Pasamos el ID del proyecto al formulario para filtrar usuarios
        kwargs = super().get_form_kwargs()
        kwargs['project_id'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        # Asignamos el proyecto automáticamente antes de guardar
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['pk']})

# EDITAR TAREA (Asignar, cambiar nombre, etc)
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'management/task_form.html'

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})

# ELIMINAR TAREA
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'management/task_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})