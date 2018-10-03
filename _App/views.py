from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.shortcuts import render
from .models import *
from .forms import *

from django.db.models import Q

# 시작 페이지
class StartPage(APIView):
    
    def get(self, request, format=None):

        return render(request, "Start/Start.html", {})    

# 메인 페이지
class HomePage(APIView):
    
    def get(self, request, format=None):

        form = SearchForm()
        
        writePostDatas = WritePostModel.objects.all()[:9]
        context = { 'writePostDatas' : writePostDatas, 'form': form }

        return render(request, "Main/Main.html", context )

class ListSearchPage(APIView):

    #검색, 해쉬태그
    def post(self, request, format=None):

        form = SearchForm(request.POST)

        if form.is_valid():
            word = form.data['word']

            writeposts = WritePostModel.objects.all()
            writepost_li = []

            for i in writeposts:
                for j in i.tags.all():
                    if str(j) == str(word):
                        writepost_hash = WritePostModel.objects.all().filter(images=i)
                        writepost_li.append(writepost_hash)

            writepost = WritePostModel.objects.filter(
                Q(content__icontains=word)
            ).distinct() 

            writepost_li.append(writepost)

            writepost_li = list(set(writepost_li))
            
            print(writepost_li)

            return render(request, "Search/Search.html", {'writepost': writepost_li })

        return Response(status=status.HTTP_201_CREATED)
    
    def get(self, request, format=None):

        form = SearchForm()

        return render(request, "Search/Search.html", {'form': form})

#리스트 페이지
class ListPage(APIView):

    #리스트 보여줌
    def get(self, request, format=None):

        form = SearchForm()

        return render(request, "List/List.html", {'form': form})
    
    def post(self, request, format=None):

        form = SearchForm(request.POST)
           
        if form.is_valid():
            word = form.data['word']
            
            writepost = WritePostModel.objects.filter( Q(content__icontains=word) ).distinct() 

            return render(request, "List/List.html", {'writepost': writepost} )

    

# 리스트 디테일 페이지
class ListDetailPage(APIView):

    # 모든 유저 게시물
    def find_post(self, post_id):
        
        print("Hello2")
        try:
            writePost = WritePostModel.objects.get(id=post_id)
            return writePost

        except WritePostModel.DoesNotExist:
            return None
    
        except WritePostModel.DoesNotExist:
            return None

    def get(self, request, post_id, format=None):

        writePostData = self.find_post(post_id)
       
        context = { 'writePostData' : writePostData }

        print(writePostData)
        print("Hello")

        return render(request, "Detail/Detail.html", context)


# # 리스트 만드는 페이지
class ListCreatePage(APIView):

    def post(self, request, format=None): 

        user = request.user

        form = WritePostForm(user, request.POST, request.FILES)

        if form.is_valid():
            user = form.cleaned_data['user']
            tags = form.cleaned_data['tags']
            
            WritePostForm(request.FILES['images'])
        
            WritePost = WritePostModel(pk=user.pk)

            form.save()
            
            WritePost.tags.add(*tags)

        return redirect('App:home')

    def get(self, request, format=None):

        user = request.user

        form = WritePostForm(user)

        return render(request, "Create/Create.html", {'form': form})


#회원가입
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUp(generic.CreateView):

    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


    