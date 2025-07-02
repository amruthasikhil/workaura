from django.shortcuts import render,redirect
from Freelancer.models import *
from Adminapp.models import *
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib import messages


def Userlandingpage(request):
    return render(request,"landingpage.html")

def Freelancersignup(request):
    return render(request,"freelancersignup.html",{"success":"no","name":"invalid"})

def Freelancersignup_Signuppost(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        location = request.POST.get('location')
        skills_expertise = request.POST.get('skills_expertise')
        portfolio_link = request.POST.get('portfolio_link')
        id_proof = request.FILES['government_id']
        #skill expertise user can add another skills and check after he joined
        login_obj=LoginDb(username=email,usertype="client")
        login_obj.save()
        print(login_obj)
        login_id = login_obj.id
        obj=FreelancerDb(login=login_id,full_name=full_name,email=email,phone_number=phone_number,location=location,skills_expertise=skills_expertise,portfolio_link=portfolio_link,id_proof=id_proof)
        obj.save()
        return render(request,"freelancersignup.html",{"success":"yes","name":full_name})

def Freelancersignin(request):
    return render(request,"freelancersignin.html")


def Profilesettingpage(request):
    lid=request.session['lid']
    data=FreelancerDb.objects.get(login=lid)
    return render(request,"profilesettingpage.html",{"data":data,"first":"yes","data2":"ok"})

def Profilesadding(request):
     if request.method == "POST":
        job = request.POST.get("job")
        country = request.POST.get("country")
        social_media_link = request.POST.get("social_media_link")
        per_hour_rate = request.POST.get("project_rate")
        availability = request.POST.get("availability")
        experience_level = request.POST.get("experience_level")
        languages_known = request.POST.get("languages_known")
        about_me = request.POST.get("about_me")
        lid = request.session.get("lid")

        FreelancerprofileDb.objects.create(
            job=job,
            country=country,
            social_media_link=social_media_link,
            per_hour_rate=per_hour_rate,
            availability=availability,
            experience_level=experience_level,
            languages_known=languages_known,
            about_me=about_me,
            lid=lid
        )
        return redirect(Userdashboard)


def Loginpopup(request):
    return render(request,"loginpopuppage.html")


def Freelancersigninpost(request):
    if request.method == "POST":
        print("oooook")
        un=request.POST.get("username")
        pwd=request.POST.get("pswd")
        obj=LoginDb.objects.get(username=un,password=pwd)
        
        if obj.usertype == "freelancer":
                print("freeeeeeeee..................")
                request.session['lid']=obj.id
                try:
                    print("yes......................................yyyy")
                    FreelancerprofileDb.objects.get(lid=obj.id)
                    return redirect(Userdashboard)
                except FreelancerprofileDb.DoesNotExist:
                    print("---------------------------------------------yes-----------------------------------")
                    return redirect(Profilesettingpage)
        elif obj.usertype == "client":
            request.session['lid']=obj.id
            clientobj=ClientDb.objects.get(login=obj.id)
            return render(request,"client_userhome.html",{"name":clientobj.full_name,"img":clientobj.business_verification_document})
        else:
                return redirect(Freelancersignin)
    else:
         print("------------------------------------jjjjjjjjjjjjjjj")
         return redirect(Freelancersignin)
    



def Changeyourpassword(request):
     if request.method == "POST":
          curpaswd=request.POST.get("cur")
          newpswd=request.POST.get("new")
          lid=request.session.get("lid")
          try:
            obj=LoginDb.objects.get(id=lid,password=curpaswd)
            if obj:
                LoginDb.objects.filter(id=lid).update(password=newpswd)
                messages.success(request,"Your Password change successfully...Thankyou!")
                return redirect(Profilesettingpage)
            else:
                messages.error(request, "The current password you entered is incorrect. Please try again.")
                return redirect(Profilesettingpage)
          except LoginDb.DoesNotExist:
              messages.error(request, "The current password you entered is incorrect. Please try again.")
              return redirect(Profilesettingpage)
              
def Userdashboard(request):
    lid=request.session.get("lid")
    obj=FreelancerDb.objects.get(login=lid)
    context={
        "name":obj.full_name,
        "imge":obj.id_proof
    }
    return render(request,"userdashboard.html",context)

def Freelancer_profile(request):
    lid=request.session.get("lid")
    obj=FreelancerDb.objects.get(login=lid)
    obj2=FreelancerprofileDb.objects.get(lid=lid)
    print(obj2)
    return render(request,"pagesprofile.html",{ "name":obj.full_name, "imge":obj.id_proof,"data2":obj2,"data":obj})

def servicelisting(request):
    lid = request.session.get("lid")
    obj = FreelancerDb.objects.get(login=lid)
    data = FreelancerServiceDb.objects.filter(freelancer_id=lid)
    newarr = []
    for i in data:
        category_id = int(i.category)
        data_ob = SubCategoryDb.objects.filter(id=category_id)
        for j in data_ob:
            newarr.append({
                "id": i.id,
                "title": i.title,
                "description": i.description,
                "price": i.price,
                "category": j.subcategory_name,
            })

    context = {
        "name": obj.full_name,
        "imge": obj.id_proof,
        "mydata": newarr
    }
    return render(request, "servicelisting.html", context)


def addservices(request):
    lid=request.session.get("lid")
    obj=FreelancerDb.objects.get(login=lid)
    services=SubCategoryDb.objects.all()
    context={
        "name":obj.full_name,
        "imge":obj.id_proof,
        "data":services
    }
    return render(request,"addservice.html",context)

def addservicespost(request):
    if request.method == "POST":
        title = request.POST.get('title')
        price = request.POST.get('price')
        category = request.POST.get('category')
        description = request.POST.get('description')
        freelancer_id = request.session.get('lid')  

        # Save data to the database
        FreelancerServiceDb.objects.create(
            title=title,
            price=price,
            category=category,
            description=description,
            freelancer_id=freelancer_id
        )
        return redirect(addservices)  


def freelancer_view_newprojects(request):
    lid=request.session.get("lid")
    userobj=FreelancerDb.objects.get(login=lid)
    data = ProjectPostDb.objects.all().order_by('-id') 
    newarr=[]
    for i in data:
        obj=ClientDb.objects.get(login=i.client_id)
        try:
            obj3=ProjectLikeDb.objects.get(pid=i.id)
            newarr.append(
                    {
                        "id":i.id,
                        "name":obj.full_name,
                        "pic":obj.business_verification_document,
                        "title":i.title,
                        "descp":i.description,
                        "date":i.created_at,
                        "lid":obj.login,
                        "like":obj3.count
                    }
                )
        except ProjectLikeDb.DoesNotExist:
            newarr.append(
                    {
                        "id":i.id,
                        "name":obj.full_name,
                        "pic":obj.business_verification_document,
                        "title":i.title,
                        "descp":i.description,
                        "date":i.created_at,
                        "lid":obj.login,
                        "like":"0"
                    }
                )
    qry=SavedProjectDb.objects.filter(freelancer_id=lid) 
    newarr2=[]
    for k in qry:
        qry2=ProjectPostDb.objects.filter(id=k.project_id)
        for j in qry2:
            print("---------------------------------------------------------------------------",j.title)
            obj=ClientDb.objects.get(login=j.client_id)
            print("---------------------------------------------------------------------------",j.title)
            print("---------------------------------------------------------------------------",obj.full_name)
            print("---------------------------------------------------------------------------",obj.business_verification_document)
            print("---------------------------------------------------------------------------",j.description)
            print("---------------------------------------------------------------------------",j.created_at)

            newarr2.append(
                        {
                            "id":j.id,
                            "name":obj.full_name,
                            "pic":obj.business_verification_document,
                            "title":j.title,
                            "descp":j.description,
                            "date":j.created_at,
                            "lid":obj.login,
                        }
                    )
     
        
    return render(request,"freelancer_view_newprojects.html",{"data":newarr,"newarr2":newarr2,"name":userobj.full_name,"imge":userobj.id_proof})

def projectviewmore(request,prjtid):
    data2=ProjectPostDb.objects.get(id=prjtid)
    subcat=SubCategoryDb.objects.get(id=data2.category)
    request.session['project_id']=prjtid
    lid=request.session.get("lid")
    userobj=FreelancerDb.objects.get(login=lid)
    return render(request,"project_viewmore.html",{"project":data2,"subcat":subcat,"name":userobj.full_name,"imge":userobj.id_proof})


def projectlike(request,pid):
    lid=request.session.get('lid')
    try:
        obj=ProjectLikeDb.objects.get(pid=pid)
        obj.count=obj.count+1
        obj.save()
    except ProjectLikeDb.DoesNotExist:
        ob=ProjectLikeDb.objects.create(pid=pid,count=1)
        ob.save()
    data = ProjectPostDb.objects.all().order_by('-id')  
    newarr=[]
    for i in data:
        obj=ClientDb.objects.get(login=i.client_id)
        print(obj.full_name,"=============================================================")
        try:
            print("00000------------------------------------------------------------------")
            obj3=ProjectLikeDb.objects.get(pid=i.id)
            print("###################################################",obj3.count)
            newarr.append(
                    {
                        "id":i.id,
                        "name":obj.full_name,
                        "pic":obj.business_verification_document,
                        "title":i.title,
                        "descp":i.description,
                        "date":i.created_at,
                        "lid":obj.login,
                        "like":obj3.count,
                    }
                )
        except ProjectLikeDb.DoesNotExist:
            newarr.append(
                    {
                        "id":i.id,
                        "name":obj.full_name,
                        "pic":obj.business_verification_document,
                        "title":i.title,
                        "descp":i.description,
                        "date":i.created_at,
                        "lid":obj.login,
                        "like":"0",
                    }
                )
    return render(request,"freelancer_view_newprojects.html",{"data":newarr})

def sendingproject_proposal(request,pid):
    lid=request.session.get("lid")
    userobj=FreelancerDb.objects.get(login=lid)
    return render(request,"projectproposal_by_freelancer.html",{"name":userobj.full_name,"imge":userobj.id_proof})


def projectsave(request,pid):
    lid=request.session.get('lid')
    try:
        sts=''
        obj2=SavedProjectDb.objects.get(project_id=pid,freelancer_id=lid)
        if obj2 :
            sts='saved'
        else :
            sts = 'not_saved'
    except SavedProjectDb.DoesNotExist:
        ob2=SavedProjectDb.objects.create(project_id=pid,freelancer_id=lid)
        ob2.save()
    data = ProjectPostDb.objects.all().order_by('-id')  
    newarr=[]
    for i in data:
        obj=ClientDb.objects.get(login=i.client_id)
        print(obj.full_name,"=============================================================")
        try:
            print("00000------------------------------------------------------------------")
            obj3=ProjectLikeDb.objects.get(pid=i.id)
            print("###################################################",obj3.count)
            newarr.append(
                    {
                        "id":i.id,
                        "name":obj.full_name,
                        "pic":obj.business_verification_document,
                        "title":i.title,
                        "descp":i.description,
                        "date":i.created_at,
                        "lid":obj.login,
                        "like":obj3.count,
                        "sts":sts
                    }
                )
        except ProjectLikeDb.DoesNotExist:
            newarr.append(
                    {
                        "id":i.id,
                        "name":obj.full_name,
                        "pic":obj.business_verification_document,
                        "title":i.title,
                        "descp":i.description,
                        "date":i.created_at,
                        "lid":obj.login,
                        "like":"0",
                        "sts":sts
                    }
                )
    return render(request,"freelancer_view_newprojects.html",{"data":newarr})


# def Projectssaves(request):
#     lid=request.session.get("lid")
#     try:
#         qry=SavedProjectDb.objects.filter(freelancer_id=lid)
#     except SavedProjectDb.DoesNotExist:
#         qry = "novalue"
#     return render(request,"freelancer_view_newprojects.html",{"qry":qry})


def freelancersend_projectproposal(request):
    if request.method == "POST":
        prdtid=request.session.get('project_id')
        lid=request.session.get('lid')
        cover_letter = request.POST.get("cover_letter")
        proposed_budget = request.POST.get("proposed_budget")
        estimated_time = request.POST.get("estimated_time")
        additional_notes = request.POST.get("additional_notes")

        # Save to the database
        ProposalDb.objects.create(
            cover_letter=cover_letter,
            proposed_budget=proposed_budget,
            estimated_time=estimated_time,
            additional_notes=additional_notes,
            project_id=prdtid,
            freelancer_id=lid
        )

        messages.success(request, "Proposal submitted successfully!")
        return redirect(freelancer_view_newprojects)  
    
def Freelancerview_prorposal_status(request):
    lid = request.session.get('lid')
    arr=[]
    data= ProposalDb.objects.filter(freelancer_id=lid)
    for i in data:
        data2 = ProjectPostDb.objects.filter(id=i.project_id)
        for j in data2:
            data3 =ClientDb.objects.get(login=j.client_id)

            arr.append({
                "fullname" : data3.full_name,
                "submitted_at":i.submitted_at,
                "cover_letter":i.cover_letter,
                "status":i.status,
                "project":j.title,
                "proposed_budget":i.proposed_budget,
                "estimated_time":i.estimated_time
            })

    return render(request,"status_of_proposal.html",{"data":arr})

def freelancer_view_clients_list(request,clid):
    data=ClientDb.objects.get(login=clid)
    data2=ClientDb.objects.all()[::-1][:4]
    return render(request,"freelancer_view_clients_list.html",{"data":data,"data2":data2})

def clientviewprofile(request):
    return render(request,"client_profile.html")
        
#########################
#################################
########################################
##############################################
#
#
## Client

#=========================================================================================================================
    
def clientsignup(request):
    return render(request,"clientsignup.html")

def clientsignup_post(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email_address = request.POST.get("email_address")
        phone_number = request.POST.get("phone_number")
        company_type = request.POST.get("company_type")
        project_needs = request.POST.get("project_needs")
        company_website = request.POST.get("company_website")
        business_verification_document = request.FILES.get("business_verification_document")
        login_obj=LoginDb(username=email_address,usertype="client")
        login_obj.save()
        print(login_obj)
        login_id = login_obj.id
        obj = ClientDb(
            full_name=full_name,
            email_address=email_address,
            phone_number=phone_number,
            company_type=company_type,
            project_needs=project_needs,
            company_website=company_website,
            business_verification_document=business_verification_document,
            login=login_id
        )
        obj.save()

        return redirect(clientsignup)  
    
def Clientproject(request):
    services=SubCategoryDb.objects.all()
    return render(request,"client_projectadd.html",{"services":services})


def Clientproject_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        budget_type = request.POST.get("budget_type")
        budget_amount = request.POST.get("budget_amount")
        category = request.POST.get("category")
        required_skills = request.POST.get("required_skills")
        deadline = request.POST.get("deadline")
        attachments = request.FILES.get("attachments")
        visibility = request.POST.get("visibility")
        client_id = request.session.get("lid")

        project_obj = ProjectPostDb(
            title=title,
            description=description,
            budget_type=budget_type,
            budget_amount=budget_amount,
            category=category,
            required_skills=required_skills,
            deadline=deadline,
            attachments=attachments,
            visibility=visibility,
            client_id=client_id
        )
        project_obj.save()

        return redirect(Clientproject)  

def Userslogout(request):
    del request.session['lid']
    return redirect(Freelancersignin)

def client_viewproject(request):
    lid=request.session.get('lid')
    project=ProjectPostDb.objects.filter(client_id=lid)
    new_arr=[]
    for i in project:
        categ= SubCategoryDb.objects.get(id=i.category)
        new_arr.append({
            "title":i.title,
            "description":i.description,
            "budget_amount":i.budget_amount,
            "category":categ.subcategory_name,
            "deadline":i.deadline,

        })
    return render(request,"clientview_addedproject.html",{"projects":new_arr})


#=================================25/06

def servicedelete(request,serviceid):
    obj=FreelancerServiceDb.objects.get(id=serviceid)
    obj.delete()
    return redirect(servicelisting)

def serviceedit(request,serviceid):
    lid=request.session.get("lid")
    obj=FreelancerDb.objects.get(login=lid)
    dataobj=FreelancerServiceDb.objects.get(id=serviceid)
    subcatdata=SubCategoryDb.objects.get(id=dataobj.category)
    services=SubCategoryDb.objects.all()
    context={
        "name":obj.full_name,
        "imge":obj.id_proof,
        "dataobj":dataobj,
        "subcatdata":subcatdata,
        "data":services
    }
    return render(request,"editservice.html",context)

    
def updateservices(request):
    if request.method  == "POST" :
        serid = request.POST.get('serid')
        title = request.POST.get('title')
        price = request.POST.get('price')
        category = request.POST.get('category')
        description = request.POST.get('description')
        freelancer_id = request.session.get('lid') 
 
        FreelancerServiceDb.objects.filter(id=serid).update(
             title = title,
            price=price,
            category=category,
            description=description,
            )
        return redirect(servicelisting)
    
def freelancer_view_newprojects_search(request):
    if request.method == "POST":
        search=request.POST.get("search")
        lid=request.session.get("lid")
        userobj=FreelancerDb.objects.get(login=lid)
        data = ProjectPostDb.objects.filter(title__contains=search)
        newarr=[]
        for i in data:
            obj=ClientDb.objects.get(login=i.client_id)
            try:
                obj3=ProjectLikeDb.objects.get(pid=i.id)
                newarr.append(
                        {
                            "id":i.id,
                            "name":obj.full_name,
                            "pic":obj.business_verification_document,
                            "title":i.title,
                            "descp":i.description,
                            "date":i.created_at,
                            "lid":obj.login,
                            "like":obj3.count
                        }
                    )
            except ProjectLikeDb.DoesNotExist:
                newarr.append(
                        {
                            "id":i.id,
                            "name":obj.full_name,
                            "pic":obj.business_verification_document,
                            "title":i.title,
                            "descp":i.description,
                            "date":i.created_at,
                            "lid":obj.login,
                            "like":"0"
                        }
                    )
        qry=SavedProjectDb.objects.filter(freelancer_id=lid) 
        newarr2=[]
        for k in qry:
            qry2=ProjectPostDb.objects.filter(id=k.project_id)
            for j in qry2:
                print("---------------------------------------------------------------------------",j.title)
                obj=ClientDb.objects.get(login=j.client_id)
                print("---------------------------------------------------------------------------",j.title)
                print("---------------------------------------------------------------------------",obj.full_name)
                print("---------------------------------------------------------------------------",obj.business_verification_document)
                print("---------------------------------------------------------------------------",j.description)
                print("---------------------------------------------------------------------------",j.created_at)

                newarr2.append(
                            {
                                "id":j.id,
                                "name":obj.full_name,
                                "pic":obj.business_verification_document,
                                "title":j.title,
                                "descp":j.description,
                                "date":j.created_at,
                                "lid":obj.login,
                            }
                        )
        
            
        return render(request,"freelancer_view_newprojects.html",{"data":newarr,"newarr2":newarr2,"name":userobj.full_name,"imge":userobj.id_proof})
    


def freelancer_updatecomplete_profile(request):
    if request.method == "POST":
        lid=request.session.get("lid")

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        location = request.POST.get('location')
        skills_expertise = request.POST.get('skills_expertise')
        portfolio_link = request.POST.get('portfolio_link')

        job = request.POST.get("job")
        country = request.POST.get("country")
        social_media_link = request.POST.get("social_media_link")
        per_hour_rate = request.POST.get("project_rate")
        availability = request.POST.get("availability")
        experience_level = request.POST.get("experience_level")
        languages_known = request.POST.get("languages_known")
        about_me = request.POST.get("about_me")
        lid = request.session.get("lid")

            
        FreelancerDb.objects.filter(login=lid).update(
                    full_name=full_name,
                    email=email,
                    phone_number=phone_number,
                    location=location,
                    skills_expertise=skills_expertise,
                    portfolio_link=portfolio_link,
                    )
       
        FreelancerprofileDb.objects.filter(lid=lid).update(
            job=job,
            country=country,
            social_media_link=social_media_link,
            per_hour_rate=per_hour_rate,
            availability=availability,
            experience_level=experience_level,
            languages_known=languages_known,
            about_me=about_me,
        )
        return redirect(Userdashboard)
    
def freelancerdashboard(request):
    lid= request.session['lid']
    lid=request.session.get("lid")
    obj=FreelancerDb.objects.get(login=lid)
    project_recommended=ProjectPostDb.objects.all()[:1]
    newarr=[]
    for i in project_recommended:
        data2=ClientDb.objects.get(login=i.client_id)
        newarr.append({
            "clientname":data2.full_name,
            "clientimg":data2.business_verification_document,
            "projecttitle":i.title,
            "project_description":i.description,
            "totalbudget":i.budget_amount,
            "budgettype":i.budget_type,
            "created_at":i.created_at
        })
    context={
        "name":obj.full_name,
        "imge":obj.id_proof,
        "project_recommended":newarr
    }

    return render(request,"freelancer_dashboard.html",context)


#=========26/05
def clienthome(request):
    return render(request,"client_userhome.html")


def clientviewfreelancers(request):
    obj=FreelancerDb.objects.all()
    coun=obj.count()
    return render(request,"clientviewfreelancers.html",{"data":obj,"tot":coun})