#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AHMED Telegram Bot - Python Version
Advanced Site Analyzer & Card Checker
"""

import requests
import time
import threading
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

# التوكن
TOKEN = '7497151281:AAHQLlqAR3dMcosj3uevoK3_E6PdHnM3inw'
URL = f'https://api.telegram.org/bot{TOKEN}/'
MAX_MESSAGE_LENGTH = 4096

# Lock للعمليات الآمنة
lock = threading.Lock()
context_data = {}

# ============================================
# دوال التعامل مع Telegram API
# ============================================

def get_updates(offset=None):
    """جلب التحديثات من تيليجرام"""
    try:
        url = URL + 'getUpdates'
        params = {'timeout': 50, 'offset': offset}
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error getting updates: {e}")
        return {'result': []}

def send_message(chat_id, text, parse_mode='HTML'):
    """إرسال رسالة"""
    try:
        url = URL + 'sendMessage'
        params = {
            'chat_id': chat_id, 
            'text': text,
            'parse_mode': parse_mode
        }
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except requests.RequestException as e:
        print(f"Error sending message to {chat_id}: {e}")

def send_action(chat_id, action='typing'):
    """إرسال حالة (typing, upload_document, etc.)"""
    try:
        url = URL + 'sendChatAction'
        params = {'chat_id': chat_id, 'action': action}
        requests.get(url, params=params, timeout=5)
    except:
        pass

def edit_message(chat_id, message_id, text, parse_mode='HTML'):
    """تعديل رسالة"""
    try:
        url = URL + 'editMessageText'
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'parse_mode': parse_mode
        }
        requests.get(url, params=params, timeout=10)
    except Exception as e:
        print(f"Error editing message: {e}")

def split_message(text):
    """تقسيم الرسائل الطويلة"""
    return [text[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]

# ============================================
# دوال تحليل المواقع
# ============================================

def analyze_site(url):
    """تحليل موقع ويب"""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    result = {
        'url': url, 
        'payment_gateways': [], 
        'captcha': False, 
        'cloudflare': False, 
        'graphql': False, 
        'platform': None, 
        'http_status': None, 
        'content_type': None, 
        'cookies': {}, 
        'error': None, 
        'country': None
    }

    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        headers = response.headers
        content_type = headers.get('Content-Type', '')
        response_text = response.text
        cookies = response.cookies.get_dict()
        country = headers.get('CF-IPCountry', 'Unknown')

        http_version = 'HTTP/1.1' if response.raw.version == 11 else 'HTTP/1.0'
        status_code = response.status_code
        reason_phrase = response.reason
        http_status = f"{http_version} {status_code} {reason_phrase}"

        result.update({
            'payment_gateways': check_payment_gateways(headers, response_text, cookies),
            'cloudflare': check_cloudflare(response_text),
            'captcha': check_captcha(response_text),
            'graphql': check_graphql(response_text),
            'platform': check_platform(response_text),
            'http_status': http_status,
            'content_type': content_type,
            'cookies': cookies,
            'country': country
        })

    except requests.Timeout:
        result['error'] = '⏰ Timeout error'
    except Exception as e:
        result['error'] = f'❌ Error: {str(e)}'
    
    return result

def check_payment_gateways(headers, response_text, cookies):
    """فحص بوابات الدفع"""
    gateway_keywords = [
        'stripe', 'paypal', 'square', 'venmo', 'bitcoin', 'braintree', 'amazon-pay',
        'adyen', '2checkout', 'skrill', 'authorize.net', 'worldpay', 'payu', 'paytm',
        'afterpay', 'alipay', 'klarna', 'affirm', 'bluesnap', 'checkout.com', 'dwolla',
        'paddle', 'payoneer', 'sagepay', 'wechat pay', 'yandex.money', 'zelle',
        'shopify', 'buy now', 'add to cart', 'store', 'checkout', 'cart', 'shop now',
        'card', 'payment', 'gateway'
    ]

    combined_text = response_text.lower() + str(headers).lower() + str(cookies).lower()
    detected = [kw.capitalize() for kw in gateway_keywords if kw in combined_text]
    return list(set(detected))

def check_cloudflare(response_text):
    """فحص Cloudflare"""
    markers = ['checking your browser', 'cf-ray', 'cloudflare']
    return any(marker in response_text.lower() for marker in markers)

def check_captcha(response_text):
    """فحص CAPTCHA"""
    markers = ['recaptcha', 'g-recaptcha', 'hcaptcha']
    return any(marker in response_text.lower() for marker in markers)

def check_graphql(response_text):
    """فحص GraphQL"""
    markers = ['graphql', 'application/graphql']
    return any(marker in response_text.lower() for marker in markers)

def check_platform(response_text):
    """فحص منصة الموقع"""
    platforms = {
        'woocommerce': ['woocommerce', 'wc-cart'],
        'magento': ['magento', 'mageplaza'],
        'shopify': ['shopify', 'myshopify'],
        'prestashop': ['prestashop'],
        'opencart': ['opencart'],
        'wordpress': ['wordpress', 'wp-content'],
        'drupal': ['drupal'],
        'joomla': ['joomla']
    }

    for platform, markers in platforms.items():
        if any(marker in response_text.lower() for marker in markers):
            return platform.capitalize()
    return None

def format_analysis(results):
    """تنسيق نتائج التحليل"""
    gateways = ', '.join(results['payment_gateways']) if results['payment_gateways'] else 'None'
    
    analysis = f"""🔍 <b>SITE ANALYSIS - AHMED</b>
