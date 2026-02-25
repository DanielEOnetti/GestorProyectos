from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_user_role(self, user):
        assignment = Assignment.objects.filter(project=self, user=user).first()
        return assignment.role if assignment else None

    #Metodo para el reto opcional
    def get_progress(self):
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0
        done_tasks = self.tasks.filter(status='DONE').count()
        return (done_tasks / total_tasks) * 100

    def __str__(self):
        return self.name
    

class Role(models.Model):
    # Ejemplo: Admin, Editor, Viewer
    name = models.CharField(max_length=50)
    can_edit = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'project')

class Task(models.Model):
    STATUS_CHOICES = [('TODO', 'To Do'), ('IN_PROG', 'In Progress'), ('DONE', 'Done')]
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='TODO')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)



class Message(models.Model):
    project = models.ForeignKey(Project, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"