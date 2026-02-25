from django import forms
from .models import Project, Assignment, User, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proyecto'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción breve', 'rows': 3}),
        }


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['user', 'role']
        labels = {
            'user': 'Seleccionar Usuario',
            'role': 'Rol a asignar'
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Extraemos el proyecto para filtrar usuarios (opcional, pero recomendado)
        self.project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)
        
        # Opcional: Aquí podrías filtrar para no mostrar usuarios que YA están en el proyecto
        # Pero por simplicidad, dejaremos que muestre todos los usuarios.
        self.fields['user'].queryset = User.objects.all()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'assigned_to', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Recibimos el project_id para filtrar usuarios
        project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)
        
        if project_id:
            # Si estamos creando, filtramos por el ID que pasamos
            self.fields['assigned_to'].queryset = User.objects.filter(assignment__project_id=project_id)
        elif self.instance.pk:
            # Si estamos editando, filtramos por el proyecto de la tarea existente
            self.fields['assigned_to'].queryset = User.objects.filter(assignment__project=self.instance.project)