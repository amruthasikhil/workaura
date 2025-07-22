from django.db import models
    
class LoginDb(models.Model):
    username=models.CharField(max_length=50,null=True,blank=True)
    password=models.CharField(max_length=50,null=True,blank=True,default="pending")
    usertype=models.CharField(max_length=50,null=True,blank=True,default="pending")


class FreelancerDb(models.Model):
    full_name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    password = models.CharField(default="pending",max_length=50,null=True,blank=True) 
    phone_number = models.CharField(max_length=50,null=True,blank=True)
    location = models.CharField(max_length=50,null=True,blank=True)
    skills_expertise = models.CharField(max_length=50,null=True,blank=True)
    portfolio_link = models.CharField(blank=True, null=True,max_length=50)
    id_proof = models.FileField(upload_to='freelancer_id_proofs',null=True,blank=True)  
    registered_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    is_verified = models.CharField(default="pending",null=True,blank=True,max_length=50)
    login=models.IntegerField(null=True,blank=True)


class FreelancerprofileDb(models.Model):
    job = models.CharField(max_length=100,blank=True, null=True)
    country = models.CharField(max_length=100,blank=True, null=True)
    social_media_link = models.CharField(blank=True, null=True,max_length=100)
    per_hour_rate = models.CharField(blank=True, null=True,max_length=10)
    availability = models.CharField(max_length=20,blank=True, null=True)
    experience_level = models.CharField(max_length=20,blank=True, null=True)
    languages_known = models.CharField(max_length=100,blank=True, null=True)
    about_me = models.CharField(blank=True, null=True,max_length=100)
    lid = models.CharField(max_length=50)  



class FreelancerServiceDb(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=10, blank=True, null=True)
    category = models.IntegerField(blank=True, null=True)
    freelancer_id = models.CharField(max_length=50)  # Reference to Freelancer
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class  ClientDb(models.Model):
    full_name = models.CharField(max_length=200, blank=True, null=True)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255,default="pending")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    company_type = models.CharField(max_length=100,  blank=True, null=True)
    project_needs = models.TextField(blank=True, null=True)
    company_website = models.CharField(max_length=200, blank=True, null=True)
    business_verification_document = models.FileField(upload_to='verification_documents', blank=True, null=True)
    login=models.IntegerField(null=True,blank=True)

class ProjectPostDb(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)  
    description = models.TextField(null=True, blank=True) 
    budget_type = models.CharField(max_length=20,null=True, blank=True)  
    budget_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    category = models.IntegerField( null=True, blank=True) 
    required_skills = models.CharField(max_length=255, null=True, blank=True)  
    deadline = models.DateField(null=True, blank=True)  
    attachments = models.FileField(upload_to='project_files', null=True, blank=True) 
    visibility = models.CharField(max_length=10, default='public')  
    client_id = models.IntegerField(null=True, blank=True)  
    created_at = models.DateField(auto_now_add=True)


class ProfileEntry(models.Model):
    freelancer=models.IntegerField(null=True,blank=True)
    what_i_do=models.CharField(max_length=500)
    why_i_choose = models.CharField(max_length=500)



class PortfolioProject(models.Model):
    freelancer = models.IntegerField(null=True,blank=True)
    project_name = models.CharField(max_length=100)
    tools_used = models.CharField(max_length=255)
    description = models.TextField()
    project_link = models.URLField(blank=True, null=True)
    image = models.FileField(upload_to='portfolio', blank=True, null=True)

    


class ProjectLikeDb(models.Model):
    pid = models.IntegerField(null=True, blank=True)  
    count = models.IntegerField(default=0)  


class ProposalDb(models.Model):
    project_id = models.IntegerField(blank=True, null=True)  
    freelancer_id = models.IntegerField(blank=True, null=True)  
    cover_letter = models.TextField(blank=True, null=True)  
    proposed_budget = models.CharField(max_length=100,blank=True, null=True)  
    estimated_time = models.CharField(max_length=50, blank=True, null=True)  
    additional_notes = models.TextField(blank=True, null=True)  
    status = models.CharField(max_length=20, default="pending")  
    submitted_at = models.DateTimeField(auto_now_add=True)  

class SavedProjectDb(models.Model):
    project_id = models.IntegerField(blank=True, null=True)  
    freelancer_id = models.IntegerField(blank=True, null=True)  

