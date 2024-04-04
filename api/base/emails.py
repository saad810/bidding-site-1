from django.core.mail import send_mail
from django.conf import settings
import random
from .models import SiteUser

def send_otp_email(email):
    try:
        subject = f'Your OTP for registration Verification'
        otp = random.randint(1000, 9999)
        message = f'Your OTP is {otp}'
        email_from = settings.EMAIL_HOST_USER  # Use the sender email configured in your settings
        send_mail(subject, message, email_from, [email])
        
        # Save OTP to SiteUser model
        user_obj = SiteUser.objects.get(user__email=email)
        user_obj.otp = otp
        user_obj.save()
        
        return True, 'OTP sent successfully'
    except Exception as e:
        return False, str(e)

def send_bid_email(email, product_name, product_price, placed_at, owner_mail):
    try:
        subject = f'New bid on {product_name}'
        email_from = settings.EMAIL_HOST_USER  # Use the sender email configured in your settings
        if owner_mail is not None:
            message = f'New Bid Placed on {product_name} at price {product_price} at {placed_at}.'
            send_mail(subject, message, email_from, [owner_mail])
        else:
            message = f'You placed a new bid on {product_name} at price {product_price} at {placed_at}.'
            send_mail(subject, message, email_from, [email])
        
        return True, 'Email sent successfully'
    except Exception as e:
        return False, str(e)

def send_Auction_email(email, product_name, product_price, start_time, end_time):
    try:
        subject = f'Auction Created Successfully'
        email_from = settings.EMAIL_HOST_USER  # Use the sender email configured in your settings
        
        message = f"""
    <html>
    <head>
        <style>
            h3 {{
                color: #007bff;
            }}
            p {{
                font-size: 16px;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <h3>Auction has been created Successfully</h3>
        <p><strong>Product Name:</strong> {product_name}</p>
        <p><strong>Start Time:</strong> {start_time}</p>
        <p><strong>Ending Time:</strong> {end_time}</p>
        <p><strong>Expected Price:</strong> {product_price}</p>
    </body>
    </html>
"""

        send_mail(subject, message, email_from, [email])
        
        return True, 'Email sent successfully'
    except Exception as e:
        return False, str(e)
