from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404, reverse,HttpResponse,HttpResponseRedirect
from .models import *
import hashlib 
import datetime
import re
from django.http import JsonResponse
from django.views.generic import ListView,View
from django.contrib import messages

def get_sea(request):
    seas_all = Seainp.objects.all().order_by('-all')[:10]
    if request.user.is_active:
        seas_ind =  Search.objects.filter(user=request.user).order_by('-sea_date')[:10]
        return seas_ind,seas_all
    return False, seas_all


def home(request):
    context={}
    context['page_title'] = 'lincart.in'
    dashboard = {'n':'Dashboard','w':'dashboard'}
    posts = {'n': 'Products','w':'posts'}
    uploadpost = {'n': 'Sell Products', 'w':'uploadpost'}
    notifications = {'n' : 'Notifications/Messages' , 'w': 'notifications'}
    liked = {'n':'Liked', 'w': 'liked'}
    settings = {'n' : 'Settings', 'w':'settings'}
    navss = [posts, uploadpost, notifications,settings, dashboard]
    context['navss'] = navss
    context['seas_ind'], context['seas_all'] = get_sea(request)
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context['data'] = data
    posts = Post.objects.filter(sell=False)
    context['posts'] = posts
    imgs = PostImage.objects.all()
    context['imgs'] = imgs
    return render(request, 'blog/base.html',context)

def search(request):
    print('search')
    context = {}
    sea = request.GET['b'] 
    sea = str(sea)
    context['page_title'] = sea
    dashboard = {'n':'Dashboard','w':'dashboard'}
    posts = {'n': 'Products','w':'posts'}
    uploadpost = {'n': 'Sell Products', 'w':'uploadpost'}
    notifications = {'n' : 'Notifications/Messages' , 'w': 'notifications'}
    liked = {'n':'Liked', 'w': 'liked'}
    settings = {'n' : 'Settings', 'w':'settings'}
    navss = [posts, uploadpost, notifications,settings, dashboard]
    context['navss'] = navss
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context['data'] = data
    if sea=='':
        return redirect('/')
    else:
        rejec = ['','a','an','the','is','are','or','and','can','could','may','might','then','if','this','that','these','those','it','he','she','to','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','as','you','of','in','has','will','we','by','us','our','its''your','all','for','on','at','his']
        sea_split = re.findall(r'[a-z0-9]*',sea.lower())
        while '' in sea_split:
            sea_split.remove('')
        print(sea_split)
        #posts = Post.objects.all().filter(post_title=sea)
        posts = Post.objects.filter(sell=False)
        post_sec = []
        for post in posts:
            post_tit_spl = re.findall(r'[a-z0-9]*',post.post_title.lower())
            post_desc_spl = re.findall(r'[a-z0-9]*',post.desc.lower())
            all_post_words = post_tit_spl + post_desc_spl
            post_tit_spl = []
            for w in all_post_words:
                if w not in rejec:
                    post_tit_spl.append(w)
            while('' in post_tit_spl):
                post_tit_spl.remove('')
            print('post_tit_spl',post_tit_spl)
            for spl in sea_split:
                print(spl)
                for post_tit in post_tit_spl:
                    reg = re.findall(spl,post_tit)
                    if len(reg)>0:
                        print('reg',reg)
                        while('' in reg):
                            reg.remove('')
                        post_sec.append(post)
                    reg = re.findall(post_tit,spl)
                    if len(reg)>0:
                        print('reg',reg)
                        while('' in reg):
                            reg.remove('')
                        post_sec.append(post)
                
                reg = re.findall(spl,post.category)
                if len(reg)>0:
                    print('reg',reg)
                    while('' in reg):
                        reg.remove('')
                    post_sec.append(post)
                reg = re.findall(post.category,spl)
                if len(reg)>0:
                    print('reg',reg)
                    while('' in reg):
                        reg.remove('')
                    post_sec.append(post)
                    
        post_cou = {}
        for post in post_sec:
            k = post_sec.count(post)
            post_cou[post.id] = k
        post_cou = sorted(post_cou.items(),key=lambda kv: kv[1],reverse=True)
        print(post_cou)
        post_fin = []
        for post in post_cou:
            post_fin.append(Post.objects.get(id=post[0]))
        context['posts'] = post_fin
        print(post_fin)
        print(len(post_fin))
        #Seainps
        if len(Seainp.objects.filter(inp=sea))>0:
            seain = Seainp.objects.get(inp=sea)
        if request.user.is_active:
            if len(Seainp.objects.filter(inp=sea))==0:
                seain = Seainp.objects.create(inp=sea)
            seain.users.add(request.user)
            seain.all=seain.num_users()
            seain.save()
            if len(Search.objects.filter(inp=sea,user=request.user))>0:
                search = Search.objects.get(inp=sea,user=request.user)
            else:
                search = Search.objects.create(inp=sea,user=request.user)
            search.sea_date = datetime.datetime.now()
            search.save()
            context['seas_ind'] = Search.objects.filter(user=request.user).order_by('-sea_date')[:10]
        context['seas_all'] = Seainp.objects.all().order_by('-all')[:10]
        context['sea'] = sea
        imgs = PostImage.objects.all()
        context['imgs'] = imgs
    return render(request,'blog/base.html',context)

