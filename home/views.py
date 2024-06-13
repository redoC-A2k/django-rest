from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from .serializers import peopleSerializer, LoginSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class LoginAPI(APIView):
    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"status": False, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            return Response(
                {"status": False, "message": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token,_  = Token.objects.get_or_create(user = user)
        return Response({"status": True, "message": "Login successful", "token": str(token)}, status=status.HTTP_201_CREATED)

class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"status": False, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            {"status": True, "message": "User created successfully"},
            status=status.HTTP_201_CREATED,
        )


# Create your views here.
@api_view(["GET", "POST"])
def index(request):
    courses = {
        "course_name": "python",
        "learn_key": ["flask", "Django", "Tornado"],
        "course_provider": "Scaler",
    }
    if request.method == "GET":
        print("You hit a get method")
        print(request.GET.get("question"))
        return Response(courses)
    elif request.method == "POST":
        print("You hit a post method")
        data = request.data
        print("Data is", data)
        return Response(courses)


class PersonApi(APIView):
    def get(self, request):
        objs = Person.objects.filter(color__isnull=False)
        serializer = peopleSerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = peopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def put(self, request):
        data = request.data
        obj = Person.objects.get(id=data["id"])
        serializer = peopleSerializer(
            obj,
            data=data,
        )
        if serializer.is_valid():
            print("Data is", serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id=data["id"])
        serializer = peopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id=data.get("id"))
        obj.delete()
        return Response({"message": "Deleted"})


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def person(request):
    print("Request method is", request.method)
    if request.method == "GET":
        objs = Person.objects.filter(color__isnull=False)
        serializer = peopleSerializer(objs, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        serializer = peopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    elif request.method == "PUT":
        data = request.data
        obj = Person.objects.get(id=data["id"])
        serializer = peopleSerializer(
            obj,
            data=data,
        )
        if serializer.is_valid():
            print("Data is", serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    elif request.method == "PATCH":
        data = request.data
        obj = Person.objects.get(id=data["id"])
        serializer = peopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    else:
        data = request.data
        obj = Person.objects.get(id=data.get("id"))
        obj.delete()
        return Response({"message": "Deleted"})


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = peopleSerializer
    queryset = Person.objects.all()

    def list(self, request):
        search = request.GET.get("search")
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)
        serializer = peopleSerializer(queryset, many=True)
        return Response(
            {"status": 200, "data": serializer.data}, status=status.HTTP_404_NOT_FOUND
        )