━━━━━━━━━━━━━━━━━━━━
<b>URL:</b> {results['url']}
<b>Status:</b> {results['http_status']}
<b>Country:</b> {results['country']}

<b>Payment Gateways:</b> {gateways}
<b>Platform:</b> {results['platform'] or 'Unknown'}

<b>Security:</b>
• Cloudflare: {'✅ Yes' if results['cloudflare'] else '❌ No'}
• CAPTCHA: {'✅ Yes' if results['captcha'] else '❌ No'}
• GraphQL: {'✅ Yes' if results['graphql'] else '❌ No'}

{'<b>Error:</b> ' + results['error'] if results['error'] else ''}
━━━━━━━━━━━━━━━━━━━━
<i>Analyzed by AHMED Bot</i>"""
    
    return analysis

# ============================================
# معالجات الأوامر
# ============================================

def handle_start(chat_id, first_name, user_id):
    """معالج أمر /start"""
    send_action(chat_id)
    text = f"""<b>👋 Welcome {first_name}!</b>

🤖 <b>AHMED Bot - Advanced Tools</b>

<b>Available Commands:</b>
/url - Analyze website
/bin - Check BIN info
/gen - Generate cards
/cmds - Show all commands
/help - Get help

<b>Your ID:</b> <code>{user_id}</code>
<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<i>Made with ❤️ by AHMED 🇮🇶</i>"""
    
    send_message(chat_id, text)

def handle_url(chat_id, message_id, text):
    """معالج أمر /url"""
    send_action(chat_id)
    
    if text.startswith('/url '):
        url = text.split(' ', 1)[1].strip()
        msg = send_message(chat_id, "⏳ <b>Analyzing...</b>")
        msg_id = msg['result']['message_id']
        
        result = analyze_site(url)
        analysis = format_analysis(result)
        edit_message(chat_id, msg_id, analysis)
    else:
        send_message(chat_id, "❌ <b>Usage:</b> <code>/url https://example.com</code>")

def handle_bin(chat_id, message_id, text):
    """معالج أمر /bin"""
    send_action(chat_id)
    
    if len(text) <= 5:
        send_message(chat_id, "❌ <b>Usage:</b> <code>/bin 123456</code>")
        return
    
    bin_number = text[5:].strip()[:6]
    
    if not bin_number.isdigit() or len(bin_number) < 6:
        send_message(chat_id, "❌ <b>Invalid BIN</b>")
        return
    
    msg = send_message(chat_id, "⏳ <b>Checking BIN...</b>")
    msg_id = msg['result']['message_id']
    
    # استدعاء API فحص BIN
    try:
        response = requests.post(
            'http://bins.su/',
            data={'action': 'searchbins', 'bins': bin_number, 'bank': '', 'country': ''},
            timeout=10
        )
        
        if 'No bins found!' in response.text:
            edit_message(chat_id, msg_id, "❌ <b>BIN Not Found</b>")
        else:
            # استخراج البيانات من الاستجابة
            result = f"""<b>✅ BIN INFO - AHMED</b>
━━━━━━━━━━━━━━━━━━━━
<b>BIN:</b> <code>{bin_number}</code>
<b>Status:</b> Valid