def user_login(request):
    print('user_login')
    if request.method=="POST":
        loc = request.POST["loc"]
        un = request.POST["username"]
        pwd = request.POST["password"]
        user = authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if len(register_table.objects.filter(user=request.user))>0:
                reg = register_table.objects.get(user=request.user)
                reg.login+=1
                reg.save()
                context = {'log_data':'Logged in Successfully'}
                messages.success(request, 'Logged in Successfully')
            if user.is_superuser:
                if loc=='home':
                    return redirect('/')
                else:
                    print('post')
                    return redirect('/post/'+loc)
            else:
                if loc=='home':
                    return redirect('/')
                else:
                    print('post')
                    return redirect('/post/'+loc)
                '''res = redirect('/')
                if "rememberme" in request.POST:
                    res.set_cookie("user_id",user.id)
                    res.set_cookie("date_login",datetime.now())
                return res'''
            # if user.is_active:
            #     return HttpResponseRedirect("/cust_dashboard")
                
        else:
            return redirect('/')


def logout(request):
    print('logout')
    if len(register_table.objects.filter(user=request.user))>0:
        reg = register_table.objects.get(user=request.user)
        reg.login-=1
        reg.save()
    auth.logout(request)
    return redirect('/')  

def register(request):
    print('register')
    if request.method=="POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        if password1==password2:
            if User.objects.filter(username=username).exists():
                return redirect('/')
            elif User.objects.filter(email=email).exists():
                return redirect('/')
            else:
                user = User.objects.create_user(username = username, password = password1, email = email,first_name = first_name, last_name = last_name)
                user.save()
                reg = register_table(user=user,email=email)
                reg.save()
                user = authenticate(username=username,password=password1)
                if user:
                    login(request,user)
                    return redirect('/')
        else:
            return redirect('/')

class check_user(View):
    def get(self,request):
        cname = request.GET.get('cname',None)
        data = {}
        print(cname)
        data['sen'] = ''
        if User.objects.filter(username=cname):
            data['sen'] = 'The username exists'
        return JsonResponse(data)


def about(request):
    context={}
    context['page_title'] = 'About'
    dashboard = {'n':'Dashboard','w':'dashboard'}
    posts = {'n': 'Products','w':'posts'}
    uploadpost = {'n': 'Sell Products', 'w':'uploadpost'}
    notifications = {'n' : 'Notifications/Messages' , 'w': 'notifications'}
    liked = {'n':'Liked', 'w': 'liked'}
    settings = {'n' : 'Settings', 'w':'settings'}
    navss = [posts, uploadpost, notifications,settings, dashboard]
    context['navss'] = navss
    #seain
    seain = Seainp.objects.all()
    context['seas_ind'], context['seas_all'] = get_sea(request)
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context['data'] = data
    return render(request,'blog/about.html',context)

def base(request,sec):
    context={}
    context['sec'] = sec
    try:
        context['chatters'] = chatters.objects.filter(user=request.user).order_by('-num')
    except:
        pass
    context['users'] = User.objects.all()
    dashboard = {'n':'Dashboard','w':'dashboard'}
    posts = {'n': 'Products','w':'posts'}
    uploadpost = {'n': 'Sell Products', 'w':'uploadpost'}
    notifications = {'n' : 'Notifications/Messages' , 'w': 'notifications'}
    liked = {'n':'Liked', 'w': 'liked'}
    settings = {'n' : 'Settings', 'w':'settings'}
    navs = [dashboard, posts, uploadpost, notifications, settings]
    context['navs'] = navs
    navss = [posts, uploadpost, notifications,settings, dashboard]
    context['navss'] = navss
    #seain
    seain = Seainp.objects.all()
    context['seas_ind'], context['seas_all'] = get_sea(request)
    t=0
    for nav in navs:
        if nav['w']==sec:
            context['page_title'] = nav['n']
            t=1
    if t==1:
        check = register_table.objects.filter(user__id=request.user.id)
        if len(check)>0:
            data = register_table.objects.get(user__id=request.user.id)
            context['data'] = data
            posts = Post.objects.filter(uname=request.user)
            context['posts'] = posts
            imgs = PostImage.objects.all()
            context['imgs'] = imgs
            return render(request,'blog/home.html',context)
        else:
            context['con'] = 'Please do Login to view'
            context['page_title'] = 'Error - 404'
            return render(request,'blog/error.html',context)
    else:
        context['con'] = 'This site do not exist'
        context['page_title'] = 'Error - 404'
        return render(request,'blog/error.html',context)

def sel_submit(request):
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
    if request.method == 'POST':
        post_title = None
        if "name" in request.POST:
            post_title  = request.POST['name']
        category = request.POST['cate']
        author = None
        if "author" in request.POST:
            author = request.POST['author']
        comp = None
        if "comp" in request.POST:
            comp = request.POST['comp']
        place = data.place
        Institute = data.Institute
        price = request.POST['price']
        if "desc" in request.POST:
            desc = request.POST['desc']
        label1 = None
        if "label1" in request.POST:
            label1 = request.POST['label1']
        inp1 = None
        if "inp1" in request.POST:
            inp1 = request.POST['inp1']
        label2 = None
        if "label2" in request.POST:
            label2 = request.POST['label2']
        inp2 = None
        if "inp2" in request.POST:
            inp2 = request.POST['inp2']
        upload = Post(uname=request.user,post_title=post_title,category=category,author=author,comp=comp,place=place,Institute=Institute,price=price,desc=desc,label1=label1,inp1=inp1,label2=label2,inp2=inp2)
        upload.save()
        images = request.FILES.getlist('cover')
        for img in images:
            image = PostImage(post=upload,cover=img)
            image.save()
        upload.sha = hashlib.sha1(str(upload.id).encode()).hexdigest()
        upload.save()
    return redirect('/uploadpost/')

