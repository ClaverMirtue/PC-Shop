from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),
    
    # User Authentication
    path('register/', views.register, name='register'),
    
    # Category Pages
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # Company Products Pages
    path('category/<slug:category_slug>/company/<slug:company_slug>/', 
         views.company_products, name='company_products'),
    
    # Product Detail Page
    path('category/<slug:category_slug>/company/<slug:company_slug>/product/<slug:product_slug>/', 
         views.product_detail, name='product_detail'),
    
    # Search
    path('search/', views.search_products, name='search_products'),
    
    # Cart
    path('cart/', views.view_cart, name='view_view'),
    path('cart2/', views.cart_view, name='cart_view'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    
    # Checkout and Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # User Profile
    path('profile/', views.user_profile, name='user_profile'),
    
    # About Us
    path('about-us/', views.about_us, name='about_us'),
    
    # Contact Us
    path('contact-us/', views.contact_us, name='contact_us'),
    
    # Newsletter
    path('subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
    
    # Compatibility Checker
    path('compatibility-checker/', views.compatibility_checker, name='compatibility_checker'),
    
    # Test View
    path('test/', views.test_view, name='test_view'),
] 