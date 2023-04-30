from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import SpeedLimit, UserInfo, Vehicle, Penalty
from . import serializers
from geopy.distance import geodesic
from .utils import get_and_authenticate_user
from rest_framework.generics import ListAPIView
from django.http import JsonResponse

User = get_user_model()

# Create your views here.

class StudentList(ListAPIView):
  queryset = Penalty.objects.all()
  serializer_class = serializers.PenaltySerializer
  

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = serializers.UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_and_authenticate_user(**serializer.validated_data)
    data = serializers.AuthUserSerializer(user).data
    resp = {
        'last_name': user.last_name,
        'success' : 'True',
        'message' : 'User logged in successfully',
        'token' : data['auth_token']
    }
    return Response(data=resp, status=status.HTTP_200_OK)

@api_view(['POST'])
def logout(request):
    if request.user.is_authenticated:
        request.user.auth_token.delete()
        resp = {
            'message': 'User logged out successfully'
        }
        return Response(data=resp, status=status.HTTP_200_OK)
    else:
        return Response(data={'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def profile(request, username=None):
    user = get_object_or_404(User, username=username) if username else request.user
    user_detail = serializers.UserSerializer(user).data
    user_info = UserInfo.objects.get(user=user)
    profile = serializers.UserInfoSerializers(user_info).data
    resp = {
        'user' : user_detail,
        'profile' : profile,
    }
    print(resp)
    return Response(data=resp, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_speed_limit(request):
    # complaint_detail = StudentComplain.objects.get(id=detailcomp_id1)
    speed_detail = SpeedLimit.objects.all()
    lat = request.headers.get('lat')
    long = request.headers.get('long')
    point = (lat, long)
  
# Print the distance calculated in km
    speed = 200
    dist = 10000
    for i in speed_detail:
        p = (i.latitude, i.longitude)
        if(geodesic(point, p) < dist):
                dist = geodesic(point, p)
                speed = i.limit

    response = {
        'speed_limit' : speed
    }
    # print(lat)
    # print(long)
    print(response)
    return Response(data=response,status=status.HTTP_200_OK)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def penalty(request, username=None):
    if request.method == 'GET':
        user = get_object_or_404(User, username=username) if username else request.user
        register_no = request.headers.get('register-no')
        print(register_no)
        vehicle = get_object_or_404(Vehicle, register_no=register_no)
        penalty = Penalty.objects.filter(user=user, vehicle=vehicle)
        penalties = serializers.PenaltySerializer(penalty,many=True).data
        resp = {
            'penalties' : penalties,
        }
        print(resp)
        return Response(data=resp,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        user = get_object_or_404(User ,username=request.user.username)
        print(request.data)
        data = request.data.copy()  # create a copy of the data dictionary
        data['user'] = user.id
        serializer = serializers.PostPenaltySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def vehicles(request, username=None):
    if request.method == 'GET':
        user = get_object_or_404(User, username=username) if username else request.user
        vehicle = Vehicle.objects.filter(user=user)
        vehicles = serializers.VehicleSerializer(vehicle,many=True).data
        resp = {
            'vehicles' : vehicles,
        }
        print(resp)
        return Response(data=resp,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        user = get_object_or_404(User ,username=request.user.username)
        print(request.data)
        data = request.data.copy()  # create a copy of the data dictionary
        user = [user.id]
        data['user'] = user
        serializer = serializers.PostVehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 