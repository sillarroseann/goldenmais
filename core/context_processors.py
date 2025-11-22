from .models import (
    Contact,
    ContactReply,
    Customer,
    Cart,
    CustomerFeedback,
    CustomerSupport,
)

def admin_context(request):
    """
    Context processor to add admin-specific data to all templates
    """
    context = {}
    
    # Only add admin context for admin pages and authenticated staff users
    if request.user.is_authenticated and request.user.is_staff:
        context['pending_contacts'] = (
            Contact.objects
            .exclude(subject__iregex=r'^\s*response to your feedback:')
            .filter(is_read=False)
            .count()
        )
        context['open_support_tickets'] = CustomerSupport.objects.exclude(status__in=['resolved', 'closed']).count()
        context['new_feedback_count'] = CustomerFeedback.objects.filter(admin_response__isnull=True).count()
    
    return context


def customer_context(request):
    """
    Context processor to add customer cart info safely
    """
    context = {}
    
    if request.user.is_authenticated:
        try:
            customer, created = Customer.objects.get_or_create(user=request.user)
            cart, created = Cart.objects.get_or_create(customer=customer)
            context['cart_items_count'] = cart.get_total_items()
            context['contact_unread_count'] = ContactReply.objects.filter(
                contact__user=request.user,
                is_admin=True,
                is_read=False
            ).exclude(contact__subject__iregex=r'^\s*response to your feedback:').count()
        except:
            context['cart_items_count'] = 0
            context['contact_unread_count'] = 0
    else:
        context['cart_items_count'] = 0
        context['contact_unread_count'] = 0
    
    return context
