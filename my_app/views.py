# Import necessary modules and classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CustomUser, Task, Category
from .serializers import UserSerializer, TaskSerializer, CategorySerializer
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from django.http import JsonResponse

# View function for user registration
@api_view(['POST'])
def user_register(request):
    # Validate and save user data using UserSerializer
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View function for user login
@api_view(['POST'])
def user_login(request):
    # Get username and password from request data
    username = request.data.get('username')
    password = request.data.get('password')

    # Find the user based on the provided username
    user = CustomUser.objects.filter(username=username).first()

    if user is not None and user.check_password(password):
        # If the user is found and the password is correct, generate a token
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'id': user.id,
                'username': user.username,
                'message': 'Login successful!',
            },
            status=status.HTTP_200_OK
        )
    else:
        # If the user is not found or the password is incorrect, return an error response
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

# View class for listing and creating tasks
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# View class for retrieving, updating, and deleting a specific task
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# View class for listing and creating categories
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# View class for retrieving, updating, and deleting a specific category
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# View class for listing tasks created by a specific user
class TasksCreatedByUser(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Task.objects.filter(created_by=user_id).order_by('-id')

# View function for retrieving categories associated with a specific user
@api_view(['GET'])
def get_user_categories(request, user_id):
    try:
        # Retrieve the categories associated with the user_id
        categories = Category.objects.filter(user=user_id)
        # Serialize the categories data
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# View function for retrieving user details
def user_detail(request, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        data = {
            "message": "User found",
            "user_id": user.id,
            "username": user.username,
        }
        return JsonResponse(data, status=200)
    except User.DoesNotExist:
        data = {"error": "User not found"}
        return JsonResponse(data, status=404)
    except Exception as e:
        data = {"error": str(e)}
        return JsonResponse(data, status=500)

# View function for deleting a user
def delete_user(request, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return JsonResponse({"message": "User deleted successfully"}, status=204)
    except User.DoesNotExist:
        data = {"error": "User not found"}
        return JsonResponse(data, status=404)
    except Exception as e:
        data = {"error": str(e)}
        return JsonResponse(data, status=500)
