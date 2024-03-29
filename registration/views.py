from django.shortcuts import render
from rest_framework.views import APIView
from . serializers import UserRegister,UserDataSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

# Create your views here.

class register(APIView):
    '''FUNCTIONALITY OF REGISTER'''
    def post(self,request,format=None):
        serializer = UserRegister(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['response']='registerd'
            data['username']=account.username
            data['email']=account.email
            token,create=Token.objects.get_or_create(user=account)
            data['token']=token.key
        else:
            data=serializer.errors
        return Response(data)   
    
class welcome(APIView):
    
    permission_classes=(IsAuthenticated,)
    
    def get(self,request):
        content={'user':str(request.user),'userid':str(request.user.id)}
        return Response(content)
    
class userDetails(APIView):
    '''FUNCTIONALITY OF GETTING USERS LIST'''
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise Http404
    def get(self,request,pk,format=None):
        userData=self.get_object(pk)
        serializer=UserDataSerializer(userData)
        return Response(serializer.data)
    
    def put(self,request,pk,format=None):
        userData=self.get_object(pk)
        serializer=UserDataSerializer(userData,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'error','error':serializer.errors})
    
    def delete(self,request,pk,format=None):
        userData=self.get_object(pk)
        userData.delete()
        return Response({'message':'user deleted'})
    
class setPagination(PageNumberPagination):
    page_size=10
    
class paginationApi(ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserDataSerializer
    pagination_class=setPagination
    filter_backends=(SearchFilter,)
    search_fields=('username','email','first_name','last_name')
