from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
    path('messages/', views.my_messages, name='my_messages'),
    path('messages/<int:contact_id>/', views.contact_conversation, name='contact_conversation'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    
    # Authentication
    path('login/', views.customer_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    
    # Cart functionality
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('direct-checkout/', views.direct_checkout, name='direct_checkout'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('track-order/<str:order_number>/', views.track_order, name='track_order'),
    path('track/', views.track_order_public, name='track_order_public'),
    path('my-orders/', views.my_orders, name='my_orders_all'),
    path('my-orders/<str:status_filter>/', views.my_orders, name='my_orders'),
    
    # Reviews
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    
    # Customer Support
    path('support/', views.customer_support, name='customer_support'),
    path('support/create/', views.create_support_ticket, name='create_support_ticket'),
    path('support/ticket/<str:ticket_number>/', views.support_ticket_detail, name='support_ticket_detail'),
    path('feedback/', views.customer_feedback, name='customer_feedback'),
    
    # Admin Dashboard
    path('admin/', views.admin_redirect, name='admin_redirect'),  # Redirect /admin/ to custom admin
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-register/', views.admin_register, name='admin_register'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-products/', views.admin_products, name='admin_products'),
    path('admin-product-add/', views.admin_product_add, name='admin_product_add'),
    path('admin-product-edit/<int:product_id>/', views.admin_product_edit, name='admin_product_edit'),
    path('admin-product-view/<int:product_id>/', views.admin_product_view, name='admin_product_view'),
    path('admin-product-quick-stock/', views.admin_quick_stock_update, name='admin_quick_stock_update'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin-order-details/<int:order_id>/', views.admin_order_details, name='admin_order_details'),
    path('admin-order-cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('admin-customers/', views.admin_customers, name='admin_customers'),
    path('admin-customer-edit/<int:customer_id>/', views.admin_customer_edit, name='admin_customer_edit'),
    path('admin-customer-view/<int:customer_id>/', views.admin_customer_view, name='admin_customer_view'),
    path('admin-contacts/', views.admin_contacts, name='admin_contacts'),
    path('admin-contact-view/<int:contact_id>/', views.admin_contact_view, name='admin_contact_view'),
    path('admin-support/', views.admin_support_dashboard, name='admin_support_dashboard'),
    path('admin-support/ticket/<str:ticket_number>/', views.admin_ticket_detail, name='admin_ticket_detail'),
    path('admin-feedback/', views.admin_feedback_dashboard, name='admin_feedback_dashboard'),
    path('admin-feedback/<int:feedback_id>/', views.admin_feedback_detail, name='admin_feedback_detail'),
    path('admin-add-staff/', views.admin_add_staff, name='admin_add_staff'),
    path('mark-contact-read/<int:contact_id>/', views.mark_contact_read, name='mark_contact_read'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]
