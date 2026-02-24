from django.contrib import admin
from .models import Project, Task, Role, Assignment

# Esto permite editar las tareas directamente dentro de la vista del Proyecto
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

# Esto permite asignar usuarios y roles dentro de la vista del Proyecto
class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'get_progress_display')
    inlines = [AssignmentInline, TaskInline]

    def get_progress_display(self, obj):
        return f"{obj.get_progress()}%"
    get_progress_display.short_description = 'Avance'

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'can_edit')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'assigned_to')
    list_filter = ('status', 'project')