"""
AI Resume Optimizer - Backend Server
Kimi API + Gumroad Payment Verification
"""
import os
import json
import time
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration
KIMI_API_KEY = os.environ.get('KIMI_API_KEY', 'your-kimi-api-key-here')
KIMI_API_URL = 'https://api.moonshot.cn/v1/chat/completions'
GUMROAD_API_KEY = os.environ.get('GUMROAD_API_KEY', 'your-gumroad-api-key-here')
GUMROAD_PRODUCT_ID = os.environ.get('GUMROAD_PRODUCT_ID', 'your-product-id')

# Simple in-memory store for verified orders (in production use Redis/DB)
verified_orders = {}
# Rate limiting: each order can generate up to 3 resumes
order_usage = {}

# Pre-generated license codes (loaded from file if exists)
LICENSE_CODES = set()
try:
    codes_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'license_codes.txt')
    if os.path.exists(codes_file):
        with open(codes_file, 'r') as f:
            LICENSE_CODES = {line.strip() for line in f if line.strip()}
except Exception:
    pass

# System prompt for resume optimization
RESUME_SYSTEM_PROMPT = """You are an expert HR consultant and resume writer specializing in helping Chinese professionals create English resumes that pass ATS (Applicant Tracking System) filters and impress Western hiring managers.

Your task:
1. Translate the Chinese resume to professional, native-level English
2. Optimize for ATS: use standard section headers, industry keywords, and clean formatting
3. Use action verbs and quantify achievements where possible
4. Follow Western resume conventions (no photo, no age, no marital status unless relevant)
5. Keep it concise (1-2 pages max)

Output format: Markdown with clear section headers.
Sections: Professional Summary, Experience, Education, Skills, Certifications (if any).

For each job in Experience:
- Job Title, Company, Location, Dates
- 3-5 bullet points starting with action verbs
- Quantify achievements with numbers/percentages where the original provides data

Do NOT invent information not in the original resume. Only optimize the language and format."""


def call_kimi_api(messages, model="moonshot-v1-32k", temperature=0.7):
    """Call Kimi (Moonshot) API"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {KIMI_API_KEY}'
    }
    data = {
        'model': model,
        'messages': messages,
        'temperature': temperature,
        'max_tokens': 4000
    }
    try:
        response = requests.post(KIMI_API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        raise Exception(f"Kimi API error: {str(e)}")


def verify_gumroad_order(order_id):
    """Verify a Gumroad order ID / license key"""
    # Check if already verified (cache)
    if order_id in verified_orders:
        return True, verified_orders[order_id]
    
    try:
        # Try license key verification first
        response = requests.get(
            f'https://api.gumroad.com/v2/licenses/verify',
            params={
                'product_id': GUMROAD_PRODUCT_ID,
                'license_key': order_id
            },
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('purchase', {}).get('success'):
                verified_orders[order_id] = data.get('purchase', {})
                return True, data.get('purchase', {})
        
        # Fallback: try sales API with order ID
        response = requests.get(
            f'https://api.gumroad.com/v2/sales/{order_id}',
            params={'access_token': GUMROAD_API_KEY},
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                sale = data.get('sale', {})
                if sale.get('state') in ['converted', 'settled']:
                    verified_orders[order_id] = sale
                    return True, sale
    except Exception as e:
        # If API fails, allow demo mode for known test orders
        pass
    
    # Check pre-generated license codes
    if order_id in LICENSE_CODES:
        verified_orders[order_id] = {'license_code': True}
        return True, {'license_code': True}
    
    # Demo mode: allow orders starting with "DEMO-" for testing
    if order_id.startswith('DEMO-'):
        verified_orders[order_id] = {'demo': True}
        return True, {'demo': True}
    
    return False, None


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/verify-order', methods=['POST'])
def verify_order():
    """Verify a Gumroad order / license key"""
    try:
        data = request.get_json()
        order_id = data.get('order_id', '').strip()
        
        if not order_id:
            return jsonify({'error': 'Order ID / License key is required'}), 400
        
        valid, order_data = verify_gumroad_order(order_id)
        
        if valid:
            usage = order_usage.get(order_id, 0)
            return jsonify({
                'success': True,
                'valid': True,
                'usage': usage,
                'max_usage': 3,
                'remaining': 3 - usage
            })
        else:
            return jsonify({
                'success': False,
                'valid': False,
                'error': 'Invalid order ID or license key. Please check your purchase confirmation email.'
            }), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/optimize', methods=['POST'])
def optimize_resume():
    """Optimize a Chinese resume to English (requires verified order)"""
    try:
        data = request.get_json()
        chinese_resume = data.get('resume', '').strip()
        order_id = data.get('order_id', '').strip()
        
        if not order_id:
            return jsonify({'error': 'Order ID is required. Please purchase access first.'}), 401
        
        # Verify order
        valid, order_data = verify_gumroad_order(order_id)
        if not valid:
            return jsonify({'error': 'Invalid or expired order ID'}), 401
        
        # Check usage limit
        usage = order_usage.get(order_id, 0)
        if usage >= 3:
            return jsonify({'error': 'Usage limit reached. You have used all 3 resume optimizations.'}), 429
        
        if not chinese_resume:
            return jsonify({'error': 'Resume content is required'}), 400
        
        if len(chinese_resume) < 50:
            return jsonify({'error': 'Resume content too short. Please provide more details.'}), 400
        
        # Call Kimi API
        messages = [
            {'role': 'system', 'content': RESUME_SYSTEM_PROMPT},
            {'role': 'user', 'content': f'Please optimize this Chinese resume into English:\n\n{chinese_resume}'}
        ]
        
        optimized_resume = call_kimi_api(messages)
        
        # Increment usage
        order_usage[order_id] = usage + 1
        
        return jsonify({
            'success': True,
            'resume': optimized_resume,
            'usage': order_usage[order_id],
            'remaining': 3 - order_usage[order_id]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/cover-letter', methods=['POST'])
def generate_cover_letter():
    """Generate a cover letter (requires verified order)"""
    try:
        data = request.get_json()
        resume = data.get('resume', '').strip()
        job_description = data.get('job_description', '').strip()
        order_id = data.get('order_id', '').strip()
        
        if not order_id:
            return jsonify({'error': 'Order ID is required'}), 401
        
        valid, order_data = verify_gumroad_order(order_id)
        if not valid:
            return jsonify({'error': 'Invalid order ID'}), 401
        
        if not resume:
            return jsonify({'error': 'Resume is required'}), 400
        
        prompt = f"""Based on the following resume and job description, write a professional cover letter.

Resume:
{resume}

Job Description:
{job_description if job_description else 'General software/tech industry position'}

Requirements:
- 3-4 paragraphs
- Professional but engaging tone
- Highlight 2-3 key achievements from the resume
- Show enthusiasm for the role
- Close with a call to action
- No more than 400 words
"""
        
        messages = [
            {'role': 'system', 'content': 'You are an expert career coach specializing in cover letters for Western job markets.'},
            {'role': 'user', 'content': prompt}
        ]
        
        cover_letter = call_kimi_api(messages, temperature=0.8)
        
        return jsonify({
            'success': True,
            'cover_letter': cover_letter
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'service': 'AI Resume Optimizer',
        'kimi_configured': KIMI_API_KEY != 'your-kimi-api-key-here',
        'gumroad_configured': GUMROAD_API_KEY != 'your-gumroad-api-key-here'
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
