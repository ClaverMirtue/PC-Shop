from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from .models import (
    Category, Company, Product, ProductImage, Review,
    Cart, CartItem, Order, OrderItem, UserProfile,
    Newsletter, ContactMessage
)
from .forms import (
    UserRegistrationForm, UserLoginForm, UserProfileForm,
    ReviewForm, ContactForm, NewsletterForm, OrderForm
)
from django.utils.text import slugify
from django.template.loader import get_template

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'pcapp/register.html', context)

# User Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

# Home Page
def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True)[:8]
    discounted_products = Product.objects.filter(discount_percentage__gt=0).order_by('-discount_percentage')[:8]
    
    # Ensure all categories have a slug
    for category in categories:
        if not category.slug:
            category.slug = slugify(category.name)
            category.save()
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'discounted_products': discounted_products,
    }
    return render(request, 'pcapp/home.html', context)

# Category Page
def category_detail(request, slug):
    # Ensure slug is not empty
    if not slug:
        messages.error(request, "Invalid URL parameter.")
        return redirect('home')
        
    try:
        category = get_object_or_404(Category, slug=slug)
        companies = category.companies.all()
        
        context = {
            'category': category,
            'companies': companies,
        }
        return render(request, 'pcapp/category_detail.html', context)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

# Company Products Page
def company_products(request, category_slug, company_slug):
    # Ensure slugs are not empty
    if not category_slug or not company_slug:
        messages.error(request, "Invalid URL parameters.")
        return redirect('home')
        
    try:
        category = get_object_or_404(Category, slug=category_slug)
        company = get_object_or_404(Company, slug=company_slug)
        
        products = Product.objects.filter(category=category, company=company)
        
        # Filtering
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        sort_by = request.GET.get('sort_by', 'name')
        
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        
        # Sorting
        if sort_by == 'price_low':
            products = products.order_by('price')
        elif sort_by == 'price_high':
            products = products.order_by('-price')
        elif sort_by == 'newest':
            products = products.order_by('-created_at')
        else:  # Default: name
            products = products.order_by('name')
        
        # Pagination
        paginator = Paginator(products, 12)  # 12 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'category': category,
            'company': company,
            'page_obj': page_obj,
            'min_price': min_price,
            'max_price': max_price,
            'sort_by': sort_by,
        }
        return render(request, 'pcapp/company_products.html', context)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

# Product Detail Page
def product_detail(request, category_slug, company_slug, product_slug):
    # Ensure slugs are not empty
    if not category_slug or not company_slug or not product_slug:
        messages.error(request, "Invalid URL parameters.")
        return redirect('home')
        
    try:
        product = get_object_or_404(
            Product,
            slug=product_slug,
            category__slug=category_slug,
            company__slug=company_slug
        )
        
        # Get product images
        images = product.images.all()
        
        # Get related products
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]
        
        # Get reviews
        reviews = product.reviews.all().order_by('-created_at')
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        review_count = reviews.count()
        
        # Review form
        if request.method == 'POST' and request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review, created = Review.objects.update_or_create(
                    product=product,
                    user=request.user,
                    defaults={
                        'rating': form.cleaned_data['rating'],
                        'comment': form.cleaned_data['comment']
                    }
                )
                messages.success(request, 'Your review has been submitted.')
                return redirect('product_detail', category_slug=category_slug, 
                               company_slug=company_slug, product_slug=product_slug)
        else:
            form = ReviewForm()
        
        context = {
            'product': product,
            'category': product.category,
            'company': product.company,
            'images': images,
            'related_products': related_products,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'review_count': review_count,
            'form': form,
        }
        return render(request, 'pcapp/product_detail.html', context)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

# Search Products
def search_products(request):
    query = request.GET.get('q', '')
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(company__name__icontains=query)
        ).distinct()
    else:
        products = Product.objects.none()
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
    }
    return render(request, 'pcapp/search_results.html', context)

# Cart Management
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'pcapp/cart.html', context)

@login_required
@require_POST
def add_to_cart(request):
    try:
        product_id = request.POST.get('product_id')
        if not product_id:
            return JsonResponse({
                'success': False,
                'message': 'Product ID is required'
            }, status=400)
            
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid quantity'
            }, status=400)
        
        product = get_object_or_404(Product, id=product_id)
        
        # Check if product is available
        if not product.is_available or product.stock <= 0:
            return JsonResponse({
                'success': False,
                'message': f'{product.name} is currently out of stock'
            }, status=400)
            
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        # Check if requested quantity exceeds stock
        if cart_item.quantity > product.stock:
            cart_item.quantity = product.stock
            cart_item.save()
            message = f'Only {product.stock} units of {product.name} are available. Your cart has been updated.'
        else:
            message = f'{product.name} added to cart'
        
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_total': cart.total_items
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)

@login_required
@require_POST
def update_cart(request):
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    cart = cart_item.cart
    
    return JsonResponse({
        'success': True,
        'item_total': cart_item.total_price if quantity > 0 else 0,
        'cart_total': cart.total_price,
        'cart_items': cart.total_items
    })

@login_required
@require_POST
def remove_from_cart(request):
    item_id = request.POST.get('item_id')
    
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart = cart_item.cart
    cart_item.delete()
    
    return JsonResponse({
        'success': True,
        'message': f'{cart_item.product.name} removed from cart',
        'cart_total': cart.total_price,
        'cart_items': cart.total_items
    })

# Checkout and Order
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('view_cart')
    
    # Get user profile for pre-filling the form
    try:
        profile = request.user.profile
        initial_data = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'phone': profile.phone,
            'address': profile.address,
            'city': profile.city,
            'state': profile.state,
            'pincode': profile.pincode,
        }
    except UserProfile.DoesNotExist:
        initial_data = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.total_price
            order.save()
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.product.discounted_price,
                    quantity=cart_item.quantity
                )
            
            # Clear the cart
            cart_items.delete()
            
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = OrderForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'pcapp/checkout.html', context)

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'pcapp/order_confirmation.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'pcapp/order_history.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'pcapp/order_detail.html', context)

# User Profile
@login_required
def user_profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'pcapp/user_profile.html', context)

# About Us Page
def about_us(request):
    return render(request, 'pcapp/about_us.html')

# Contact Us Page
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. We will get back to you soon.')
            return redirect('contact_us')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'pcapp/contact_us.html', context)

# Newsletter Subscription
@require_POST
def subscribe_newsletter(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'message': 'Thank you for subscribing to our newsletter!'
        })
    return JsonResponse({
        'success': False,
        'message': 'Invalid email address.'
    })

# Compatibility Checker Tool
def compatibility_checker(request):
    # This is a simplified version. In a real application, you would need
    # to implement a more sophisticated compatibility checking logic.
    cpu = request.GET.get('cpu')
    motherboard = request.GET.get('motherboard')
    ram = request.GET.get('ram')
    gpu = request.GET.get('gpu')
    
    context = {
        'cpu': cpu,
        'motherboard': motherboard,
        'ram': ram,
        'gpu': gpu,
        'is_compatible': True,  # Placeholder
        'compatibility_notes': []  # Placeholder
    }
    return render(request, 'pcapp/compatibility_checker.html', context)

def test_view(request):
    return render(request, 'pcapp/cart_test.html', {'message': 'This is a test view.'})

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'pcapp/cart_test.html', context) 