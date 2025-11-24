from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, Http404
from django.db.models import Q, Avg, Sum
from django.db import models
from django.utils import timezone
from django.utils import timezone
from decimal import Decimal
import json
from .models import Product, Customer, Cart, CartItem, Order, OrderItem, Contact, ContactReply, Review, OrderTracking, Category, CustomerSupport, SupportMessage, CustomerFeedback
# Payment imports - will be enabled after migration
# from .payment_service import get_payment_service
from .forms import ContactForm, CustomUserCreationForm, AddToCartForm, ReviewForm, AdminRegistrationForm
from .decorators import admin_required
import random
import string

FEEDBACK_RESPONSE_SUBJECT_PREFIX = "response to your feedback:"

def _is_feedback_response_subject(subject):
    if not subject:
        return False
    return subject.strip().lower().startswith(FEEDBACK_RESPONSE_SUBJECT_PREFIX)

def home(request):
    """Homepage view with featured products and combos"""
    featured_products = Product.objects.filter(is_featured=True)[:3]
    combo_deals = Product.objects.filter(product_type='bundles')[:3]
    seasonal_items = Product.objects.filter(product_type='fresh-corn')[:3]
    
    context = {
        'featured_products': featured_products,
        'combo_deals': combo_deals,
        'seasonal_items': seasonal_items,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page view"""
    featured_reviews = Review.objects.filter(is_featured=True)[:3]
    bestselling_products = Product.objects.filter(is_bestseller=True)[:3]
    
    context = {
        'featured_reviews': featured_reviews,
        'bestselling_products': bestselling_products,
    }
    return render(request, 'core/about.html', context)


def products(request):
    """Products listing page with filtering and sorting"""
    products_list = Product.objects.all()
    categories = Category.objects.all()
    
    # Filtering
    category_filter = request.GET.get('category')
    price_filter = request.GET.get('price')
    sort_by = request.GET.get('sort', 'newest')
    free_delivery = request.GET.get('free_delivery')
    search_query = request.GET.get('search')
    
    if category_filter and category_filter != 'all':
        products_list = products_list.filter(product_type=category_filter)
    
    if price_filter and price_filter != 'all':
        if price_filter == '100-500':
            products_list = products_list.filter(price__gte=100, price__lte=500)
    
    if free_delivery:
        products_list = products_list.filter(free_delivery=True)
    
    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Sorting
    if sort_by == 'newest':
        products_list = products_list.order_by('-created_at')
    elif sort_by == 'bestseller':
        products_list = products_list.order_by('-is_bestseller', '-created_at')
    elif sort_by == 'price-low-high':
        products_list = products_list.order_by('price')
    elif sort_by == 'price-high-low':
        products_list = products_list.order_by('-price')
    
    # Pagination
    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    # Featured combos
    featured_combos = Product.objects.filter(product_type='bundles', is_featured=True)[:2]
    
    # Customer reviews
    customer_reviews = Review.objects.filter(is_featured=True)[:3]
    
    context = {
        'products': products,
        'categories': categories,
        'featured_combos': featured_combos,
        'customer_reviews': customer_reviews,
        'current_category': category_filter,
        'current_price': price_filter,
        'current_sort': sort_by,
        'search_query': search_query,
    }
    return render(request, 'core/products.html', context)


def product_detail(request, slug):
    """Individual product detail page"""
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()[:5]
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Forms
    add_to_cart_form = AddToCartForm()
    review_form = ReviewForm() if request.user.is_authenticated else None
    
    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'avg_rating': avg_rating,
        'add_to_cart_form': add_to_cart_form,
        'review_form': review_form,
    }
    return render(request, 'core/product_detail.html', context)


def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.user = request.user
                contact.name = contact.name or (request.user.get_full_name() or request.user.username)
                contact.email = contact.email or request.user.email
            contact.save()
            messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
            if request.user.is_authenticated:
                return redirect('contact_conversation', contact_id=contact.id)
            return redirect('contact')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
            }
        form = ContactForm(initial=initial)
    
    user_contacts = None
    if request.user.is_authenticated:
        user_contacts = Contact.objects.filter(user=request.user)\
            .exclude(subject__iregex=r'^\s*response to your feedback:')\
            .order_by('-last_updated')
    
    context = {
        'form': form,
        'user_contacts': user_contacts,
    }
    return render(request, 'core/contact.html', context)


@login_required
def my_messages(request):
    """List of contact conversations for the logged-in user"""
    contacts = Contact.objects.filter(user=request.user)\
        .exclude(subject__iregex=r'^\s*response to your feedback:')\
        .prefetch_related('replies__sender')\
        .order_by('-last_updated')
    contacts = list(contacts)
    for contact in contacts:
        replies = list(contact.replies.all())
        latest_reply = replies[-1] if replies else None
        if latest_reply:
            contact.latest_message = latest_reply.message
            contact.latest_message_sender = 'admin' if latest_reply.is_admin else 'customer'
            contact.latest_message_time = latest_reply.created_at
        else:
            contact.latest_message = contact.message
            contact.latest_message_sender = 'customer'
            contact.latest_message_time = contact.created_at
    context = {
        'contacts': contacts,
    }
    return render(request, 'core/my_messages.html', context)


@login_required
def contact_conversation(request, contact_id):
    """Detailed conversation thread for a contact message"""
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if _is_feedback_response_subject(contact.subject):
        return redirect('customer_feedback')
    replies = contact.replies.select_related('sender').all()
    
    # Mark admin replies as read when the customer views them
    contact.replies.filter(is_admin=True, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            ContactReply.objects.create(
                contact=contact,
                sender=request.user,
                sender_name=request.user.get_full_name() or request.user.username,
                message=message_text,
                is_admin=False
            )
            contact.is_read = False  # notify admins of new reply
            contact.last_updated = timezone.now()
            contact.save(update_fields=['is_read', 'last_updated'])
            messages.success(request, 'Reply sent!')
            return redirect('contact_conversation', contact_id=contact.id)
    
    context = {
        'contact': contact,
        'replies': replies,
        'is_admin_view': False,
    }
    return render(request, 'core/contact_conversation.html', context)


def signup(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a Customer object for the new user
            Customer.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Golden Mais!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


def customer_login(request):
    """Custom customer login view with auto-redirect for logged-in users"""
    # If user is already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validate input
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'registration/login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Ensure session is saved
            request.session.modified = True
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')


@login_required
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            # Get or create cart
            cart, created = Cart.objects.get_or_create(customer=customer)
            
            # Get or create cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            if not is_ajax:
                messages.success(request, f'{product.name} added to cart!')
            
            # Always return JSON response for AJAX requests
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': f'{product.name} added to cart!',
                    'cart_count': cart.get_total_items()
                })
            
            # Check if user wants to stay on current page
            if request.POST.get('stay_on_page'):
                return redirect(request.META.get('HTTP_REFERER', 'product_detail'), slug=product.slug)
    
    return redirect('product_detail', slug=product.slug)


@login_required
def profile(request):
    """Display profile info and allow account deletion"""
    customer = getattr(request.user, 'customer', None)

    if request.method == 'POST' and request.POST.get('action') == 'delete_account':
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')

    context = {
        'customer': customer,
    }
    return render(request, 'core/profile.html', context)


@login_required
def buy_now(request, product_id):
    """Direct checkout for a single product (TikTok-style)"""
    product = get_object_or_404(Product, id=product_id)
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            # Create a temporary cart item for direct checkout
            temp_cart_item = {
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity
            }
            
            # Store in session for checkout
            request.session['buy_now_item'] = {
                'product_id': product.id,
                'quantity': quantity,
                'price': float(product.price),
                'total': float(product.price * quantity)
            }
            
            return redirect('direct_checkout')
    
    return redirect('product_detail', slug=product.slug)


@login_required
def cart_view(request):
    """Shopping cart view"""
    customer, created = Customer.objects.get_or_create(user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
    }
    return render(request, 'core/cart.html', context)


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = cart_item.cart if quantity > 0 else cart_item.cart
        return JsonResponse({
            'success': True,
            'new_quantity': quantity if quantity > 0 else 0,
            'item_total': float(cart_item.get_total_price()) if quantity > 0 else 0,
            'cart_total': float(cart.get_total_price()),
            'cart_count': cart.get_total_items(),
            'removed': quantity <= 0
        })
    
    return redirect('cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer__user=request.user)
    cart = cart_item.cart
    cart_item.delete()
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': float(cart.get_total_price()),
            'cart_count': cart.get_total_items(),
            'removed': True
        })
    
    return redirect('cart')


@login_required
def add_review(request, product_id):
    """Add product review"""
    product = get_object_or_404(Product, id=product_id)
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.customer = customer
            
            # Check if user already reviewed this product
            existing_review = Review.objects.filter(
                product=product, 
                customer=customer
            ).first()
            
            if existing_review:
                messages.warning(request, 'You have already reviewed this product!')
            else:
                review.save()
                messages.success(request, 'Thank you for your review!')
    
    return redirect('product_detail', slug=product.slug)


def search(request):
    """Search products"""
    query = request.GET.get('q', '')
    products = Product.objects.none()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'core/search_results.html', context)


# Admin Views
def admin_redirect(request):
    """Redirect /admin/ to custom admin login"""
    return redirect('admin_login')


def admin_login(request):
    """Admin login page"""
    # If user is already logged in as staff, redirect to dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    # If user is authenticated but not staff, logout first to allow admin login
    if request.user.is_authenticated and not request.user.is_staff:
        logout(request)
        messages.info(request, 'Please login with admin credentials.')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validate input
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'admin/login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            # Ensure session is saved
            request.session.modified = True
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            # Use next_page parameter if provided, otherwise go to dashboard
            next_page = request.GET.get('next', 'admin_dashboard')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'admin/login.html')


def admin_register(request):
    """Public admin registration page"""
    # If user is authenticated but not staff, logout first to allow admin registration
    if request.user.is_authenticated and not request.user.is_staff:
        logout(request)
        messages.info(request, 'Please register with admin credentials.')
    
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Staff user {user.username} created successfully! You can now login.')
            return redirect('admin_login')
    else:
        form = AdminRegistrationForm()
    
    context = {'form': form}
    return render(request, 'admin/public_register.html', context)


@admin_required
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    # Get statistics
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()
    total_reviews = Review.objects.count()
    
    # Recent activity
    recent_orders = Order.objects.order_by('-created_at')[:5]
    recent_customers = Customer.objects.order_by('-created_at')[:5]
    recent_reviews = Review.objects.order_by('-created_at')[:5]
    recent_feedback = (
        CustomerFeedback.objects
        .select_related('customer__user')
        .order_by('-created_at')[:3]
    )
    pending_contacts = (
        Contact.objects
        .exclude(subject__iregex=r'^\s*response to your feedback:')
        .filter(is_read=False)
        .count()
    )
    
    # Monthly statistics
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_orders = Order.objects.filter(created_at__gte=current_month).count()
    monthly_customers = Customer.objects.filter(created_at__gte=current_month).count()
    
    # Low stock products
    low_stock_products = Product.objects.filter(stock_quantity__lt=10)
    
    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_reviews': total_reviews,
        'recent_orders': recent_orders,
        'recent_customers': recent_customers,
        'recent_reviews': recent_reviews,
        'recent_feedback': recent_feedback,
        'pending_contacts': pending_contacts,
        'monthly_orders': monthly_orders,
        'monthly_customers': monthly_customers,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'admin/dashboard.html', context)


@admin_required
def admin_products(request):
    """Admin products management"""
    products = Product.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'search_query': search_query,
    }
    return render(request, 'admin/products.html', context)


@admin_required
def admin_product_add(request):
    """Admin add new product view"""
    categories = Category.objects.all()
    
    if request.method == 'POST':
        # Create new product
        from django.utils.text import slugify
        
        name = request.POST.get('name')
        slug = slugify(name)
        
        # Ensure unique slug
        original_slug = slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        product = Product.objects.create(
            name=name,
            slug=slug,
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            stock_quantity=request.POST.get('stock_quantity'),
            product_type=request.POST.get('product_type'),
            is_featured='is_featured' in request.POST,
            is_bestseller='is_bestseller' in request.POST,
            is_new='is_new' in request.POST,
            free_delivery='free_delivery' in request.POST,
        )
        
        # Handle image upload
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            product.save()
        
        messages.success(request, f'Product "{product.name}" created successfully!')
        return redirect('admin_products')
    
    context = {
        'categories': categories,
        'product_types': Product.PRODUCT_TYPES,
    }
    return render(request, 'admin/product_add.html', context)


@admin_required
def admin_product_edit(request, product_id):
    """Admin product edit view"""
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        # Update product fields
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock_quantity = request.POST.get('stock_quantity')
        product.product_type = request.POST.get('product_type')
        
        # Handle category
        category_id = request.POST.get('category')
        if category_id:
            product.category = Category.objects.get(id=category_id)
        
        # Handle boolean fields
        product.is_featured = 'is_featured' in request.POST
        product.is_bestseller = 'is_bestseller' in request.POST
        product.is_new = 'is_new' in request.POST
        product.free_delivery = 'free_delivery' in request.POST
        
        # Handle image upload
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        product.save()
        messages.success(request, f'Product "{product.name}" updated successfully!')
        return redirect('admin_products')
    
    context = {
        'product': product,
        'categories': categories,
        'product_types': Product.PRODUCT_TYPES,
    }
    return render(request, 'admin/product_edit.html', context)


@admin_required
def admin_product_view(request, product_id):
    """Admin product view (detailed view for admin)"""
    product = get_object_or_404(Product, id=product_id)
    
    # Get product reviews
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'admin/product_view.html', context)


@admin_required
def admin_quick_stock_update(request):
    """Handle quick stock adjustments from dashboard"""
    if request.method != 'POST':
        messages.error(request, 'Invalid stock update request.')
        return redirect('admin_dashboard')

    product_id = request.POST.get('product_id')
    operation = request.POST.get('operation', 'set')
    quantity_value = request.POST.get('quantity')

    try:
        quantity = int(quantity_value)
        if quantity < 0:
            raise ValueError
    except (TypeError, ValueError):
        messages.error(request, 'Please provide a valid quantity (0 or higher).')
        return redirect('admin_dashboard')

    product = get_object_or_404(Product, id=product_id)

    if operation == 'add':
        product.stock_quantity = product.stock_quantity + quantity
        action = 'added to'
    else:
        product.stock_quantity = quantity
        action = 'updated for'

    product.save(update_fields=['stock_quantity'])
    messages.success(request, f'Stock {action} {product.name}: now {product.stock_quantity} items available.')
    return redirect('admin_dashboard')


@admin_required
def admin_orders(request):
    """Admin orders management"""
    orders = Order.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'admin/orders.html', context)


@admin_required
def admin_order_details(request, order_id):
    """Admin order details view"""
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    tracking_updates = OrderTracking.objects.filter(order=order).order_by('-created_at')
    
    context = {
        'order': order,
        'order_items': order_items,
        'tracking_updates': tracking_updates,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'admin/order_details.html', context)


@admin_required
def admin_customers(request):
    """Admin customers management"""
    customers = Customer.objects.all().order_by('-created_at')
    
    # Search functionality
    raw_search_query = (request.GET.get('search') or '').strip()
    normalized_query = raw_search_query.lstrip('@')
    if normalized_query:
        customers = customers.filter(
            Q(user__username__icontains=normalized_query) |
            Q(user__email__icontains=normalized_query) |
            Q(user__first_name__icontains=normalized_query) |
            Q(user__last_name__icontains=normalized_query)
        )
    
    # Pagination
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    customers = paginator.get_page(page_number)
    
    # Metrics for floating cards
    total_customers_count = Customer.objects.count()
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_new_customers = Customer.objects.filter(created_at__gte=current_month).count()
    total_orders_overall = Order.objects.count()
    average_orders_per_customer = 0
    if total_customers_count > 0:
        average_orders_per_customer = round(total_orders_overall / total_customers_count, 1)
    
    context = {
        'customers': customers,
        'search_query': raw_search_query,
        'total_customers_count': total_customers_count,
        'monthly_new_customers': monthly_new_customers,
        'average_orders_per_customer': average_orders_per_customer,
    }
    return render(request, 'admin/customers.html', context)


@admin_required
def admin_customer_edit(request, customer_id):
    """Admin customer edit view"""
    customer = get_object_or_404(Customer, id=customer_id)
    user = customer.user
    
    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.username = request.POST.get('username', '')
        
        # Update customer fields
        customer.phone = request.POST.get('phone', '')
        customer.address = request.POST.get('address', '')
        customer.city = request.POST.get('city', '')
        
        # Handle user status
        user.is_active = 'is_active' in request.POST
        
        try:
            user.save()
            customer.save()
            messages.success(request, f'Customer "{user.get_full_name() or user.username}" updated successfully!')
            return redirect('admin_customers')
        except Exception as e:
            messages.error(request, f'Error updating customer: {str(e)}')
    
    context = {
        'customer': customer,
        'user': user,
    }
    return render(request, 'admin/customer_edit.html', context)


@admin_required
def admin_customer_view(request, customer_id):
    """Admin customer view (detailed view for admin)"""
    customer = get_object_or_404(Customer, id=customer_id)
    user = customer.user
    
    # Get customer orders
    orders = Order.objects.filter(customer=customer).order_by('-created_at')[:10]
    
    # Get customer reviews
    reviews = Review.objects.filter(customer=customer).order_by('-created_at')[:5]
    
    # Calculate statistics
    total_orders = Order.objects.filter(customer=customer).count()
    total_spent = Order.objects.filter(customer=customer).aggregate(
        total=Sum('total')
    )['total'] or 0
    
    context = {
        'customer': customer,
        'user': user,
        'orders': orders,
        'reviews': reviews,
        'total_orders': total_orders,
        'total_spent': total_spent,
    }
    return render(request, 'admin/customer_view.html', context)


@admin_required
def admin_contacts(request):
    """Admin contact messages management"""
    contacts = Contact.objects.exclude(subject__iregex=r'^\s*response to your feedback:')\
        .prefetch_related('replies__sender')\
        .order_by('-created_at')
    
    # Filter by read status
    status_filter = request.GET.get('status')
    if status_filter == 'unread':
        contacts = contacts.filter(is_read=False)
    elif status_filter == 'read':
        contacts = contacts.filter(is_read=True)
    
    # Pagination
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    contacts = paginator.get_page(page_number)
    for contact in contacts:
        replies = list(contact.replies.all())
        latest_reply = replies[-1] if replies else None
        if latest_reply:
            contact.latest_message = latest_reply.message
            contact.latest_message_sender = 'admin' if latest_reply.is_admin else 'customer'
            contact.latest_message_time = latest_reply.created_at
        else:
            contact.latest_message = contact.message
            contact.latest_message_sender = 'customer'
            contact.latest_message_time = contact.created_at
    
    context = {
        'contacts': contacts,
        'status_filter': status_filter,
    }
    return render(request, 'admin/contacts.html', context)


@admin_required
def admin_contact_view(request, contact_id):
    """Admin contact view (detailed view for admin)"""
    contact = get_object_or_404(Contact, id=contact_id)
    if _is_feedback_response_subject(contact.subject):
        return redirect('admin_feedback_dashboard')
    replies = contact.replies.select_related('sender').all()
    
    # Mark conversation as read for admins
    if not contact.is_read:
        contact.is_read = True
        contact.save(update_fields=['is_read'])
    contact.replies.filter(is_admin=False, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            ContactReply.objects.create(
                contact=contact,
                sender=request.user,
                sender_name=request.user.get_full_name() or request.user.username,
                message=message_text,
                is_admin=True,
                is_read=True
            )
            contact.is_read = True
            contact.last_updated = timezone.now()
            contact.save(update_fields=['is_read', 'last_updated'])
            messages.success(request, 'Reply sent successfully!')
            return redirect('admin_contact_view', contact_id=contact.id)
    
    context = {
        'contact': contact,
        'replies': replies,
    }
    return render(request, 'admin/contact_view.html', context)
@admin_required
def admin_add_staff(request):
    """Admin add staff view"""
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            try:
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_staff=True,  # Make them staff
                    is_active=True
                )
                
                # Create customer profile for the staff user
                Customer.objects.create(user=user)
                
                messages.success(request, f'Staff member "{user.get_full_name() or user.username}" created successfully!')
                return redirect('admin_add_staff')
                
            except Exception as e:
                messages.error(request, f'Error creating staff member: {str(e)}')
    
    # Get all staff members for display
    staff_members = User.objects.filter(is_staff=True).order_by('-date_joined')
    
    context = {
        'staff_members': staff_members,
    }
    return render(request, 'admin/add_staff.html', context)


@admin_required
@require_POST
def mark_contact_read(request, contact_id):
    """Mark contact message as read"""
    contact = get_object_or_404(Contact, id=contact_id)
    contact.is_read = True
    contact.save()
    messages.success(request, 'Message marked as read.')
    return redirect('admin_contacts')



@admin_required
def update_order_status(request, order_id):
    """Update order status with tracking"""
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        tracking_message = request.POST.get('tracking_message', '')
        location = request.POST.get('location', '')
        
        if new_status in dict(Order.STATUS_CHOICES):
            old_status = order.status
            order.status = new_status
            
            # Set tracking number if moving to shipped status
            if new_status == 'shipped' and not order.tracking_number:
                import random
                import string
                order.tracking_number = 'GM' + ''.join(random.choices(string.digits, k=8))
            
            # Set estimated delivery if moving to shipped
            if new_status == 'shipped' and not order.estimated_delivery:
                from datetime import datetime, timedelta
                order.estimated_delivery = datetime.now() + timedelta(days=3)
            
            # Set delivered timestamp
            if new_status == 'delivered' and not order.delivered_at:
                from datetime import datetime
                order.delivered_at = datetime.now()
            
            order.save()
            
            # Create tracking update
            OrderTracking.objects.create(
                order=order,
                status=new_status,
                message=tracking_message or f'Order status updated to {order.get_status_display()}',
                location=location,
                updated_by=request.user.get_full_name() or request.user.username
            )
            
            messages.success(request, f'Order #{order.order_number} status updated from {old_status} to {new_status}')
    
    return redirect('admin_orders')


@admin_required
def cancel_order(request, order_id):
    """Cancel an order"""
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Only allow cancellation if order is not already delivered or cancelled
        if order.status not in ('delivered', 'cancelled'):
            old_status = order.status
            order.status = 'cancelled'
            order.save()
            
            # Create tracking update
            cancellation_reason = request.POST.get('cancellation_reason', 'Order cancelled by admin')
            OrderTracking.objects.create(
                order=order,
                status='cancelled',
                message=cancellation_reason,
                location='Golden Mais Farm, Calubian, Leyte',
                updated_by=request.user.get_full_name() or request.user.username
            )
            
            messages.success(request, f'Order #{order.order_number} has been cancelled.')
        else:
            messages.error(request, f'Cannot cancel order #{order.order_number}. Order is already {order.get_status_display()}.')
    
    return redirect('admin_order_details', order_id=order_id)


@login_required
def checkout(request):
    """Checkout view"""
    customer, _ = Customer.objects.get_or_create(user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')

    subtotal = sum(item.product.price * item.quantity for item in cart_items)

    def _checkout_context(**overrides):
        base_context = {
            'cart_items': cart_items,
            'total_amount': subtotal,
            'customer': customer,
            'preselected_payment': overrides.get('preselected_payment', request.GET.get('payment', 'cash')),
            'selected_delivery_method': overrides.get('selected_delivery_method', 'pickup'),
            'phone_value': overrides.get('phone_value', customer.phone or ''),
            'delivery_address_value': overrides.get('delivery_address_value', getattr(customer, 'address', '')),
            'notes_value': overrides.get('notes_value', ''),
            'digital_payment_error': overrides.get('digital_payment_error', False),
        }
        base_context.update(overrides)
        return base_context

    if request.method == 'POST':
        delivery_method = request.POST.get('delivery_method', 'pickup')
        delivery_address = request.POST.get('delivery_address', '')
        phone = request.POST.get('phone', customer.phone or '')
        notes = request.POST.get('notes', '')
        payment_method = request.POST.get('payment_method', 'cash')
        payment_confirmed = request.POST.get('payment_confirmed') == 'true'

        # Validate stock availability for all items
        stock_errors = []
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock_quantity:
                stock_errors.append(
                    f"{cart_item.product.name}: Only {cart_item.product.stock_quantity} in stock, "
                    f"but you ordered {cart_item.quantity}."
                )
        
        if stock_errors:
            for error in stock_errors:
                messages.error(request, error)
            context = _checkout_context(
                preselected_payment=payment_method,
                selected_delivery_method=delivery_method,
                phone_value=phone,
                delivery_address_value=delivery_address,
                notes_value=notes,
            )
            return render(request, 'core/checkout.html', context)

        if payment_method in ('gcash', 'maya'):
            # Redirect to GCash/PayMaya with phone number and order details
            order_items_text = '\n'.join([
                f"- {item.product.name}: {item.quantity}x ₱{item.product.price}"
                for item in cart_items
            ])
            delivery_fee = Decimal('50.00') if delivery_method == 'delivery' else Decimal('0.00')
            total = subtotal + delivery_fee
            
            message = f"Golden Mais Order:\n{order_items_text}\nDelivery: ₱{delivery_fee}\nTotal: ₱{total}"
            phone_number = "09631186511"
            
            # For GCash/PayMaya, redirect to messaging app with order details
            import urllib.parse
            encoded_message = urllib.parse.quote(message)
            
            # Create order first to track the payment attempt
            order = Order.objects.create(
                customer=customer,
                delivery_method=delivery_method,
                delivery_address=delivery_address,
                phone=phone,
                notes=notes,
                status='pending',
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                total=total
            )
            
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            OrderTracking.objects.create(
                order=order,
                status='pending',
                message='Order placed. Awaiting payment via GCash/PayMaya. Please send payment to the provided number.',
                location='Golden Mais Farm, Calubian, Leyte',
                updated_by='System'
            )
            
            # Clear cart
            cart_items.delete()
            
            messages.success(request, f'Order #{order.order_number} created! Please send payment via GCash/PayMaya.')
            
            # Redirect to messaging (SMS/WhatsApp)
            return redirect(f'https://wa.me/{phone_number}?text={encoded_message}')

        # Update customer phone if provided
        if phone and phone != customer.phone:
            customer.phone = phone
            customer.save()

        delivery_fee = Decimal('50.00') if delivery_method == 'delivery' else Decimal('0.00')
        total = subtotal + delivery_fee

        order = Order.objects.create(
            customer=customer,
            delivery_method=delivery_method,
            delivery_address=delivery_address,
            phone=phone,
            notes=notes,
            status='pending',
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        OrderTracking.objects.create(
            order=order,
            status='pending',
            message='Order has been placed successfully. We will start preparing your fresh corn products.',
            location='Golden Mais Farm, Calubian, Leyte',
            updated_by='System'
        )

        cart_items.delete()

        messages.success(request, f'Order #{order.order_number} placed successfully!')
        return redirect('order_success', order_id=order.id)

    context = _checkout_context()
    return render(request, 'core/checkout.html', context)


@login_required
def direct_checkout(request):
    """Direct checkout for Buy Now functionality (TikTok-style)"""
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    # Get buy now item from session
    buy_now_item = request.session.get('buy_now_item')
    if not buy_now_item:
        messages.error(request, 'No item selected for direct checkout.')
        return redirect('products')
    
    product = get_object_or_404(Product, id=buy_now_item['product_id'])
    
    if request.method == 'POST':
        # Get form data
        delivery_method = request.POST.get('delivery_method', 'pickup')
        delivery_address = request.POST.get('delivery_address', '')
        phone = request.POST.get('phone', customer.phone or '')
        notes = request.POST.get('notes', '')
        payment_method = request.POST.get('payment_method', 'cash')
        
        # Update customer phone if provided
        if phone and phone != customer.phone:
            customer.phone = phone
            customer.save()
        
        # Calculate totals
        subtotal = Decimal(str(buy_now_item['total']))
        delivery_fee = Decimal('50.00') if delivery_method == 'delivery' else Decimal('0.00')
        total = subtotal + delivery_fee
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            delivery_method=delivery_method,
            delivery_address=delivery_address,
            phone=phone,
            notes=notes,
            status='pending',
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total
        )
        
        # Create order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=buy_now_item['quantity'],
            price=Decimal(str(buy_now_item['price']))
        )
        
        # Create initial tracking entry
        OrderTracking.objects.create(
            order=order,
            status='pending',
            message='Order has been placed successfully. We will start preparing your fresh corn products.',
            location='Golden Mais Farm, Calubian, Leyte',
            updated_by='System'
        )
        
        # Clear session
        del request.session['buy_now_item']
        
        messages.success(request, f'Order #{order.order_number} placed successfully!')
        return redirect('order_success', order_id=order.id)
    
    # Calculate totals for display
    subtotal = Decimal(str(buy_now_item['total']))
    delivery_fee = Decimal('50.00')  # Default delivery fee
    total_with_delivery = subtotal + delivery_fee
    
    context = {
        'product': product,
        'quantity': buy_now_item['quantity'],
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total_with_delivery': total_with_delivery,
        'total_pickup': subtotal,
        'customer': customer,
        'is_direct_checkout': True,
    }
    return render(request, 'core/direct_checkout.html', context)


@login_required
def order_success(request, order_id):
    """Order success page"""
    customer, created = Customer.objects.get_or_create(user=request.user)
    order = get_object_or_404(Order, id=order_id, customer=customer)
    
    context = {
        'order': order,
    }
    return render(request, 'core/order_success.html', context)


@login_required
def track_order(request, order_number):
    """Order tracking page with progress timeline"""
    customer, created = Customer.objects.get_or_create(user=request.user)
    order = get_object_or_404(Order, order_number=order_number, customer=customer)
    
    # Get all tracking updates ordered by newest first
    tracking_updates = order.tracking_updates.all().order_by('-created_at')
    
    # Calculate progress percentage based on status
    progress_map = {
        'pending': 10,
        'confirmed': 25,
        'processing': 50,
        'ready_for_pickup': 65,
        'shipped': 85,
        'delivered': 100,
        'returned': 75,
        'cancelled': 0
    }
    progress_percentage = progress_map.get(order.status, 0)
    
    context = {
        'order': order,
        'tracking_updates': tracking_updates,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'core/track_order.html', context)


def track_order_public(request):
    """Public order tracking - no login required"""
    order = None
    tracking_updates = []
    
    if request.method == 'POST':
        order_number = request.POST.get('order_number', '').strip().upper()
        phone = request.POST.get('phone', '').strip()
        
        if order_number and phone:
            try:
                order = Order.objects.get(order_number=order_number, phone=phone)
                tracking_updates = order.tracking_updates.all()
            except Order.DoesNotExist:
                messages.error(request, 'Order not found. Please check your order number and phone number.')
    
    context = {
        'order': order,
        'tracking_updates': tracking_updates,
    }
    return render(request, 'core/track_order_public.html', context)


@login_required
def my_orders(request, status_filter='all'):
    """My Orders page with status filtering (like Shopee)"""
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    # Get all orders for the customer
    orders = Order.objects.filter(customer=customer)
    
    # Filter by status category
    if status_filter == 'to_pay':
        # Orders that are pending payment (for COD, this might be pending/confirmed)
        orders = orders.filter(status__in=['pending', 'confirmed'])
    elif status_filter == 'to_ship':
        # Orders being processed/prepared
        orders = orders.filter(status__in=['processing', 'ready_for_pickup'])
    elif status_filter == 'to_receive':
        # Orders that are shipped/out for delivery
        orders = orders.filter(status='shipped')
    elif status_filter == 'completed':
        # Orders that are delivered/completed
        orders = orders.filter(status='delivered')
    elif status_filter == 'returned':
        # Returned orders
        orders = orders.filter(status='returned')
    elif status_filter == 'cancelled':
        # Cancelled orders
        orders = orders.filter(status='cancelled')
    
    # Get counts for each status category
    status_counts = {
        'to_pay': Order.objects.filter(customer=customer, status__in=['pending', 'confirmed']).count(),
        'to_ship': Order.objects.filter(customer=customer, status__in=['processing', 'ready_for_pickup']).count(),
        'to_receive': Order.objects.filter(customer=customer, status='shipped').count(),
        'completed': Order.objects.filter(customer=customer, status='delivered').count(),
        'returned': Order.objects.filter(customer=customer, status='returned').count(),
        'cancelled': Order.objects.filter(customer=customer, status='cancelled').count(),
    }
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'status_counts': status_counts,
    }
    return render(request, 'core/my_orders.html', context)


# Customer Support Views
@login_required
def customer_support(request):
    """Customer support dashboard"""
    customer, created = Customer.objects.get_or_create(user=request.user)
    tickets = CustomerSupport.objects.filter(customer=customer)\
        .prefetch_related('messages__sender')\
        .order_by('-updated_at')
    tickets = list(tickets)
    for ticket in tickets:
        ticket.latest_admin_reply = (
            ticket.messages
            .filter(is_internal=False, sender__is_staff=True)
            .order_by('-created_at')
            .first()
        )
    
    context = {
        'tickets': tickets,
    }
    return render(request, 'core/customer_support.html', context)


@login_required
def create_support_ticket(request):
    """Create new support ticket"""
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        priority = request.POST.get('priority', 'medium')
        
        ticket = CustomerSupport.objects.create(
            customer=customer,
            subject=subject,
            description=description,
            priority=priority
        )
        
        # Create initial message
        SupportMessage.objects.create(
            ticket=ticket,
            sender=request.user,
            message=description
        )
        
        messages.success(request, f'Support ticket #{ticket.ticket_number} created successfully!')
        return redirect('support_ticket_detail', ticket_number=ticket.ticket_number)
    
    return render(request, 'core/create_support_ticket.html')


@login_required
def support_ticket_detail(request, ticket_number):
    """Support ticket detail and messaging"""
    customer, created = Customer.objects.get_or_create(user=request.user)
    ticket = get_object_or_404(CustomerSupport, ticket_number=ticket_number, customer=customer)
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            SupportMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                message=message_text
            )
            ticket.updated_at = timezone.now()
            ticket.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            
            messages.success(request, 'Message sent successfully!')
            return redirect('support_ticket_detail', ticket_number=ticket_number)
    
    ticket_messages = ticket.messages.filter(is_internal=False)
    
    context = {
        'ticket': ticket,
        'messages': ticket_messages,
    }
    return render(request, 'core/support_ticket_detail.html', context)


@login_required
def customer_feedback(request):
    """Customer feedback form"""
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        feedback_type = request.POST.get('feedback_type')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        rating = request.POST.get('rating')
        order_id = request.POST.get('order_id')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        
        CustomerFeedback.objects.create(
            customer=customer,
            feedback_type=feedback_type,
            subject=subject,
            message=message,
            rating=int(rating) if rating else None,
            order_id=order_id if order_id else None,
            is_anonymous=is_anonymous
        )
        
        messages.success(request, 'Thank you for your feedback!')
        return redirect('customer_feedback')
    
    orders = Order.objects.filter(customer=customer).order_by('-created_at')[:10]
    
    feedback_entries = CustomerFeedback.objects.filter(customer=customer).order_by('-created_at')
    context = {
        'orders': orders,
        'feedback_entries': feedback_entries,
    }
    return render(request, 'core/customer_feedback.html', context)


# Admin Support Views
@staff_member_required
def admin_support_dashboard(request):
    """Admin support dashboard"""
    tickets = CustomerSupport.objects.all()
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    
    # Filter by priority
    priority_filter = request.GET.get('priority')
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    
    # Statistics
    stats = {
        'total_tickets': CustomerSupport.objects.count(),
        'open_tickets': CustomerSupport.objects.filter(status='open').count(),
        'in_progress_tickets': CustomerSupport.objects.filter(status='in_progress').count(),
        'resolved_tickets': CustomerSupport.objects.filter(status='resolved').count(),
    }
    
    context = {
        'tickets': tickets,
        'stats': stats,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    }
    return render(request, 'admin/support_dashboard.html', context)


@staff_member_required
def admin_ticket_detail(request, ticket_number):
    """Admin ticket detail and management"""
    ticket = get_object_or_404(CustomerSupport, ticket_number=ticket_number)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if not action:
            if request.POST.get('message'):
                action = 'send_message'
            elif request.POST.get('status'):
                action = 'update_status'
        
        if action == 'send_message':
            message_text = request.POST.get('message')
            is_internal = request.POST.get('is_internal') == 'on'
            
            if message_text:
                SupportMessage.objects.create(
                    ticket=ticket,
                    sender=request.user,
                    message=message_text,
                    is_internal=is_internal
                )
                ticket.updated_at = timezone.now()
                ticket.save()
                
                messages.success(request, 'Message sent successfully!')
        
        elif action == 'update_status':
            new_status = request.POST.get('status') or ticket.status
            priority = request.POST.get('priority') or ticket.priority
            assigned_to_id = request.POST.get('assigned_to') or (ticket.assigned_to.id if ticket.assigned_to else None)
            
            ticket.status = new_status
            ticket.priority = priority
            
            if assigned_to_id:
                ticket.assigned_to = User.objects.get(id=assigned_to_id)
            
            if new_status == 'resolved':
                ticket.resolved_at = timezone.now()
            
            ticket.save()
            messages.success(request, 'Ticket updated successfully!')
        
        return redirect('admin_ticket_detail', ticket_number=ticket_number)
    
    conversation = ticket.messages.all()
    staff_users = User.objects.filter(is_staff=True)
    
    context = {
        'ticket': ticket,
        'messages': conversation,
        'staff_users': staff_users,
    }
    return render(request, 'admin/ticket_detail.html', context)


@staff_member_required
def admin_feedback_dashboard(request):
    """Admin feedback dashboard"""
    feedback_list = CustomerFeedback.objects.all()
    
    # Filter by type
    type_filter = request.GET.get('type')
    if type_filter:
        feedback_list = feedback_list.filter(feedback_type=type_filter)
    
    # Filter by rating
    rating_filter = request.GET.get('rating')
    if rating_filter:
        feedback_list = feedback_list.filter(rating=rating_filter)
    
    context = {
        'feedback_list': feedback_list,
        'type_filter': type_filter,
        'rating_filter': rating_filter,
    }
    return render(request, 'admin/feedback_dashboard.html', context)


@staff_member_required
def admin_feedback_detail(request, feedback_id):
    """Admin feedback detail and response"""
    feedback = get_object_or_404(CustomerFeedback, id=feedback_id)
    
    if request.method == 'POST':
        admin_response = request.POST.get('admin_response', '').strip()
        is_published = request.POST.get('is_published') == 'on'
        
        feedback.admin_response = admin_response
        feedback.is_published = is_published
        feedback.responded_by = request.user
        feedback.responded_at = timezone.now()
        feedback.save()
        
        # Responses stay inside the feedback module; no contact threads.
        
        messages.success(request, 'Response sent successfully!')
        return redirect('admin_feedback_detail', feedback_id=feedback_id)
    
    context = {
        'feedback': feedback,
    }
    return render(request, 'admin/feedback_detail.html', context)

