from rest_framework import serializers
from .models import SiteUser, Products, ProductImage,ProductCategory, Bids,WinningBid,Auction_Details
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class SiteUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()


    class Meta:
        model = SiteUser
        fields = ['id','user', 'phone']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            site_user = SiteUser.objects.create(user=user, **validated_data)
            return site_user
        else:
            raise serializers.ValidationError(user_serializer.errors)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    

class UserDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SiteUser
        fields = ['id','user','phone']
        depth = 1

        def __str__(self):
            return f'self.user" "self.phone'
        def create(self, validated_data):
            user_data = validated_data.pop('user')
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                site_user = SiteUser.objects.create(user=user, **validated_data)
                return site_user
            else:
                raise serializers.ValidationError(user_serializer.errors)

class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    
        
class ProductListSerializer(serializers.ModelSerializer):

    product_images= serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Products
        fields = ['id','product_images','name','category','description', 'initial_price','updated_at','created_at']
        # depth = 1

        def __str__(self):
            return f'self.name" "self.category" "self.initial_price'
        
class ProductDetailSerializer(serializers.ModelSerializer):
    product_images= serializers.StringRelatedField(many=True, read_only=True)
    product_bids= serializers.StringRelatedField(many=True, read_only=True)
     
    class Meta:
        model = Products
        fields = ['id','product_images','name','category','description', 'initial_price','product_bids','updated_at','created_at']
        depth = 1

        def __str__(self):
            return f'self.name" "self.category" "self.initial_price'
    

class ProductImageSerializer(serializers.ModelSerializer):
     # Define allowed image formats as a class attribute
    ALLOWED_IMAGE_FORMATS = ['image/png', 'image/jpeg']

    def validate_image(self, value):
        # Check if the image is in the allowed format
        if value.content_type not in self.ALLOWED_IMAGE_FORMATS:
            raise serializers.ValidationError("Only JPEG and PNG images are allowed.")

        # Check if the image size is within the allowed limit (e.g., 2MB)
        max_size = 2 * 1024 * 1024  # 2MB
        if value.size > max_size:
            raise serializers.ValidationError("Image size exceeds the allowed limit (2MB).")

        return value

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product']  # Include 'product' field explicitly
        # depth = 1
        extra_kwargs = {
            'product': {'required': True},  # Ensure 'product' field is required
        }

    # Define the __str__ method outside the Meta class
    def __str__(self):
        return f'{self.product} {self.image}' 


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id','title','detail']
        

        def __str__(self):
            return f'self.title" "self.detail'

class ProductCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id','title','detail']
        depth = 1

        def __str__(self):
            return f'self.title" "self.detail'

        
class InternetProductSearchSerializer(serializers.Serializer):
    asin = serializers.CharField()
    product_title = serializers.CharField()
    product_price = serializers.CharField()
    currency = serializers.CharField()
    # Add other fields as needed

 
# bids
class BidsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bids
        fields = ['id','bidder','product','price','created_at']
        # depth = 1

        def __str__(self):
            return f'self.bidder" "self.product" "self.price'
    

        
class BidsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bids
        fields = ['id','bidder','product','price','created_at']
        depth = 1

        def __str__(self):
            return f'self.bidder" "self.product" "self.price'
        

class BidsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bids
        fields = ['id','bidder','product','price','created_at']
        depth = 1

        def __str__(self):
            return f'self.bidder" "self.product" "self.price'
        

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction_Details
        fields = ['id','product','start_time','end_time']
        # depth = 1

        def __str__(self):
            return f'self.product'
    
class AuctionDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Auction_Details
        fields = ['id','product','start_time','end_time']
        depth = 1

        def __str__(self):
            return f'self.product'
        