<i>Full details available</i>
━━━━━━━━━━━━━━━━━━━━"""
            edit_message(chat_id, msg_id, result)
    except Exception as e:
        edit_message(chat_id, msg_id, f"❌ <b>Error:</b> {str(e)}")

def handle_gen(chat_id, message_id, text, username):
    """معالج أمر /gen"""
    send_action(chat_id)
    
    if len(text) <= 5:
        send_message(chat_id, "❌ <b>Usage:</b> <code>/gen 123456|xx|25|xxx|10</code>")
        return
    
    params = text[5:].strip().replace('|', ' ').split()
    
    if len(params) < 1:
        send_message(chat_id, "❌ <b>Invalid format</b>")
        return
    
    msg = send_message(chat_id, "⏳ <b>Generating cards...</b>")
    msg_id = msg['result']['message_id']
    
    import random
    
    bin_code = params[0] if len(params) > 0 else '123456'
    month = params[1] if len(params) > 1 else 'xx'
    year = params[2] if len(params) > 2 else 'xx'
    cvv = params[3] if len(params) > 3 else 'xxx'
    amount = int(params[4]) if len(params) > 4 else 10
    
    if amount > 20:
        amount = 20
    
    cards = []
    for _ in range(amount):
        # توليد رقم بطاقة عشوائي
        card_num = bin_code + ''.join([str(random.randint(0, 9)) for _ in range(16 - len(bin_code))])
        
        # توليد الشهر
        if month == 'xx' or month == 'x':
            gen_month = f"{random.randint(1, 12):02d}"
        else:
            gen_month = month if len(month) == 2 else f"0{month}"
        
        # توليد السنة
        if year == 'xx' or year == 'x':
            gen_year = random.randint(25, 30)
        else:
            gen_year = year
        
        # توليد CVV
        if cvv == 'xxx' or cvv == 'xx' or cvv == 'x':
            gen_cvv = random.randint(100, 999)
        else:
            gen_cvv = cvv
        
        cards.append(f"{card_num}|{gen_month}|{gen_year}|{gen_cvv}")
    
    result = f"""<b>💳 CARD GENERATOR - AHMED</b>
━━━━━━━━━━━━━━━━━━━━
<b>Format:</b> <code>{bin_code}|{month}|{year}|{cvv}</code>
<b>Amount:</b> {amount}

<code>{chr(10).join(cards)}</code>

<b>Generated by:</b> @{username}
<i>Bot by AHMED</i>"""
    
    edit_message(chat_id, msg_id, result)

def handle_cmds(chat_id):
    """معالج أمر /cmds"""
    commands = """<b>📋 AVAILABLE COMMANDS - AHMED</b>
━━━━━━━━━━━━━━━━━━━━

<b>🔍 Analysis Tools:</b>
/url <code>link</code> - Analyze website
/bin <code>123456</code> - Check BIN info

<b>💳 Card Tools:</b>
/gen <code>bin|mm|yy|cvv|amount</code> - Generate cards

<b>ℹ️ Information:</b>
/start - Start bot
/cmds - Show commands
/help - Get help

<b>📝 Examples:</b>
• <code>/url https://example.com</code>
• <code>/bin 123456</code>
• <code>/gen 123456|xx|25|xxx|10</code>

<i>Made by AHMED 🇮🇶</i>"""
    
    send_message(chat_id, commands)

def handle_file(chat_id, file_content):
    """معالج الملفات"""
    encodings = ['utf-8', 'latin-1', 'windows-1252']
    urls = []
    
    for encoding in encodings:
        try:
            urls = file_content.decode(encoding).splitlines()
            break
        except UnicodeDecodeError:
            continue
    
    if not urls:
        send_message(chat_id, "❌ <b>Error: Unable to decode file</b>")
        return
    
    with lock:
        context_data[chat_id] = {'url_list': [url.strip() for url in urls if url.strip()]}
    
    send_message(chat_id, f"✅ <b>{len(context_data[chat_id]['url_list'])} URLs uploaded</b>\n\nUse /url to analyze")

# ============================================
# الحلقة الرئيسية
# ============================================

def main():
    """الحلقة الرئيسية للبوت"""
    offset = None
    print("🤖 AHMED Bot started successfully! 🇮🇶")
    
    while True:
        try:
            updates = get_updates(offset)
            
            if 'result' in updates:
                for update in updates['result']:
                    offset = update['update_id'] + 1
                    
                    if 'message' in update:
                        chat_id = update['message']['chat']['id']
                        text = update['message'].get('text', '')
                        document = update['message'].get('document')
                        first_name = update['message']['from'].get('first_name', 'User')
                        username = update['message']['from'].get('username', 'unknown')
                        user_id = update['message']['from']['id']
                        message_id = update['message']['message_id']

                        if text:
                            if text.startswith('/start'):
                                handle_start(chat_id, first_name, user_id)
                            elif text.startswith('/url'):
                                threading.Thread(target=handle_url, args=(chat_id, message_id, text)).start()
                            elif text.startswith('/bin'):
                                threading.Thread(target=handle_bin, args=(chat_id, message_id, text)).start()
                            elif text.startswith('/gen'):
                                threading.Thread(target=handle_gen, args=(chat_id, message_id, text, username)).start()
                            elif text.startswith('/cmds') or text.startswith('/help'):
                                handle_cmds(chat_id)
                        
                        elif document:
                            file_id = document['file_id']
                            file_info = requests.get(URL + 'getFile', params={'file_id': file_id}).json()
                            
                            if 'result' in file_info:
                                file_path = file_info['result']['file_path']
                                file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
                                file_content = requests.get(file_url).content
                                threading.Thread(target=handle_file, args=(chat_id, file_content)).start()
            
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()