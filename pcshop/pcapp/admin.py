from django.contrib import admin
from .models import (
    Category, Company, Product, ProductImage, Review,
    Cart, CartItem, Order, OrderItem, UserProfile,
    Newsletter, ContactMessage
)

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity', 'total_price')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    filter_horizontal = ('categories',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'company', 'price', 'discounted_price', 'stock', 'is_available', 'is_featured')
    list_filter = ('category', 'company', 'is_available', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('product__name', 'user__username', 'comment')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_price', 'updated_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_price', 'payment_method', 'payment_status', 'order_status', 'created_at')
    list_filter = ('payment_status', 'order_status', 'payment_method')
    search_fields = ('user__username', 'full_name', 'email', 'phone')
    inlines = [OrderItemInline]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'state')
    search_fields = ('user__username', 'phone', 'city', 'state')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('email',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

    def has_add_permission(self, request):
        return False
