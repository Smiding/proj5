# Import required modules from Django
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Custom User Manager to handle user creation and superuser creation
class CustomUserManager(BaseUserManager):
    # Method to create a regular user
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        # Normalize email address and create a user instance
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Method to create a superuser
    def create_superuser(self, username, email, password=None):
        # Create a regular user first
        user = self.create_user(email=email, username=username, password=password)
        # Set the user as a staff member and superuser
        user.is_staff = True
        user.is_superuser = True
        user.date_joined = timezone.now()
        user.save(using=self._db)
        return user

# Custom User model, inheriting from AbstractBaseUser and PermissionsMixin
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Fields for username, email, and date joined
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Boolean fields for staff and superuser status
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # CustomUserManager as the model's objects manager
    objects = CustomUserManager()

    # USERNAME_FIELD specifies the field used as the unique identifier for login
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS specifies additional required fields during user creation
    REQUIRED_FIELDS = ['email']

    # Custom delete method to handle related objects deletion
    def delete(self, *args, **kwargs):
        # Handle the deletion of related tasks first
        tasks = Task.objects.filter(created_by=self)
        # Delete all associated tasks
        tasks.delete()

        # Get all categories associated with the user
        categories = Category.objects.filter(user=self)
        # Delete all associated categories
        categories.delete()

        # Call the original delete method to delete the user
        super().delete(*args, **kwargs)

    # String representation of the user model (username)
    def __str__(self):
        return self.username

# Category model to represent task categories
class Category(models.Model):
    # ForeignKey to CustomUser to associate a user with a category
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=-1)
    name = models.CharField(max_length=100)

    # String representation of the category model (category name)
    def __str__(self):
        return self.name

# Task model to represent tasks
class Task(models.Model):
    # Choices for task states and priorities
    STATE_CHOICES = (
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )

    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )

    # ForeignKey to CustomUser to associate a user with a task
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks_created', default=-1)

    # Fields for task details
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='New')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')

    # String representation of the task model (task title)
    def __str__(self):
        return self.title