def prof_update(request):
    context = {}
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        if request.method=="POST":
            fn = request.POST["first_name"]
            ln = request.POST["last_name"]
            em = request.POST["email"]
            con = request.POST["contact"]
            inst = request.POST['institute']
            place = request.POST["place"]
            occ = request.POST["occupation"]

            usr = User.objects.get(id=request.user.id)
            usr.first_name = fn
            usr.last_name = ln
            usr.email = em
            usr.save()

            posts = Post.objects.filter(uname=request.user)
            for post in posts:
                post.place = place
                post.Institute = inst
                post.save()

            data.contact_number = con
            data.place = place
            data.occupation = occ
            data.Institute = inst
            data.save()
            context['data'] =data
            if "image" in request.FILES:
                img = request.FILES["image"]
                data.profile_pic = img
                data.save()
    return redirect('/settings/')

def change_password(request):
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
    if request.method=="POST":
        current = request.POST["cpassword"]
        new_pas = request.POST["npassword"]
        user = User.objects.get(id=request.user.id)
        uname = user.username
        check1 = user.check_password(current)
        if check1==True:
            user.set_password(new_pas)
            user.save()
            user = User.objects.get(username=uname)
            auth.login(request,user)
    return redirect('/settings/')


def open_post(request,sha):
    context={}
    context['sha'] = sha
    context['page_title'] = 'Home'
    dashboard = {'n':'Dashboard','w':'dashboard'}
    posts = {'n': 'Products','w':'posts'}
    uploadpost = {'n': 'Sell Products', 'w':'uploadpost'}
    notifications = {'n' : 'Notifications/Messages' , 'w': 'notifications'}
    liked = {'n':'Liked', 'w': 'liked'}
    settings = {'n' : 'Settings', 'w':'settings'}
    navss = [posts, uploadpost, notifications,settings, dashboard]
    context['navss'] = navss
    #seain
    seain = Seainp.objects.all()
    context['seas_ind'], context['seas_all'] = get_sea(request)
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context['data'] = data
    imgs = PostImage.objects.all()
    context['imgs'] = imgs
    check=Post.objects.filter(sha=sha)
    if len(check)>0:
        if sha=='lastpost':
            post_main = Post.objects.get(uname=request.user)[-1]
        else:
            post_main = Post.objects.get(sha = sha)
        context['post'] = post_main
        post_sec = []
        rejec = ['','a','an','the','is','are','or','and','can','could','may','might','then','if','this','that','these','those','it','he','she','to','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','as','you','of','in','has','will','we','by','us','our','its''your','all','for','on','at','his']
        post_tit = re.findall(r'[a-z0-9]*',post_main.post_title.lower())
        post_des = re.findall(r'[a-z0-9]*',post_main.desc.lower())
        post_spl = post_tit + post_des
        while('' in post_spl):
            post_spl.remove('')
        print('post_spl',post_spl)
        posts = Post.objects.all().exclude(sha=sha)
        for post in posts:
            oth_post_tit_spl = re.findall(r'[a-z0-9]*',post.post_title.lower())
            oth_post_desc_spl = re.findall(r'[a-z0-9]*',post.desc.lower())
            for spl in post_spl:
                if str(spl).lower() not in rejec:
                    print(spl)
                    for oth_post_tit in oth_post_tit_spl:
                        reg = re.findall(spl,oth_post_tit)
                        for i in rejec:
                            while i in reg:
                                reg.remove(i)
                        if len(reg)>0:
                            print('reg',reg)
                            post_sec.append(post)
                        reg = re.findall(post.post_title.lower(),spl.lower())
                        for i in rejec:
                            while i in reg:
                                reg.remove(i)
                        if len(reg)>0:
                            print('reg',reg)
                            post_sec.append(post)
                    for oth_post_desc in oth_post_desc_spl:
                        reg = re.findall(spl,oth_post_desc)
                        for i in rejec:
                            while i in reg:
                                reg.remove(i)
                        if len(reg)>0:
                            print('reg',reg)
                            post_sec.append(post)
                        reg = re.findall(oth_post_desc,spl)
                        for i in rejec:
                            while i in reg:
                                reg.remove(i)
                        if len(reg)>0:
                            print('reg',reg)
                            post_sec.append(post)
                        reg = re.findall(spl.lower(),post.category.lower())
                        for i in rejec:
                            while i in reg:
                                reg.remove(i)
                        if len(reg)>0:
                            print('reg',reg)
                            post_sec.append(post)
                    
                    
                    reg = re.findall(spl.lower(),post.desc.lower())
                    for i in rejec:
                        while i in reg:
                            reg.remove(i)
                    while('' in reg):
                        reg.remove('')
                    if len(reg)>0:
                        post_sec.append(post)
        if len(post_sec)>0:
            post_cou = {}
            for post in post_sec:
                k = post_sec.count(post)
                post_cou[post.id] = k
            max_cou = max(list(post_cou.values()))
            print('max_cou',max_cou)
            post_cou = sorted(post_cou.items(),key=lambda kv: kv[1],reverse=True)
            post_fin = []
            for post in post_cou:
                if max_cou>0 and post[1]>max_cou/5:
                    post_fin.append(Post.objects.get(id=post[0]))
            print(post_cou)
            context['oth_posts'] = post_fin
            imgs = PostImage.objects.all()
            context['imgs'] = imgs
        return render(request, 'blog/open_post.html',context)
    context['con'] = 'No post available'
    context['page_title'] = 'Error - 404'
    return render(request,'blog/error.html',context)

