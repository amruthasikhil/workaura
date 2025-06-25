from django.urls import path
from Adminapp import views

urlpatterns=[
    path('adminhome',views.adminindex,name="adminhome"),
      path('dashboard',views.dashboard,name="dashboard"),
       path('newfreelancers',views.newfreelancers,name="newfreelancers"),
        path('approving/<int:fid>',views.Approving,name="approving"),
                path('rejected/<int:fid>',views.Rejecting,name="rejected"),

        path('viewcategory',views.Viewcategory,name="viewcategory"),
         path('viewcategory_search',views.Viewcategory_search,name="viewcategory_search"),

        path('addcategory',views.Addcategory,name="addcategory"),
          path('addcategory_post',views.Addcategory_post,name="addcategory_post"),

          path('viewsubcategory',views.Viewsubcategory,name="viewsubcategory"),
          path('viewsubcategory_searchpost',views.Viewsubcategory_searchpost,name="viewsubcategory_searchpost"),
        
        path('addsubcategory',views.Addsubcategory,name="addsubcategory"),

        path('addsubcategory_post',views.AddSubCategory_post,name="addsubcategory_post"),

         path('adminlogin',views.Adminlogin,name="adminlogin"),
         path('adminlogout',views.Adminlogout,name="adminlogout"),
         path('adminloginpost',views.Adminlogin_post,name="adminloginpost")

]