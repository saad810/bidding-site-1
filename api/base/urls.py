from django.urls import path
from . import views

urlpatterns = [
# Users
    path('users/', views.UserList.as_view()),
    path('users/<str:pk>', views.UserDetail.as_view()),
    # path('users/register', views.SiteUserCreateAPIView.as_view(), name='user-register'),
    # path('users/login', views.UserLogin.as_view(), name='user-login'),
    
# Products
    path('products/', views.ProductsList.as_view()),
    path('products/<str:pk>', views.ProductsDetail.as_view()),

# main function 1  
    path('products/search-value/', views.InternetProductSearch.as_view()),

# images

    path('products/image/', views.ProductImageList.as_view()),
    path('products/image/<str:pk>', views.ProductImageDetails.as_view()),
    
# categories
    path('category/', views.CategoryList.as_view()),
    path('category/<str:pk>', views.CategoryDetail.as_view()),

# product by category
    path('products/category/<str:category_id>', views.ProductByCategoryAPIView.as_view()),

# bids
    path('bids/', views.BidsList.as_view()),
    path('bids/<str:pk>', views.BidsDetails.as_view()),
# auth
    path('auth/login/', views.LoginView.as_view(), name='auth-login'),
    path('auth/verify/', views.VerifyOtp.as_view(), name='auth-verify-otp'),

# auction
    path('auction/', views.AuctionList.as_view()),
    path('auction/<str:pk>', views.AuctionDetailsList.as_view()),
]