def post_edit(request,sha):
    context={}
    dashboard = {'n':'Dashboard','w':'dashboard'}
    posts = {'n': 'Products','w':'posts'}
    uploadpost = {'n': 'Sell Products', 'w':'uploadpost'}
    notifications = {'n' : 'Notifications/Messages' , 'w': 'notifications'}
    liked = {'n':'Liked', 'w': 'liked'}
    settings = {'n' : 'Settings', 'w':'settings'}
    navs = [dashboard, posts, uploadpost, notifications, settings]
    context['navs'] = navs
    navss = [posts, uploadpost, notifications,settings, dashboard]
    context['navss'] = navss
    #seain
    seain = Seainp.objects.all()
    context['seas_ind'], context['seas_all'] = get_sea(request)
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user=request.user)
        context['data'] = data
        check = Post.objects.filter(sha=sha)
        if(len(check)>0):
            post = Post.objects.get(sha=sha)
            if post.uname == request.user:
                context['post'] = post
                context['page_title'] = 'Edit Post - '+post.post_title
                imgs = PostImage.objects.all()
                context['imgs'] = imgs
                return render(request,'blog/edit_post.html',context)
            else:
                context['page_title'] = 'Error - 404'
                context['con'] = "Unable to edit this post"
                return render(request,'blog/error.html',context)
        else:
            context['page_title'] = 'Error - 404'
            context['con'] = "This post didn't exist"
            return render(request,'blog/error.html',context)
    else:
        context['page_title'] = 'Error - 404'
        context['con'] = "Please do Login"
        return render(request,'blog/error.html',context)
    

def post_update(request):
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
    if request.method=="POST":
        id =request.POST['id']
        post = Post.objects.get(id=id)
        post_title = None
        if "name" in request.POST:
            post_title  = request.POST['name']
            post.post_title = post_title
        category = request.POST['cate']
        post.category=category
        author = None
        if "author" in request.POST:
            author = request.POST['author']
            post.author = author
        comp = None
        if "comp" in request.POST:
            comp = request.POST['comp']
            post.comp=comp
        place = data.place
        price = request.POST['price']
        post.price=price
        if "desc" in request.POST:
            desc = request.POST['desc']
            post.desc=desc
        label1 = None
        if "label1" in request.POST:
            label1 = request.POST['label1']
            post.label1=label1
        inp1 = None
        if "inp1" in request.POST:
            inp1 = request.POST['inp1']
            post.inp1=inp1
        label2 = None
        if "label2" in request.POST:
            label2 = request.POST['label2']
            post.label2=label2
        inp2 = None
        if "inp2" in request.POST:
            inp2 = request.POST['inp2']
            post.inp2=inp2
        post.save()
        images = request.FILES.getlist('cover')
        for img in images:
            image = PostImage(post=post,cover=img)
            image.save()
    return redirect('/posts/')

class post_delete(View):
    def get(self, request):
        id = request.GET.get('id',None)
        Post.objects.get(id=id).delete()
        data={
            'deleted':True
        }
        return JsonResponse(data)

class post_chan(View):
    def  get(self, request):
        id = request.GET.get('id', None)

        obj = Post.objects.get(id=id)
        if(obj.sell):
            obj.sell=False
        else:
            obj.sell=True
        obj.save()

        data = {'id':obj.id,'chan':obj.sell}

        return JsonResponse(data)

class img_delete(View):
    def get(self, request):
        id = request.GET.get('id',None)
        PostImage.objects.get(id=id).delete()
        data={
            'deleted':True
        }
        return JsonResponse(data)

class dp_delete(View):
    def get(self, request):
        id = request.GET.get('id',None)
        register_table.objects.get(id=id).profile_pic.delete()
        data={
            'deleted':True
        }
        return JsonResponse(data)

def faqs(request):
    context={}
    context['page_title'] = 'FAQs'
    dashboard = {'n':'Dashboard','w':'dashboard'}
    posts = {'n': 'Products','w':'posts'}
    uploadpost = {'n': 'Sell Products', 'w':'uploadpost'}
    notifications = {'n' : 'Notifications/Messages' , 'w': 'notifications'}
    liked = {'n':'Liked', 'w': 'liked'}
    settings = {'n' : 'Settings', 'w':'settings'}
    navss = [posts, uploadpost, notifications,settings, dashboard]
    context['navss'] = navss
    #seain
    seain = Seainp.objects.all()
    context['seas_ind'], context['seas_all'] = get_sea(request)
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context['data'] = data
    contacts = contact.objects.all()
    context['contacts'] = contacts
    return render(request,'blog/faqs.html',context)

