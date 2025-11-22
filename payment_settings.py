# Payment Gateway Settings for Golden Mais
# Add these settings to your Django settings.py file

# PayMaya Configuration
# Get these credentials from PayMaya Developer Portal: https://developers.paymaya.com/
PAYMAYA_PUBLIC_KEY = 'pk-Z0OSzLvIcOI2UIvDhdTGVVfRSSeiGStnceqwUE7n0Ah'  # Replace with your actual public key
PAYMAYA_SECRET_KEY = 'sk-X8qolYjy62kIzEki9URu7QXkJIhgHGVVfRSSeiGStnceqwUE7n0Ah'  # Replace with your actual secret key
PAYMAYA_BASE_URL = 'https://pg-sandbox.paymaya.com'  # Use 'https://pg.paymaya.com' for production

# GCash Configuration (via PayMaya)
# GCash uses the same PayMaya infrastructure but with different credentials
GCASH_PUBLIC_KEY = 'pk-MOfNKu3FmHMVMeRzgbOvFBfJufTlpWhcRbxp'  # Replace with your actual GCash public key
GCASH_SECRET_KEY = 'sk-uh4ZhLdH2Q8rKVfRSSeiGStnceqwUE7n0Ah'  # Replace with your actual GCash secret key
GCASH_BASE_URL = 'https://pg-sandbox.paymaya.com'  # Use 'https://pg.paymaya.com' for production

# Security Settings
PAYMENT_WEBHOOK_SECRET = 'your-webhook-secret-key-here'  # Used to verify webhook signatures

# Additional Payment Settings
PAYMENT_TIMEOUT = 30  # Timeout in seconds for payment API calls
PAYMENT_RETRY_ATTEMPTS = 3  # Number of retry attempts for failed API calls

# Currency Settings
DEFAULT_CURRENCY = 'PHP'
CURRENCY_SYMBOL = '₱'

# Order Settings
ORDER_EXPIRY_MINUTES = 30  # Orders expire after 30 minutes if not paid

"""
IMPORTANT SETUP INSTRUCTIONS:

1. SANDBOX TESTING:
   - The above keys are sandbox/test keys for development
   - Use these for testing without real money transactions
   - Test cards: https://developers.paymaya.com/blog/entry/checkout-api-test-cards-and-test-accounts

2. PRODUCTION SETUP:
   - Replace sandbox keys with production keys from PayMaya/GCash
   - Change base URLs to production endpoints
   - Set up proper webhook endpoints
   - Enable SSL/HTTPS for security

3. WEBHOOK SETUP:
   - Configure webhook URL in PayMaya dashboard: https://yourdomain.com/payment-webhook/
   - Webhook events to subscribe to:
     - CHECKOUT_SUCCESS
     - CHECKOUT_FAILURE
     - CHECKOUT_CANCELLED

4. SECURITY CONSIDERATIONS:
   - Store secret keys in environment variables, not in code
   - Use Django's SECRET_KEY for additional security
   - Implement proper logging for payment transactions
   - Set up monitoring for failed payments

5. TESTING PROCESS:
   - Test with sandbox credentials first
   - Use test card numbers provided by PayMaya
   - Verify webhook handling works correctly
   - Test all payment scenarios (success, failure, cancellation)

6. ENVIRONMENT VARIABLES SETUP:
   Add to your .env file or environment:
   
   PAYMAYA_PUBLIC_KEY=your_actual_public_key
   PAYMAYA_SECRET_KEY=your_actual_secret_key
   GCASH_PUBLIC_KEY=your_actual_gcash_public_key
   GCASH_SECRET_KEY=your_actual_gcash_secret_key
   PAYMENT_WEBHOOK_SECRET=your_webhook_secret

7. DJANGO SETTINGS.PY:
   import os
   from django.core.exceptions import ImproperlyConfigured
   
   def get_env_variable(var_name):
       try:
           return os.environ[var_name]
       except KeyError:
           error_msg = f"Set the {var_name} environment variable"
           raise ImproperlyConfigured(error_msg)
   
   # Payment Gateway Settings
   PAYMAYA_PUBLIC_KEY = get_env_variable('PAYMAYA_PUBLIC_KEY')
   PAYMAYA_SECRET_KEY = get_env_variable('PAYMAYA_SECRET_KEY')
   # ... etc for other keys

8. REQUIRED PACKAGES:
   pip install requests
   pip install python-decouple  # For environment variable management
"""
