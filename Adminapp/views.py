from django.shortcuts import render,redirect
from Freelancer.models import *
from Adminapp.models import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.models import User


def adminindex(request):
    context={'pagename':"Admin Homepage" }
    return render(request,"adminindex.html",context)

def dashboard(request):
    return render(request,"dashboard.html",{'pagename':"Dashboard"})

def newfreelancers(request):
    data=FreelancerDb.objects.filter(is_verified="pending")
    return render(request,"newfreelancers.html",{"data":data,'pagename':"New Freelancers"})

#---------------------category-----------------------------------------------------------------------------------------

def Viewcategory(request):
    categories = CategoryDb.objects.all() 
    return render(request, "view_category.html", {'pagename': "Category List", 'categories': categories})

def Viewcategory_search(request):
    if request.method == "POST":
        search = request.POST.get("search")  
        if search:  
            categories = CategoryDb.objects.filter(category_name__contains=search)  
        else:  
            categories = CategoryDb.objects.all()  # Fetch all categories
        return render(request, "view_category.html", {'pagename': "Category List", 'categories': categories})
    

def Addcategory(request):
    return render(request,"add_category.html",{'pagename':"Add New Category "})


def Addcategory_post(request):
    if request.method == "POST":
        category_name = request.POST.get("category_name")
        if category_name:
            CategoryDb.objects.create(category_name=category_name)
            return redirect("viewcategory")  

    return render(request, "add_category.html", {'pagename': "Add New Category"})

#-----------------------------------------------------------------------------------------------------------------


#-------------------------------------------- subcategory
def Viewsubcategory(request):
    qry=CategoryDb.objects.all()
    new_arr=[]
    for i in qry:
        qry2=SubCategoryDb.objects.filter(category_name=i.id)
        for j in qry2:
            new_arr.append({
                "catname":i.category_name,
                "subname":j.subcategory_name
            })
    return render(request,"view_subcategories.html",{'pagename':"Sub Category List","data":new_arr})


def Viewsubcategory_searchpost(request):
    if request.method=="POST":
        search=request.POST.get("search")
        qry=CategoryDb.objects.all()
        new_arr=[]
        for i in qry:
            qry2=SubCategoryDb.objects.filter(category_name=i.id,subcategory_name__contains=search)
            for j in qry2:
                new_arr.append({
                    "catname":i.category_name,
                    "subname":j.subcategory_name
                })
        return render(request,"view_subcategories.html",{'pagename':"Sub Category List","data":new_arr})




def Addsubcategory(request):
    qry=CategoryDb.objects.all()
    return render(request,"add_subcategories.html",{'pagename':"Add New Sub Category ","data":qry})

def AddSubCategory_post(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')  
        subcategory_name = request.POST.get('subcategory_name')  
        SubCategoryDb.objects.create(category_name=category_id, subcategory_name=subcategory_name)  
        return redirect(Viewsubcategory)  

def Approving(request,fid):
    FreelancerDb.objects.filter(id=fid).update(is_verified="approved")
    return redirect(newfreelancers)

def Rejecting(request,fid):
    FreelancerDb.objects.filter(id=fid).update(is_verified="rejected")
    return redirect(newfreelancers) 


def Adminlogin(request):
    return render(request,"adminlogin.html")


def Adminlogin_post(request):
    if request.method == "POST":
        un=request.POST.get('username')
        pswd=request.POST.get("password")
        if User.objects.filter(username__contains=un).exists():
            user=authenticate(username=un,password=pswd)
            if user is not None:
                request.session['username']=un
                request.session['password']=pswd
                login(request,user)
                return redirect(dashboard)
            else:
                return redirect(Adminlogin)
        else:
            return redirect(Adminlogin)
        
def Adminlogout(request):
    del request.session['username']
    del request.session['password']
    return redirect(Adminlogin)