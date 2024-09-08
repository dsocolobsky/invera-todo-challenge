from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import User, Task
from .serializers import UserSerializer, TaskSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .authentication import BearerTokenAuthentication


class TaskFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    description = filters.CharFilter(lookup_expr="icontains")
    completed = filters.BooleanFilter()
    created_at = filters.DateFromToRangeFilter()
    userid = filters.NumberFilter(field_name="user__id")
    username = filters.CharFilter(field_name="user__username")

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "completed",
            "created_at",
            "user",
            "username",
        ]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AllTaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BearerTokenAuthentication]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter

    def list(self, request, *args, **kwargs):
        if not request.user or request.user.username != "admin":
            return Response(
                {"error": "Authentication header is missing"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return super().list(request, *args, **kwargs)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BearerTokenAuthentication]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response(
                {"error": "Authentication header is missing"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Both username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "A user with this username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.create_user(username=username, password=password)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CreateAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.pk, "username": user.username}
        )
