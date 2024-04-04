import requests
from . import serializers
from .models import SiteUser, Products,Auction_Details, ProductCategory, ProductImage, Bids
from rest_framework import generics,permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .emails import send_otp_email, send_bid_email, send_Auction_email
from django.core.exceptions import ValidationError

class UserList(generics.ListCreateAPIView):
    queryset = SiteUser.objects.all()
    serializer_class = serializers.SiteUserSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        success, message = send_otp_email(instance.user.email)
        if success:
            return Response({'message': message}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
 
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SiteUser.objects.all()
    serializer_class = serializers.UserDetailSerializer

class VerifyOtp(APIView):
    def post(self, request):
        try:
            serializer = serializers.VerifyOtpSerializer(data=request.data)
            print('serializer',serializer)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                user = User.objects.get(email=email)
                print('user',user)
                userInfo = SiteUser.objects.get(user=user)
                print('SiteUser',userInfo)
                if userInfo.otp == otp:
                    userInfo.isVerified = True
                    userInfo.save()
                    return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

# products 
class ProductsList(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = serializers.ProductListSerializer

    def get_queryset(self):
        queryset = Products.objects.all().order_by('id')  # or any other field you want to order by
        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        # SORTINg
        sort_by = self.request.query_params.get('sort_by')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('initial_price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-initial_price')
        return queryset
    def perform_create(self, serializer):
        instance = serializer.save()

        return Response(status=status.HTTP_201_CREATED)
    

class ProductsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = serializers.ProductDetailSerializer
 
class ProductImageList(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer   

class ProductImageDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer   

class CategoryList(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer

class CategoryDetail(generics.RetrieveDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer

class ProductByCategoryAPIView(APIView):
    def get(self, request, category_id):
        try:
            category = ProductCategory.objects.get(id=category_id)
            products = Products.objects.filter(category=category)
            serializer = serializers.ProductDetailSerializer(products, many=True)
            return Response(serializer.data)
        except ProductCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class InternetProductSearch(generics.ListAPIView):
    serializer_class = serializers.InternetProductSearchSerializer

    def get_queryset(self):
        queryset = []  # Initialize an empty queryset

        # Get the query parameter from the user's request
        query = self.request.query_params.get('query')

        if not query:
            return queryset  # Return empty queryset if query is not provided

        # Define the options for the request
        options = {
            'method': 'GET',
            'url': 'https://real-time-amazon-data.p.rapidapi.com/search',
            'params': {
                'query': query,
                'page': '1',
                'country': 'US',
                'category_id': 'aps'
            },
            'headers': {
                'X-RapidAPI-Key': '9c201b076dmsh9bd5caba53d0eb5p138352jsncdc232706d84',
                'X-RapidAPI-Host': 'real-time-amazon-data.p.rapidapi.com'
            }
        }

        try:
            # Make the request
            response = requests.request(**options)

            # Check if the request was successful
            if response.status_code == 200:
                # Extract the product data from the response
                products = response.json().get('data', {}).get('products', [0])
                return [products[0]]  # Return the first product in the list

                # Assuming products is a list of product dictionaries
                # You can adjust this part based on the actual structure of the response

        except Exception as e:
            print(f"Error: {e}")

        return queryset


class BidsList(generics.ListCreateAPIView):
    queryset = Bids.objects.all()
    serializer_class = serializers.BidsSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        # instance = serializer.save()
        product_name = instance.product.name
        bidder_email = instance.bidder.user.email
        bid_price = instance.price
        placed_at = instance.created_at
        success, message = send_bid_email(bidder_email, product_name, bid_price, placed_at, owner_mail=None)
        if success:
            return Response({'message': message}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get_queryset(self):
        queryset = Bids.objects.all().order_by('id')  # or any other field you want to order by        
        # SORTINg
        sort_by = self.request.query_params.get('sort_by')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        return queryset

class BidsDetails(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Bids.objects.all()
    serializer_class = serializers.BidsSerializer

    def get_queryset(self):
        bids_id = self.kwargs['pk']
        return Bids.objects.filter(id=bids_id)
    
    
class AuctionList(generics.ListCreateAPIView):
    queryset = Auction_Details.objects.all()
    serializer_class = serializers.AuctionSerializer


class AuctionDetailsList(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction_Details.objects.all()
    serializer_class = serializers.AuctionSerializer



# authentication

class LoginView(APIView):
    def post(self, request):
        try:
            serializer = serializers.LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                try:
                    userData = User.objects.get(email=email)
                    if userData.check_password(password):
                        refresh = RefreshToken.for_user(userData)
                        return Response({
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'user_id': userData.id,
                            'email': userData.email,
                        })
                    else:
                        return Response({'message': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    return Response({'message': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
