from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import Question
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from urllib.parse import urlencode

# Create your views here.

def top(request):
    return render(request,'top.html')

def signup(request):
    if request.method=='POST':
        username=request.POST['username_data']
        email=request.POST['email_data']
        password=request.POST['password_data']
        try:
            User.objects.create_user(username,email,password)
        except IntegrityError:
            return render(request,'signup.html',{'error':'このユーザー名は既に登録されています。'})
    else:
        return render(request,'signup.html',{})

    return redirect('signup_success')

def signup_success(request):
    return render(request,'signup_success.html')


def loginview(request):
    if request.method=='GET':
        if request.GET.get('error'):
            return render(request,'login.html',{'error':'このユーザーは登録されていません。'})
    if request.method=='POST':
        username=request.POST['username_data']
        password=request.POST['password_data']
        print(username)
        print(password)
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            redirect_url=reverse('loginview')
            parameter=urlencode({'error':'1'})
            url=f'{redirect_url}?{parameter}'
            #return render(request,'login.html',{'error':'このユーザーは登録されていません。'})
            return redirect(url)
    return render(request,'login.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('top')
    if 'ques_num' in request.session:
        request.session['ques_num']=0

    if 'ans_num' in request.session:
        request.session['ans_num']=0

    return render(request,'home.html')

def question(request):
    if not request.user.is_authenticated:
        return redirect('top')
    #現在の出題数
    if 'ques_num' in request.session:
        request.session['ques_num']+=1
        #本番では消す
        #if request.session['ques_num']==6:
        #    request.session['ques_num']=1
    else:
        request.session['ques_num']=1
    #正解数
    if not 'ans_num' in request.session:
        request.session['ans_num']=0
    
    print(request.session['ques_num'])
    print(request.session['ans_num'])
    ans_num=request.session['ans_num']
    question=Question.objects.get(pk=request.session['ques_num'])

    return render(request,'question.html',{'question':question,'ans_num':ans_num})

def answer(request,ans):
    #ログインしていなかったらトップ画面へ
    if not request.user.is_authenticated:
        return redirect('top')
    #現在の問題数
    answer=Question.objects.get(pk=request.session['ques_num'])
    #現在の正解数
    if answer.answer==ans:
        request.session['ans_num']+=1
    ans_num=request.session['ans_num']
    #レコード数を格納 
    record_num=Question.objects.all().count()
    #最終問題かチェック
    if request.session['ques_num']==record_num:
        return render(request,'answer.html',{'answer':answer,'ans_num':ans_num,'flg':1})

    return render(request,'answer.html',{'answer':answer,'ans_num':ans_num,'flg':0})

def result(request):
    ans_num=request.session['ans_num']
    request.session['ans_num']=0
    request.session['ques_num']=0
    return render(request,'result.html',{'ans_num':ans_num})

def logoutview(request):
    logout(request)
    return redirect('logout_success')

def logout_success(request):
    return render(request,'logout_success.html')