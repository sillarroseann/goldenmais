import requests
import json
import hashlib
import hmac
import base64
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import uuid


class PaymentGatewayService:
    """
    Service class to handle payment gateway integrations for GCash and PayMaya
    """
    
    def __init__(self):
        # PayMaya Configuration
        self.paymaya_public_key = getattr(settings, 'PAYMAYA_PUBLIC_KEY', '')
        self.paymaya_secret_key = getattr(settings, 'PAYMAYA_SECRET_KEY', '')
        self.paymaya_base_url = getattr(settings, 'PAYMAYA_BASE_URL', 'https://pg-sandbox.paymaya.com')
        
        # GCash Configuration (via PayMaya)
        self.gcash_public_key = getattr(settings, 'GCASH_PUBLIC_KEY', '')
        self.gcash_secret_key = getattr(settings, 'GCASH_SECRET_KEY', '')
        self.gcash_base_url = getattr(settings, 'GCASH_BASE_URL', 'https://pg-sandbox.paymaya.com')
    
    def create_paymaya_payment(self, order, payment_obj, request):
        """
        Create PayMaya payment checkout session
        """
        try:
            # Prepare payment data
            payment_data = {
                "totalAmount": {
                    "value": float(order.total),
                    "currency": "PHP"
                },
                "buyer": {
                    "firstName": order.customer.user.first_name or "Customer",
                    "lastName": order.customer.user.last_name or "",
                    "contact": {
                        "phone": order.phone,
                        "email": order.customer.user.email
                    }
                },
                "items": [],
                "redirectUrl": {
                    "success": request.build_absolute_uri(reverse('payment_success', args=[payment_obj.id])),
                    "failure": request.build_absolute_uri(reverse('payment_failed', args=[payment_obj.id])),
                    "cancel": request.build_absolute_uri(reverse('payment_cancelled', args=[payment_obj.id]))
                },
                "requestReferenceNumber": f"GM-{order.order_number}-{payment_obj.id}",
                "metadata": {
                    "order_id": str(order.id),
                    "payment_id": str(payment_obj.id)
                }
            }
            
            # Add order items
            for item in order.items.all():
                payment_data["items"].append({
                    "name": item.product.name,
                    "quantity": item.quantity,
                    "code": str(item.product.id),
                    "description": item.product.description[:100],
                    "amount": {
                        "value": float(item.price),
                        "currency": "PHP"
                    },
                    "totalAmount": {
                        "value": float(item.price * item.quantity),
                        "currency": "PHP"
                    }
                })
            
            # Add delivery fee if applicable
            if order.delivery_fee > 0:
                payment_data["items"].append({
                    "name": "Delivery Fee",
                    "quantity": 1,
                    "code": "DELIVERY",
                    "description": "Delivery fee for your order",
                    "amount": {
                        "value": float(order.delivery_fee),
                        "currency": "PHP"
                    },
                    "totalAmount": {
                        "value": float(order.delivery_fee),
                        "currency": "PHP"
                    }
                })
            
            # Make API request to PayMaya
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {self._get_paymaya_auth_header()}'
            }
            
            response = requests.post(
                f"{self.paymaya_base_url}/v1/checkouts",
                headers=headers,
                data=json.dumps(payment_data),
                timeout=30
            )
            
            if response.status_code == 200:
                checkout_data = response.json()
                
                # Update payment object
                payment_obj.gateway_transaction_id = checkout_data.get('checkoutId')
                payment_obj.gateway_reference_number = checkout_data.get('requestReferenceNumber')
                payment_obj.gateway_response = checkout_data
                payment_obj.status = 'processing'
                payment_obj.save()
                
                return {
                    'success': True,
                    'checkout_url': checkout_data.get('redirectUrl'),
                    'checkout_id': checkout_data.get('checkoutId'),
                    'reference_number': checkout_data.get('requestReferenceNumber')
                }
            else:
                return {
                    'success': False,
                    'error': f'PayMaya API Error: {response.status_code}',
                    'details': response.text
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Payment creation failed: {str(e)}'
            }
    
    def create_gcash_payment(self, order, payment_obj, request):
        """
        Create GCash payment via PayMaya GCash integration
        """
        try:
            # Similar to PayMaya but with GCash specific configuration
            payment_data = {
                "totalAmount": {
                    "value": float(order.total),
                    "currency": "PHP"
                },
                "buyer": {
                    "firstName": order.customer.user.first_name or "Customer",
                    "lastName": order.customer.user.last_name or "",
                    "contact": {
                        "phone": order.phone,
                        "email": order.customer.user.email
                    }
                },
                "items": [],
                "redirectUrl": {
                    "success": request.build_absolute_uri(reverse('payment_success', args=[payment_obj.id])),
                    "failure": request.build_absolute_uri(reverse('payment_failed', args=[payment_obj.id])),
                    "cancel": request.build_absolute_uri(reverse('payment_cancelled', args=[payment_obj.id]))
                },
                "requestReferenceNumber": f"GM-GCASH-{order.order_number}-{payment_obj.id}",
                "metadata": {
                    "order_id": str(order.id),
                    "payment_id": str(payment_obj.id),
                    "payment_method": "gcash"
                }
            }
            
            # Add order items (same logic as PayMaya)
            for item in order.items.all():
                payment_data["items"].append({
                    "name": item.product.name,
                    "quantity": item.quantity,
                    "code": str(item.product.id),
                    "description": item.product.description[:100],
                    "amount": {
                        "value": float(item.price),
                        "currency": "PHP"
                    },
                    "totalAmount": {
                        "value": float(item.price * item.quantity),
                        "currency": "PHP"
                    }
                })
            
            if order.delivery_fee > 0:
                payment_data["items"].append({
                    "name": "Delivery Fee",
                    "quantity": 1,
                    "code": "DELIVERY",
                    "description": "Delivery fee for your order",
                    "amount": {
                        "value": float(order.delivery_fee),
                        "currency": "PHP"
                    },
                    "totalAmount": {
                        "value": float(order.delivery_fee),
                        "currency": "PHP"
                    }
                })
            
            # Use GCash credentials
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {self._get_gcash_auth_header()}'
            }
            
            response = requests.post(
                f"{self.gcash_base_url}/v1/checkouts",
                headers=headers,
                data=json.dumps(payment_data),
                timeout=30
            )
            
            if response.status_code == 200:
                checkout_data = response.json()
                
                # Update payment object
                payment_obj.gateway_transaction_id = checkout_data.get('checkoutId')
                payment_obj.gateway_reference_number = checkout_data.get('requestReferenceNumber')
                payment_obj.gateway_response = checkout_data
                payment_obj.status = 'processing'
                payment_obj.save()
                
                return {
                    'success': True,
                    'checkout_url': checkout_data.get('redirectUrl'),
                    'checkout_id': checkout_data.get('checkoutId'),
                    'reference_number': checkout_data.get('requestReferenceNumber')
                }
            else:
                return {
                    'success': False,
                    'error': f'GCash API Error: {response.status_code}',
                    'details': response.text
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'GCash payment creation failed: {str(e)}'
            }
    
    def verify_payment(self, payment_obj):
        """
        Verify payment status from gateway
        """
        try:
            if not payment_obj.gateway_transaction_id:
                return {'success': False, 'error': 'No transaction ID found'}
            
            # Determine which gateway to use
            if payment_obj.payment_method == 'gcash':
                auth_header = self._get_gcash_auth_header()
                base_url = self.gcash_base_url
            else:  # paymaya
                auth_header = self._get_paymaya_auth_header()
                base_url = self.paymaya_base_url
            
            headers = {
                'Authorization': f'Basic {auth_header}'
            }
            
            response = requests.get(
                f"{base_url}/v1/checkouts/{payment_obj.gateway_transaction_id}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                payment_data = response.json()
                status = payment_data.get('status', '').lower()
                
                # Update payment object with latest data
                payment_obj.gateway_response = payment_data
                
                if status == 'payment_success':
                    payment_obj.mark_as_paid()
                    return {'success': True, 'status': 'completed', 'data': payment_data}
                elif status == 'payment_failed':
                    payment_obj.status = 'failed'
                    payment_obj.save()
                    return {'success': False, 'status': 'failed', 'data': payment_data}
                elif status == 'payment_cancelled':
                    payment_obj.status = 'cancelled'
                    payment_obj.save()
                    return {'success': False, 'status': 'cancelled', 'data': payment_data}
                else:
                    return {'success': True, 'status': 'pending', 'data': payment_data}
            else:
                return {'success': False, 'error': f'API Error: {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': f'Verification failed: {str(e)}'}
    
    def handle_webhook(self, webhook_data, signature=None):
        """
        Handle payment webhook notifications
        """
        try:
            # Verify webhook signature if provided
            if signature and not self._verify_webhook_signature(webhook_data, signature):
                return {'success': False, 'error': 'Invalid webhook signature'}
            
            # Extract payment information
            checkout_id = webhook_data.get('id')
            status = webhook_data.get('status', '').lower()
            reference_number = webhook_data.get('requestReferenceNumber', '')
            
            # Find payment object
            from .models import Payment
            try:
                payment = Payment.objects.get(gateway_transaction_id=checkout_id)
            except Payment.DoesNotExist:
                return {'success': False, 'error': 'Payment not found'}
            
            # Update payment status based on webhook
            payment.gateway_response = webhook_data
            
            if status == 'payment_success':
                payment.mark_as_paid()
            elif status == 'payment_failed':
                payment.status = 'failed'
                payment.save()
            elif status == 'payment_cancelled':
                payment.status = 'cancelled'
                payment.save()
            
            return {'success': True, 'payment_id': payment.id, 'status': status}
            
        except Exception as e:
            return {'success': False, 'error': f'Webhook processing failed: {str(e)}'}
    
    def _get_paymaya_auth_header(self):
        """Get PayMaya authorization header"""
        credentials = f"{self.paymaya_public_key}:"
        return base64.b64encode(credentials.encode()).decode()
    
    def _get_gcash_auth_header(self):
        """Get GCash authorization header"""
        credentials = f"{self.gcash_public_key}:"
        return base64.b64encode(credentials.encode()).decode()
    
    def _verify_webhook_signature(self, payload, signature):
        """Verify webhook signature for security"""
        # This would implement signature verification based on the gateway's requirements
        # For now, return True (implement proper verification in production)
        return True


# Utility function to get payment service instance
def get_payment_service():
    return PaymentGatewayService()