def faqs_search(request):
    context={}
    context['page_title'] = 'FAQs'
    dashboard = {'n':'Dashboard','w':'dashboard'}
    posts = {'n': 'Products','w':'posts'}
    uploadpost = {'n': 'Sell Products', 'w':'uploadpost'}
    notifications = {'n' : 'Notifications/Messages' , 'w': 'notifications'}
    liked = {'n':'Liked', 'w': 'liked'}
    settings = {'n' : 'Settings', 'w':'settings'}
    navss = [posts, uploadpost, notifications,settings, dashboard]
    context['navss'] = navss
    #seain
    seain = Seainp.objects.all()
    context['seas_ind'], context['seas_all'] = get_sea(request)
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context['data'] = data
    contacts = contact.objects.all()
    context['contacts'] = contacts

    sea = request.GET['faq'] 
    sea = str(sea)
    if sea=='':
        return render(request,'blog/faqs.html',context)
    else:
        sea_split = re.findall(r'[a-z0-9]*',sea.lower())
        while '' in sea_split:
            sea_split.remove('')
        posts = contact.objects.all()
        print('posts',posts)
        post_sec = []
        rejec = ['','a','an','the','is','are','or','and','can','could','may','might','then','if','this','that','these','those','it','he','she','to','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','as','you','of','in','has','will','we','by','us','our','its''your','all','for','on']
        for post in posts:
            post_tit_spl = re.findall(r'[a-z0-9]*',str(post.msg).lower())
            post_desc_spl = re.findall(r'[a-z0-9]*',str(post.ans).lower())
            post_tit_sql = post_tit_spl + post_desc_spl
            while('' in post_tit_spl):
                post_tit_spl.remove('')
            print('post_tit_spl',post_tit_spl)
            for spl in sea_split:
                if spl not in rejec:
                    print('spl',spl)
                    for post_tit in post_tit_spl:
                        if post_tit not in rejec:
                            reg = re.findall(spl,post_tit)
                            if len(reg)>0:
                                print('reg',reg)
                                while('' in reg):
                                    reg.remove('')
                                post_sec.append(post)
                                print('post',post)
                            reg = re.findall(post_tit,spl)
                            if len(reg)>0:
                                print('reg',reg)
                                while('' in reg):
                                    reg.remove('')
                                post_sec.append(post)
                                print('post',post)

        if len(post_sec)>0:
            post_cou = {}
            for post in post_sec:
                k = post_sec.count(post)
                post_cou[post.id] = k
            max_cou = max(list(post_cou.values()))
            post_cou = sorted(post_cou.items(),key=lambda kv: kv[1],reverse=True)
            post_fin = []
            for post in post_cou:
                if max_cou>0 and post[1]>max_cou/5:
                    post_fin.append(contact.objects.get(id=post[0]))
                    print(post)
            context['contacts'] = post_fin
        context['fq'] = sea
    return render(request,'blog/faqs.html',context)

class theme_light(View):
    def get(self, request):
        obj = register_table.objects.get(user=request.user)
        obj.darkmode=False
        obj.save()
        data={'id':obj.id,'darkmode':obj.darkmode}
        return JsonResponse(data)

class theme_dark(View):
    def get(self, request):
        obj = register_table.objects.get(user=request.user)
        obj.darkmode=True
        obj.save()
        data={'id':obj.id,'darkmode':obj.darkmode}
        return JsonResponse(data)

def contact_us(request):
    context={}
    context['page_title'] = 'Contact Us'
    context['con'] = True
    #seain
    seain = Seainp.objects.all()
    context['seas_ind'], context['seas_all'] = get_sea(request)
    check = register_table.objects.filter(user__id=request.user.id)
    dashboard = {'n':'Dashboard','w':'dashboard'}
    posts = {'n': 'Products','w':'posts'}
    uploadpost = {'n': 'Sell Products', 'w':'uploadpost'}
    notifications = {'n' : 'Notifications/Messages' , 'w': 'notifications'}
    liked = {'n':'Liked', 'w': 'liked'}
    settings = {'n' : 'Settings', 'w':'settings'}
    navss = [posts, uploadpost, notifications,settings, dashboard]
    context['navss'] = navss
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context['data'] = data
    return render(request,'blog/contact.html',context)

def feedback_us(request):
    context={}
    context['page_title'] = 'Contact Us'
    context['con'] = False
    #seain
    seain = Seainp.objects.all()
    context['seas_ind'], context['seas_all'] = get_sea(request)
    check = register_table.objects.filter(user__id=request.user.id)
    dashboard = {'n':'Dashboard','w':'dashboard'}
    posts = {'n': 'Products','w':'posts'}
    uploadpost = {'n': 'Sell Products', 'w':'uploadpost'}
    notifications = {'n' : 'Notifications/Messages' , 'w': 'notifications'}
    liked = {'n':'Liked', 'w': 'liked'}
    settings = {'n' : 'Settings', 'w':'settings'}
    navss = [posts, uploadpost, notifications,settings, dashboard]
    context['navss'] = navss
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context['data'] = data
    return render(request,'blog/contact.html',context)

def send_msg(request):
    if request.method == 'POST':
        email = request.POST['msg_email']
        msg = request.POST['msg_msg']
        send = contact(email=email,msg=msg)
        send.save()
    return redirect('/contact/')

def send_feedback(request):
    if request.method == 'POST':
        email = request.POST['msg_email']
        msg = request.POST['msg_msg']
        send = feedback(email=email,msg=msg)
        send.save()
    return redirect('/feedback/')

class sea_delete(View):
    def get(self, request):
        id = request.GET.get('id',None)
        search = Search.objects.get(id=id)
        seain = Seainp.objects.get(inp=search.inp)
        seain.users.remove(request.user)
        seain.all=seain.num_users()
        seain.save()
        if seain.all==0:
            seain.delete()
        search.delete()
        data={}
        if len(Search.objects.filter(user=request.user).order_by('-sea_date'))>9:
            s = Search.objects.filter(user=request.user).order_by('-sea_date')[9]
            print(s)
            if s is not None:
                data['sinp']=s.inp
                data['sid']=s.id
                data['st']=True
        data['deleted']=True
        print(data)
        return JsonResponse(data)

