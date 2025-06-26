from django.urls import path
from Freelancer import views

urlpatterns=[
    path('userhome',views.Userlandingpage,name="userhome"),
      path('freelancersignup',views.Freelancersignup,name="freelancersignup"),
      path('freelancersignin',views.Freelancersignin,name="freelancersignin"),
 path('freelancer_profile',views.Freelancer_profile,name="freelancer_profile"),



      path('freelancerloginpost',views.Freelancersigninpost,name="freelancerloginpost"),
       path('freelancersignuppost',views.Freelancersignup_Signuppost,name="freelancersignuppost"),
      path('profilesetting',views.Profilesettingpage,name="profilesetting"),
      path('loginpopup',views.Loginpopup,name="loginpopup"),

      path('profilesadding',views.Profilesadding,name="profilesadding"),
 path('changepassword',views.Changeyourpassword,name="changepassword"),

  path('userdashboard',views.Userdashboard,name="userdashboard"),

  path('servicelisting',views.servicelisting,name="servicelisting"),

   path('addservices',views.addservices,name="addservices"),
     path('addservicespost',views.addservicespost,name="addservicespost"),
    
     path('deleteservice/<int:serviceid>',views.servicedelete,name="deleteservice"),

       path('editservice/<int:serviceid>',views.serviceedit,name="editservice"),
    
     path('updateservices',views.updateservices,name="updateservices"),

     path('freelancer_view_newprojects_search',views.freelancer_view_newprojects_search,name="freelancer_view_newprojects_search"),
    
    
         path('freelancer_updatecomplete_profile',views.freelancer_updatecomplete_profile,name="freelancer_updatecomplete_profile"),

             path('freelancerdashboard',views.freelancerdashboard,name="freelancerdashboard"),

    
    
    path('clienthome',views.clienthome,name="clienthome"),
    
    
     path('freelancer_view_newprojects',views.freelancer_view_newprojects,name="freelancer_view_newprojects"),

     path('freelancer_view_newprojects_more/<int:prjtid>',views.projectviewmore,name="freelancer_view_newprojects_more"),
     path('projectlike/<int:pid>',views.projectlike,name="projectlike"),

      path('projectsave/<int:pid>',views.projectsave,name="projectsave"),

     path('sendingproject_proposal/<int:pid>',views.sendingproject_proposal,name="sendingproject_proposal"),
     path('freelancersend_projectproposal/',views.freelancersend_projectproposal,name="freelancersend_projectproposal"),

     path('Freelancerview_prorposal_status/',views.Freelancerview_prorposal_status,name="freelancerview_prorposal_status"),



       path('userslogout',views.Userslogout,name="userslogout"),

       path('freelancer_view_clients_list/<int:clid>',views.freelancer_view_clients_list,name="freelancer_view_clients_list"),

    
    
    
    
      path('clientsingup',views.clientsignup,name="clientsingup"),

       path('clientsingup_post',views.clientsignup_post,name="clientsingup_post"),

        path('clientproject',views.Clientproject,name="clientproject"),
          path('Clientproject_post',views.Clientproject_post,name="clientproject_post"),

           path('client_viewproject',views.client_viewproject,name="client_viewproject"),
             path('clientviewprofile',views.clientviewprofile,name="clientviewprofile"),

]