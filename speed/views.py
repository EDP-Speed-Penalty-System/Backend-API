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
def get_speed_limit(request,lat, long):
    # complaint_detail = StudentComplain.objects.get(id=detailcomp_id1)
    speed_detail = SpeedLimit.objects.all()
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
    return Response(data=response,status=status.HTTP_200_OK)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def penalty(request, username=None):
    if request.method == 'GET':
        user = get_object_or_404(User, username=username) if username else request.user
        penalty = Penalty.objects.filter(user=user)
        penalties = serializers.PenaltySerializer(penalty,many=True).data
        resp = {
            'penalties' : penalties,
        }
        print(resp)
        return Response(data=resp,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        user = get_object_or_404(User ,username=request.user.username)
        serializer = serializers.PenaltySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def penalty(request):

#     if request.method == 'GET':
#         user = get_object_or_404(User ,username=request.user.username)
#         penalty = Penalty.objects.filter(user=user)
#         penalties = serializers.PenaltySerializers(penalty,many=True).data
#         resp = {
#             'penalties' : penalties,
#         }
#         return Response(data=resp,status=status.HTTP_200_OK)
    
#     elif request.method == 'POST':
#         user = get_object_or_404(User ,username=request.user.username)
#         serializer = serializers.PenaltySerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def student_complain_api(request):
#     user = get_object_or_404(User,username = request.user.username)
#     user = ExtraInfo.objects.all().filter(user = user).first()
#     if user.user_type == 'student':
#         complain = StudentComplain.objects.filter(complainer = user)
#     elif user.user_type == 'staff':
#         staff = ExtraInfo.objects.get(id=user.id)
#         staff = Caretaker.objects.get(staff_id=staff)
#         complain = StudentComplain.objects.filter(location = staff.area)
#     elif user.user_type == 'faculty':
#         faculty = ExtraInfo.objects.get(id=user.id)
#         faculty = Supervisor.objects.get(sup_id=faculty)
#         complain = StudentComplain.objects.filter(location = faculty.area)
#     complains = serializers.StudentComplainSerializers(complain,many=True).data
#     resp = {
#         'student_complain' : complains,
#     }
#     return Response(data=resp,status=status.HTTP_200_OK)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def create_complain_api(request):
#     serializer = serializers.StudentComplainSerializers(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE','PUT'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def edit_complain_api(request,c_id):
#     try: 
#         complain = StudentComplain.objects.get(id = c_id) 
#     except StudentComplain.DoesNotExist: 
#         return Response({'message': 'The Complain does not exist'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'DELETE':
#         complain.delete()
#         return Response({'message': 'Complain deleted'},status=status.HTTP_404_NOT_FOUND)
#     elif request.method == 'PUT':
#         serializer = serializers.StudentComplainSerializers(complain,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def worker_api(request):

#     if request.method == 'GET':
#         worker = Workers.objects.all()
#         workers = serializers.WorkersSerializers(worker,many=True).data
#         resp = {
#             'workers' : workers,
#         }
#         return Response(data=resp,status=status.HTTP_200_OK)

#     elif request.method =='POST':
#         user = get_object_or_404(User ,username=request.user.username)
#         user = ExtraInfo.objects.all().filter(user = user).first()
#         try :
#             caretaker = Caretaker.objects.get(staff_id=user)
#         except Caretaker.DoesNotExist:
#             return Response({'message':'Logged in user does not have the permissions'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#         serializer = serializers.WorkersSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE','PUT'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def edit_worker_api(request,w_id):
#     user = get_object_or_404(User ,username=request.user.username)
#     user = ExtraInfo.objects.all().filter(user = user).first()
#     try :
#         caretaker = Caretaker.objects.get(staff_id=user)
#     except Caretaker.DoesNotExist:
#         return Response({'message':'Logged in user does not have the permissions'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#     try: 
#         worker = Workers.objects.get(id = w_id) 
#     except Workers.DoesNotExist: 
#         return Response({'message': 'The worker does not exist'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'DELETE':
#         worker.delete()
#         return Response({'message': 'Worker deleted'},status=status.HTTP_404_NOT_FOUND)
#     elif request.method == 'PUT':
#         serializer = serializers.WorkersSerializers(worker,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def caretaker_api(request):

#     if request.method == 'GET':
#         caretaker = Caretaker.objects.all()
#         caretakers = serializers.CaretakerSerializers(caretaker,many=True).data
#         resp = {
#             'caretakers' : caretakers,
#         }
#         return Response(data=resp,status=status.HTTP_200_OK)
    
#     elif request.method == 'POST':
#         user = get_object_or_404(User ,username=request.user.username)
#         user = ExtraInfo.objects.all().filter(user = user).first()
#         try :
#             supervisor = Supervisor.objects.get(sup_id=user)
#         except Supervisor.DoesNotExist:
#             return Response({'message':'Logged in user does not have the permissions'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#         serializer = serializers.CaretakerSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

# @api_view(['DELETE','PUT'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def edit_caretaker_api(request,c_id):
#     user = get_object_or_404(User ,username=request.user.username)
#     user = ExtraInfo.objects.all().filter(user = user).first()
#     try :
#         supervisor = Supervisor.objects.get(sup_id=user)
#     except Supervisor.DoesNotExist:
#         return Response({'message':'Logged in user does not have the permissions'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#     try: 
#         caretaker = Caretaker.objects.get(id = c_id) 
#     except Caretaker.DoesNotExist: 
#         return Response({'message': 'The Caretaker does not exist'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'DELETE':
#         caretaker.delete()
#         return Response({'message': 'Caretaker deleted'},status=status.HTTP_404_NOT_FOUND)
#     elif request.method == 'PUT':
#         serializer = serializers.CaretakerSerializers(caretaker,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def supervisor_api(request):

#     if request.method == 'GET':
#         supervisor = Supervisor.objects.all()
#         supervisors = serializers.SupervisorSerializers(supervisor,many=True).data
#         resp = {
#             'supervisors' : supervisors,
#         }
#         return Response(data=resp,status=status.HTTP_200_OK)
    
#     elif request.method == 'POST':
#         user = get_object_or_404(User,username=request.user.username)
#         if user.is_superuser == False:
#             return Response({'message':'Logged in user does not have permission'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#         serializer = serializers.SupervisorSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
# @api_view(['DELETE','PUT'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def edit_supervisor_api(request,s_id):
#     user = get_object_or_404(User,username=request.user.username)
#     if user.is_superuser == False:
#         return Response({'message':'Logged in user does not have permission'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#     try: 
#         supervisor = Supervisor.objects.get(id = s_id) 
#     except Supervisor.DoesNotExist: 
#         return Response({'message': 'The Caretaker does not exist'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'DELETE':
#         supervisor.delete()
#         return Response({'message': 'Caretaker deleted'},status=status.HTTP_404_NOT_FOUND)
#     elif request.method == 'PUT':
#         serializer = serializers.SupervisorSerializers(supervisor,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