class inc_num(View):
    def get(self, request):
        rec = request.GET.get('rec',None)
        user = request.GET.get('user',None)
        print('rec, user',rec,user)
        rec_r = register_table.objects.get(user=User.objects.get(username=rec))
        if len(chatters.objects.filter(user=User.objects.get(username=rec),recipient=User.objects.get(username=user)))>0:
            rec_c = chatters.objects.get(user=User.objects.get(username=rec),recipient=User.objects.get(username=user))
        else:
            rec_c = chatters.objects.create(user=User.objects.get(username=rec),recipient=User.objects.get(username=user))
            rec_c.notification=True
            rec_c.save()
        print('rec_c')
        if rec_r.max_num!=rec_c.num+1:
            rec_c.num=rec_r.max_num
            rec_r.max_num+=1
            rec_c.save()
            rec_r.save()

        rec_r = register_table.objects.get(user=User.objects.get(username=user))
        if len(chatters.objects.filter(user=User.objects.get(username=user),recipient=User.objects.get(username=rec)))>0:
            rec_c = chatters.objects.get(user=User.objects.get(username=user),recipient=User.objects.get(username=rec))
        else:
            rec_c = chatters.objects.create(user=User.objects.get(username=user),recipient=User.objects.get(username=rec))
        print('rec_c')
        if rec_r.max_num!=rec_c.num+1:
            rec_c.num=rec_r.max_num
            rec_r.max_num+=1
            rec_c.save()
            rec_r.save()
        print('increased')
        data={}
        return JsonResponse(data)

class get_users(View):
    def get(self, request):
        users = list(chatters.objects.filter(user=request.user).order_by('-num'))
        print('users',users)
        data=[]
        iam = request.user
        for user in users:
            det={}
            exist = len(MessageModel.objects.filter(user=iam,recipient=user.recipient))>0 and len(MessageModel.objects.filter(user=user.recipient,recipient=iam))>0
            print('exist',exist)
            print('exist',len(MessageModel.objects.filter(user=user.recipient,recipient=iam))>0)
            print('exist',len(MessageModel.objects.filter(user=iam,recipient=user.recipient))>0)
            if len(MessageModel.objects.filter(user=iam,recipient=user.recipient))>0 and len(MessageModel.objects.filter(user=user.recipient,recipient=iam))>0:
                chat_det1 = list(MessageModel.objects.filter(user=iam,recipient=user.recipient).order_by('-timestamp'))[0]
                chat_det2 = list(MessageModel.objects.filter(user=user.recipient,recipient=iam).order_by('-timestamp'))[0]
                if chat_det1.timestamp>chat_det2.timestamp:
                    chat_det = chat_det1
                else:
                    chat_det = chat_det2
                    print('chat_det',chat_det.user)
            else:
                if len(MessageModel.objects.filter(user=iam,recipient=user.recipient))>0:
                    chat_det1 = list(MessageModel.objects.filter(user=iam,recipient=user.recipient).order_by('-timestamp'))[0]
                    chat_det = chat_det1
                    print('chat_det',chat_det.user)
                elif len(MessageModel.objects.filter(user=user.recipient,recipient=iam))>0:
                    chat_det2 = list(MessageModel.objects.filter(user=user.recipient,recipient=iam).order_by('-timestamp'))[0]
                    chat_det = chat_det2
                    print('chat_det',chat_det.user)
            if len(MessageModel.objects.filter(user=iam,recipient=user.recipient))>0 or len(MessageModel.objects.filter(user=user.recipient,recipient=iam))>0:    
                
                if chat_det.body=='' and chat_det.msg1=='' and chat_det.msg2=='':
                    det['atuser'] = 'none'
                else:
                    if chat_det.user.username==request.user.username:
                        if chat_det.body=='':
                            det['last_msg']=(str(chat_det.msg2))[:50]
                        else:
                            det['last_msg']=('You: '+str(chat_det.body))[:50]
                    if chat_det.recipient.username==request.user.username:
                        if chat_det.body=='':
                            det['last_msg']=(str(chat_det.msg1))[:50]
                        else:
                            det['last_msg']=(str(chat_det.user.username)+': '+str(chat_det.body))[:50]
                    det['atuser'] = 'block'
            
            else:
                print('atuser none')
                det['atuser'] = 'none'
            
            det['username']=user.recipient.username
            det['notif']='&#9679;'
            det['color']='cornflowerblue'
            det['msg_count']=str(int(user.msg_count))
            if user.msg_count==0:
                det['display']='none'
            else:
                det['display']='block'
            '''if user.notification:
                det['color']='red'
                '''
            data.append(det)
        print('users',data)
        #data={'users':users}
        return JsonResponse(data,safe=False)

class put_notif(View):
    def get(self, request):
        rec = request.GET.get('rec',None)
        sender = request.GET.get('sender',None)
        user = request.user.username
        reciver = request.GET.get('reciver',None)
        print('rec user sender reciver',rec,user,sender,reciver)
        data={}
        notif_count = register_table.objects.get(user=User.objects.get(username=reciver)).login
        if user!=sender:
            if register_table.objects.get(user=User.objects.get(username=reciver)).login==0:
                rec_c = chatters.objects.get(user=User.objects.get(username=reciver),recipient=User.objects.get(username=sender))
                if rec_c.notification:
                    rec_c.msg_count+=1
                else:
                    rec_c.notification=True
                    rec_c.msg_count=1
                rec_c.save()
                print('notif1',1/notif_count)
            elif reciver==user and sender==rec:
                rec_c = chatters.objects.get(user=User.objects.get(username=reciver),recipient=User.objects.get(username=sender))
                rec_c.notification=False
                rec_c.msg_count=0
                print('notif',False)
                rec_c.save()
            else:
                rec_c = chatters.objects.get(user=User.objects.get(username=reciver),recipient=User.objects.get(username=sender))
                if rec_c.notification:
                    rec_c.msg_count+=1
                else:
                    rec_c.notification=True
                    rec_c.msg_count=1
                print('notif2',1/notif_count)
                rec_c.save()
        else:
            if sender==user and rec!=reciver:
                rec_c = chatters.objects.get(user=User.objects.get(username=sender),recipient=User.objects.get(username=reciver))
                if rec_c.notification:
                    rec_c.msg_count+=1
                else:
                    rec_c.notification=True
                    rec_c.msg_count=1
                print('notif3',1/notif_count)
                rec_c.save()
            else:
                rec_c = chatters.objects.get(user=User.objects.get(username=sender),recipient=User.objects.get(username=reciver))
                rec_c.notification=False
                rec_c.msg_count=0
                print('notif',False)
                rec_c.save()
        #if len(chatters.objects.filter(user=User.objects.get(username=user),recipient=User.objects.get(username=rec)))>0:
        '''if sender!=user:
            rec_c = chatters.objects.get(user=User.objects.get(username=user),recipient=User.objects.get(username=sender))
            if rec!=sender and user!=sender:
                if rec_c.notification:
                    rec_c.msg_count+=1
                else:
                    rec_c.notification=True
                    rec_c.msg_count=1
                print('notif',True)
                rec_c.save()
                if rec_c.msg_count>0:
                    data['msg_count'] = rec_c.msg_count
                print('msg_count',data['msg_count'])
                data['notif']=True
            else:
                rec_c.notification=False
                rec_c.msg_count=0
                rec_c.save()
        #print('user_active rec','akash admin',rec,register_table.objects.get(user=User.objects.get(username=rec)).login)
        #if sender!=user and rec!='':
        elif rec!='' and user==sender:
            rec_c = chatters.objects.get(user=User.objects.get(username=rec),recipient=User.objects.get(username=sender))
            #if rec!='' and user==sender and register_table.objects.get(user=User.objects.get(username=rec)).login==False:
            if rec_c.notification:
                rec_c.msg_count+=1
            else:
                rec_c.notification=True
                rec_c.msg_count=1
            print('notif',True)
            rec_c.save()
            if rec_c.msg_count>0:
                data['msg_count'] = rec_c.msg_count
            print('msg_count',data['msg_count'])
            data['notif']=True
        if rec==sender:
            rec_c = chatters.objects.get(user=User.objects.get(username=user),recipient=User.objects.get(username=sender))
            rec_c.notification=False
            rec_c.msg_count=0
            rec_c.save()'''
        return JsonResponse(data)

class remove_notif(View):
    def get(self,request):
        rec = request.GET.get('rec',None)
        user = request.user.username
        data={}
        if len(chatters.objects.filter(user=User.objects.get(username=user),recipient=User.objects.get(username=rec)))>0:
            rec_c = chatters.objects.get(user=User.objects.get(username=user),recipient=User.objects.get(username=rec))
        else:
            rec_c = chatters.objects.create(user=User.objects.get(username=user),recipient=User.objects.get(username=rec))
        rec_c.notification=False
        rec_c.msg_count=0
        rec_c.save()
        print('notif',False)
        print(rec_c.notification)
        data['notif']=False
        print('removed')
        return JsonResponse(data)

class chat_user(View):
    def get(self, request):
        rec = request.GET.get('rec',None)
        user = request.user.username
        data={}
        data['got'] = False
        data['created'] = False
        data['all'] = False
        if rec!=user:
            if len(User.objects.filter(username=rec))==0:
                data['all'] = True
            elif len(chatters.objects.filter(user=User.objects.get(username=user),recipient=User.objects.get(username=rec)))>0:
                rec_c = chatters.objects.get(user=User.objects.get(username=user),recipient=User.objects.get(username=rec))
                data['got'] = True
                data['username'] = rec_c.recipient.username
            else:
                rec_c = chatters.objects.create(user=User.objects.get(username=user),recipient=User.objects.get(username=rec))
                data['created'] = True
                data['username'] = rec_c.recipient.username
        else:
            data['all']=True
        print(data)
        return JsonResponse(data)

class send_request(View):
    def get(self, request):
        rec = request.GET.get('rec',None)
        id = request.GET.get('id',None)
        user = request.user.username
        data={'sender':user}
        print('data sender',user)
        rec_r = register_table.objects.get(user=User.objects.get(username=user))
        if len(chatters.objects.filter(user=User.objects.get(username=user),recipient=User.objects.get(username=rec)))>0:
            rec_u = chatters.objects.get(user=User.objects.get(username=user),recipient=User.objects.get(username=rec))
        else:
            rec_u = chatters.objects.create(user=User.objects.get(username=user),recipient=User.objects.get(username=rec))
        '''if rec_u.notification:
            rec_u.msg_count+=1
        else:
            rec_u.notification=True
            rec_u.msg_count=1'''
        if rec_r.max_num!=rec_u.num+1:
            rec_u.num=rec_r.max_num
            rec_r.max_num+=1
        rec_r.save()
        rec_u.save()
        rec_r = register_table.objects.get(user=User.objects.get(username=rec))
        if len(chatters.objects.filter(user=User.objects.get(username=rec),recipient=User.objects.get(username=user)))>0:
            rec_u = chatters.objects.get(user=User.objects.get(username=rec),recipient=User.objects.get(username=user))
        else:
            rec_u = chatters.objects.create(user=User.objects.get(username=rec),recipient=User.objects.get(username=user))
        '''if rec_u.notification:
            rec_u.msg_count+=1
        else:
            rec_u.notification=True
            rec_u.msg_count=1'''
        if rec_r.max_num!=rec_u.num+1:
            rec_u.num=rec_r.max_num
            rec_r.max_num+=1
        rec_r.save()
        rec_u.save()
        msg1 = 'You requested '+str(rec)+' to buy their product <a target="_blank" href="/post/'+Post.objects.get(id=id).sha+'/">'+str(Post.objects.get(id=id).post_title)+'</a>'
        msg2 = str(user)+' requested you to buy your product <a target="_blank" href="/post/'+Post.objects.get(id=id).sha+'/">'+str(Post.objects.get(id=id).post_title)+'</a>'
        msg = MessageModel.objects.create(user=User.objects.get(username=user),recipient=User.objects.get(username=rec),body='',msg1=msg2,msg2=msg1)
        print('msg',msg)
        return JsonResponse(data)


class get_messages(View):
    def get(self, request):
        rec = request.GET.get('rec',None)
        user = request.user.username
        data=[]
        msgs1 = MessageModel.objects.filter(user=User.objects.get(username=user),recipient=User.objects.get(username=rec)).order_by('-timestamp')
        msgs2 = MessageModel.objects.filter(user=User.objects.get(username=rec),recipient=User.objects.get(username=user)).order_by('-timestamp')
        i=0
        j=0
        if len(msgs1)==0 and len(msgs2)==0:
            pass
        elif len(msgs1)==0:
            for msg in msgs2:
                det={}
                det['body']=msg.body
                det['user']=msg.user.username
                det['recipient']=msg.recipient.username
                det['timestamp']=msg.timestamp
                det['msg1']=msg.msg1
                det['msg2']=msg.msg2
                data.append(det)
        elif len(msgs2)==0:
            for msg in msgs1:
                det={}
                det['body']=msg.body
                det['user']=msg.user.username
                det['recipient']=msg.recipient.username
                det['timestamp']=msg.timestamp
                det['msg1']=msg.msg1
                det['msg2']=msg.msg2
                data.append(det)
        else:
            while i<=len(msgs1) or j<=len(msgs2):
                det={}
                if i==len(msgs1):
                    for msg in msgs2:
                        det={}
                        det['body']=msg.body
                        det['user']=msg.user.username
                        det['recipient']=msg.recipient.username
                        det['timestamp']=msg.timestamp
                        det['msg1']=msg.msg1
                        det['msg2']=msg.msg2
                        data.append(det)
                elif j==len(msgs2):
                    for msg in msgs1:
                        det={}
                        det['body']=msg.body
                        det['user']=msg.user.username
                        det['recipient']=msg.recipient.username
                        det['timestamp']=msg.timestamp
                        det['msg1']=msg.msg1
                        det['msg2']=msg.msg2
                        data.append(det)
                else:
                    if msgs1[i].timestamp>msgs2[j].timestamp:
                        det['body']=msgs1[i].body
                        det['user']=msgs1[i].user.username
                        det['recipient']=msgs2[i].recipient.username
                        det['timestamp']=msgs2[i].timestamp
                        det['msg1']=msgs2[i].msg1
                        det['msg2']=msgs2[i].msg2
                        i+=1
                    else:
                        det['body']=msgs2[i].body
                        det['user']=msgs2[i].user.username
                        det['recipient']=msgs2[i].recipient.username
                        det['timestamp']=msgs2[i].timestamp
                        det['msg1']=msgs2[i].msg1
                        det['msg2']=msgs2[i].msg2
                        j+=1
                    data.append(det)
        
        print('data',data)
        return JsonResponse(data,safe=False)

class get_search(View):
    def get(self, request):
        sea = request.GET.get('sea',None).lower()
        search = Search.objects.filter(user=request.user).order_by('-sea_date')
        sea_all = Search.objects.all().order_by('-sea_date')
        data=[]
        #sea_split = re.findall(r'[a-z0-9]*',sea.lower())
        '''while '' in sea_split:
            sea_split.remove('')
        print(sea_split)
        c=0
        for sea in sea_split:
            for i in seain:
                if c<10:
                    reg = re.findall(sea,i)
                    c+=1'''
        c=0
        sealist=[]
        if len(sea)>0:
            for s in search:
                for i in range(len(s.inp)):
                    inp=s.inp
                    det={}
                    if sea==inp[i:i+len(sea)].lower() and s.inp.lower() not in sealist:
                        det['inp']=s.inp
                        det['id']=s.id
                        det['me']=True
                        data.append(det)
                        sealist.append(s.inp.lower())
                        c+=1
                if c==10:
                    break
            if c<10:
                for s in sea_all:
                    for i in range(len(s.inp)):
                        inp=s.inp
                        det={}
                        if sea==inp[i:i+len(sea)].lower() and s.inp.lower() not in sealist:
                            det['inp']=s.inp
                            det['id']=s.id
                            det['me']=False
                            data.append(det)
                            sealist.append(s.inp.lower())
                            c+=1
                    if c==10:
                        break
        else:
            for s in search:
                det={}
                det['inp']=s.inp
                det['id']=s.id
                det['me']=True
                data.append(det)
                c+=1
                if c==10:
                    break

        print(data)
        
        return JsonResponse(data,safe=False)


