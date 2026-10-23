import os
import json
import requests
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'nexus_secure_secret_key_2026')

# Vercel Read-Only File System Fix for SQLite
if os.environ.get('VERCEL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/nexus_courses.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///nexus_courses.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False, default=199)
    videos_count = db.Column(db.Integer, nullable=False, default=25)
    validity = db.Column(db.String(100), nullable=False, default="Lifetime Access")
    image_url = db.Column(db.String(500), nullable=False)
    demo_video_urls = db.Column(db.Text, nullable=True)
    telegram_url = db.Column(db.String(500), default="https://t.me/NexusSupportBot")
    demo_instructions = db.Column(db.Text, default="1. Neeche scroll karke saare demo videos dekhein\n2. Stream smoothly without any lag\n3. Click Buy Now to join full course")
    enabled = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=0)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), unique=True, nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    utr = db.Column(db.String(50), nullable=False)
    screenshot = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_visits = db.Column(db.Integer, default=0)

# --- INITIALIZE DATABASE & DEFAULT DATA ---
with app.app_context():
    db.create_all()
    
    if not Admin.query.filter_by(username='arushdev').first():
        hashed_pw = generate_password_hash('arush300')
        admin = Admin(username='arushdev', password_hash=hashed_pw)
        db.session.add(admin)
    
    default_settings = {
        'site_name': 'NEXUS COURSES',
        'site_caption': 'Master High-Income Skills with Premium Curated Masterclasses',
        'site_logo': 'https://i.ibb.co/5X0hc5dd/logo.png',
        'upi_id': 'nexuspayments@oksbi',
        'upi_name': 'Nexus Digital Store',
        'telegram_support': 'https://t.me/NexusSupportBot',
        'telegram_bot_token': '',
        'telegram_chat_id': '',
        'payment_instructions': '1. Scan QR or pay directly to the UPI ID\n2. Copy the 12-digit UTR/Ref Number\n3. Upload payment screenshot and UTR below for instant verification'
    }
    for k, v in default_settings.items():
        if not Setting.query.filter_by(key=k).first():
            db.session.add(Setting(key=k, value=v))
            
    if Plan.query.count() == 0:
        initial_plans = [
            ("Python Mastery & Backend Pro", "Build robust backend applications, APIs, and automated systems with Python.", 199, 30, "Lifetime Access", "https://i.ibb.co/Fb6S1mYg/course1.jpg", "https://www.w3schools.com/html/mov_bbb.mp4,https://www.w3schools.com/html/mov_bbb.mp4"),
            ("Full Stack Web Development Bootcamp", "Master HTML, CSS, JavaScript, React, and Node.js from scratch.", 299, 45, "Lifetime Access", "https://i.ibb.co/ZRqKVvRQ/course2.jpg", "https://www.w3schools.com/html/mov_bbb.mp4"),
            ("Advanced React & Next.js Masterclass", "Build lightning-fast, SEO-optimized web applications with modern React.", 249, 28, "Lifetime Access", "https://i.ibb.co/21H7BGM2/course3.jpg", ""),
            ("Data Science & Machine Learning Pro", "Analyze complex datasets and build predictive AI models using Python.", 399, 50, "Lifetime Access", "https://i.ibb.co/QF2v05qK/course4.jpg", ""),
            ("Cybersecurity & Ethical Hacking 2026", "Learn penetration testing, network security, and vulnerability assessment.", 349, 35, "Lifetime Access", "https://i.ibb.co/5X0hc5dd/course5.jpg", ""),
            ("UI/UX Design Master Course", "Design stunning user interfaces and seamless experiences in Figma.", 199, 22, "Lifetime Access", "https://i.ibb.co/HLw36KQ4/course6.jpg", ""),
            ("Android & iOS App Development", "Create cross-platform mobile applications using Flutter and React Native.", 299, 40, "Lifetime Access", "https://i.ibb.co/9kKCd6ZF/course7.jpg", ""),
            ("Cloud Computing & AWS DevOps", "Master cloud infrastructure, Docker, Kubernetes, and CI/CD pipelines.", 449, 38, "Lifetime Access", "https://i.ibb.co/C5KZBm7f/course8.jpg", ""),
            ("AI & Generative Prompt Engineering", "Leverage LLMs, AI agents, and prompt frameworks to supercharge productivity.", 199, 20, "Lifetime Access", "https://i.ibb.co/qFhKnzcH/course9.jpg", ""),
            ("Digital Marketing & Growth Hacking", "Scale brands, run high-converting ad campaigns, and master SEO.", 199, 25, "Lifetime Access", "https://i.ibb.co/84598K8j/course10.jpg", "")
        ]
        for idx, (title, desc, price, vids, val, img, demo_vids) in enumerate(initial_plans):
            p = Plan(title=title, description=desc, price=price, videos_count=vids, validity=val, image_url=img, demo_video_urls=demo_vids, order_index=idx)
            db.session.add(p)
            
    if not Analytics.query.first():
        db.session.add(Analytics(total_visits=1))
    db.session.commit()

def get_settings():
    return {s.key: s.value for s in Setting.query.all()}

def send_telegram_notification(order_info):
    settings = get_settings()
    token = settings.get('telegram_bot_token', '').strip()
    chat_id = settings.get('telegram_chat_id', '').strip()
    
    if token and chat_id:
        message = (
            f"🚨 *New Payment Submission!* 🚨\n\n"
            f"🆔 *Order ID:* `{order_info['order_id']}`\n"
            f"📚 *Course:* {order_info['course_name']}\n"
            f"💰 *Amount:* ₹{order_info['amount']}\n"
            f"🔢 *UTR Number:* `{order_info['utr']}`\n"
            f"⏳ *Status:* Pending Verification"
        )
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=5)
        except Exception as e:
            print("Telegram notification error:", e)

# --- ROUTES ---
@app.route('/')
def index():
    analytics = Analytics.query.first()
    if analytics:
        analytics.total_visits += 1
        db.session.commit()
    settings = get_settings()
    plans = Plan.query.filter_by(enabled=True).order_by(Plan.order_index.asc()).all()
    return render_template_string(INDEX_HTML, settings=settings, plans=plans)

@app.route('/demo/<int:plan_id>')
def demo_page(plan_id):
    settings = get_settings()
    plan = Plan.query.get_or_404(plan_id)
    demo_list = [url.strip() for url in plan.demo_video_urls.split(',')] if plan.demo_video_urls else []
    return render_template_string(DEMO_HTML, settings=settings, plan=plan, demo_list=demo_list)

@app.route('/payment/<int:plan_id>', methods=['GET', 'POST'])
def payment_page(plan_id):
    settings = get_settings()
    plan = Plan.query.get_or_404(plan_id)
    if request.method == 'POST':
        utr = request.form.get('utr', '').strip()
        if not utr or len(utr) < 8:
            flash('Please enter a valid UTR / Transaction Reference Number.', 'error')
            return redirect(url_for('payment_page', plan_id=plan_id))
        
        order_id = 'NEXUS-' + datetime.utcnow().strftime('%Y%m%d%H%M%S') + '-' + str(plan.id)
        
        screenshot_filename = None
        if 'screenshot' in request.files:
            file = request.files['screenshot']
            if file and file.filename != '':
                upload_folder = os.path.join('/tmp', 'uploads') if os.environ.get('VERCEL') else os.path.join('static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                filename = f"{order_id}_{file.filename}"
                file.save(os.path.join(upload_folder, filename))
                screenshot_filename = filename

        new_order = Order(
            order_id=order_id,
            plan_id=plan.id,
            course_name=plan.title,
            amount=plan.price,
            utr=utr,
            screenshot=screenshot_filename,
            status='Pending'
        )
        db.session.add(new_order)
        db.session.commit()
        
        send_telegram_notification({'order_id': order_id, 'course_name': plan.title, 'amount': plan.price, 'utr': utr})
        
        return redirect(url_for('payment_success', order_id=order_id))
    return render_template_string(PAYMENT_HTML, settings=settings, plan=plan)

@app.route('/success/<order_id>')
def payment_success(order_id):
    settings = get_settings()
    order = Order.query.filter_by(order_id=order_id).first_or_404()
    return render_template_string(SUCCESS_HTML, settings=settings, order=order)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    settings = get_settings()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_logged'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password!', 'error')
    return render_template_string(ADMIN_LOGIN_HTML, settings=settings)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    settings = get_settings()
    plans = Plan.query.order_by(Plan.order_index.asc()).all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    analytics = Analytics.query.first()
    stats = {
        'visits': analytics.total_visits if analytics else 0,
        'pending': sum(1 for o in orders if o.status == 'Pending'),
        'approved': sum(1 for o in orders if o.status == 'Approved'),
        'revenue': sum(o.amount for o in orders if o.status == 'Approved')
    }
    return render_template_string(ADMIN_DASHBOARD_HTML, settings=settings, plans=plans, orders=orders, stats=stats)

@app.route('/admin/plan/save', methods=['POST'])
def admin_save_plan():
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    plan_id = request.form.get('plan_id')
    title = request.form.get('title')
    description = request.form.get('description')
    price = int(request.form.get('price', 199))
    videos_count = int(request.form.get('videos_count', 25))
    validity = request.form.get('validity', 'Lifetime Access')
    image_url = request.form.get('image_url')
    demo_video_urls = request.form.get('demo_video_urls', '')
    demo_instructions = request.form.get('demo_instructions')
    enabled = True if request.form.get('enabled') == 'on' else False
    
    if plan_id:
        plan = Plan.query.get_or_404(plan_id)
        plan.title = title
        plan.description = description
        plan.price = price
        plan.videos_count = videos_count
        plan.validity = validity
        plan.image_url = image_url
        plan.demo_video_urls = demo_video_urls
        plan.demo_instructions = demo_instructions
        plan.enabled = enabled
    else:
        max_order = db.session.query(db.func.max(Plan.order_index)).scalar() or 0
        new_plan = Plan(
            title=title, description=description, price=price, videos_count=videos_count, validity=validity,
            image_url=image_url, demo_video_urls=demo_video_urls, demo_instructions=demo_instructions,
            enabled=enabled, order_index=max_order + 1
        )
        db.session.add(new_plan)
    db.session.commit()
    flash('Course plan saved successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/plan/delete/<int:plan_id>')
def admin_delete_plan(plan_id):
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    plan = Plan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    flash('Course plan deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/settings/update', methods=['POST'])
def admin_update_settings():
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    for key in ['site_name', 'site_caption', 'site_logo', 'upi_id', 'upi_name', 'telegram_support', 'telegram_bot_token', 'telegram_chat_id', 'payment_instructions']:
        val = request.form.get(key)
        if val is not None:
            setting = Setting.query.filter_by(key=key).first()
            if setting:
                setting.value = val
            else:
                db.session.add(Setting(key=key, value=val))
    db.session.commit()
    flash('Settings updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/order/status/<int:order_id>/<status>')
def admin_order_status(order_id, status):
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    order = Order.query.get_or_404(order_id)
    if status in ['Pending', 'Approved', 'Rejected']:
        order.status = status
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reset-stats')
def admin_reset_stats():
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    Order.query.delete()
    analytics = Analytics.query.first()
    if analytics:
        analytics.total_visits = 0
    db.session.commit()
    flash('All orders and statistics have been reset successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# --- HTML TEMPLATES ---
BASE_HEAD = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ settings.site_name }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #0a0118; color: #f3f4f6; font-family: system-ui, sans-serif; }
        .glass { background: rgba(19, 5, 40, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(147, 51, 234, 0.2); }
        .glow-effect { box-shadow: 0 0 25px rgba(147, 51, 234, 0.25); }
        .glow-blue { box-shadow: 0 0 25px rgba(59, 130, 246, 0.25); }
    </style>
</head>
<body class="min-h-screen flex flex-col">
    <header class="glass sticky top-0 z-50 border-b border-purple-900/40">
        <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
            <a href="/" class="flex items-center gap-3">
                <span class="text-xl font-extrabold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">{{ settings.site_name }}</span>
            </a>
            <a href="/admin/login" class="px-4 py-2 text-sm font-bold rounded-xl bg-purple-600 hover:bg-purple-500 text-white shadow-lg glow-effect transition">
                <i class="fa-solid fa-lock mr-1.5"></i> Admin Panel
            </a>
        </div>
    </header>
    <main class="flex-grow">{% block content %}{% endblock %}</main>
    <a href="{{ settings.telegram_support }}" target="_blank" class="fixed bottom-6 right-6 z-50 bg-blue-600 hover:bg-blue-500 text-white w-14 h-14 rounded-full flex items-center justify-center text-2xl shadow-2xl glow-blue transition transform hover:scale-110">
        <i class="fa-brands fa-telegram"></i>
    </a>
    <footer class="glass border-t border-purple-900/40 py-8 mt-16 text-center text-sm text-purple-300/60">
        <p>&copy; 2026 {{ settings.site_name }}. All rights reserved.</p>
    </footer>
</body>
</html>
"""

INDEX_HTML = BASE_HEAD.replace('{% block content %}{% endblock %}', """
<section class="py-16 px-4 text-center">
    <div class="max-w-4xl mx-auto">
        <span class="px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider bg-purple-900/60 text-purple-300 border border-purple-500/30">🚀 Premium Learning Platform</span>
        <h1 class="text-4xl md:text-6xl font-black mt-6 tracking-tight bg-gradient-to-r from-white via-purple-200 to-blue-300 bg-clip-text text-transparent">{{ settings.site_name }}</h1>
        <p class="mt-4 text-lg md:text-xl text-purple-200/70 max-w-2xl mx-auto">{{ settings.site_caption }}</p>
    </div>
</section>
<section class="max-w-7xl mx-auto px-4 pb-20">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {% for plan in plans %}
        <div class="glass rounded-2xl overflow-hidden border border-purple-900/50 hover:border-purple-500/50 transition duration-300 flex flex-col group">
            <!-- Non-cropped image frame -->
            <div class="relative w-full h-60 bg-black/80 flex items-center justify-center p-3">
                <img src="{{ plan.image_url }}" alt="{{ plan.title }}" class="w-full h-full object-contain group-hover:scale-105 transition duration-500" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600'">
                <div class="absolute top-3 right-3 bg-purple-900/90 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold text-purple-200 border border-purple-500/30">
                    <i class="fa-solid fa-video mr-1"></i> {{ plan.videos_count }} Videos
                </div>
            </div>
            <div class="p-6 flex flex-col flex-grow">
                <h3 class="text-xl font-bold text-white group-hover:text-purple-300 transition">{{ plan.title }}</h3>
                <p class="mt-2 text-sm text-purple-200/70 flex-grow line-clamp-2">{{ plan.description }}</p>
                <div class="mt-4 mb-4 flex items-center justify-between">
                    <span class="text-xs text-purple-300/60 block">Price</span>
                    <span class="text-2xl font-black text-white">₹{{ plan.price }}</span>
                </div>
                <!-- Stacked Buttons: View Demo Top (Red), Buy Now Bottom (Gradient) -->
                <div class="flex flex-col gap-2.5">
                    <a href="/demo/{{ plan.id }}" class="w-full py-3 rounded-xl bg-red-600 hover:bg-red-500 text-white text-center text-sm font-bold shadow-lg transition flex items-center justify-center gap-2">
                        <i class="fa-solid fa-play-circle"></i> View Demo
                    </a>
                    <a href="/payment/{{ plan.id }}" class="w-full py-3 rounded-xl bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white text-center text-sm font-bold shadow-lg glow-effect transition">
                        Buy Now (₹{{ plan.price }})
                    </a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</section>
""")

DEMO_HTML = BASE_HEAD.replace('{% block content %}{% endblock %}', """
<div class="max-w-4xl mx-auto px-4 py-12">
    <a href="/" class="inline-flex items-center gap-2 text-sm font-semibold text-purple-400 hover:text-purple-300 mb-6">
        <i class="fa-solid fa-arrow-left"></i> Back to Courses
    </a>
    <div class="glass rounded-3xl p-6 md:p-10 border border-purple-900/50 glow-effect flex flex-col gap-8">
        
        <!-- Main Thumbnail Frame (Un-cropped) -->
        <div class="w-full rounded-2xl overflow-hidden border border-purple-500/30 h-96 bg-black/80 flex items-center justify-center p-4">
            <img src="{{ plan.image_url }}" alt="{{ plan.title }}" class="w-full h-full object-contain drop-shadow-2xl" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800'">
        </div>

        <!-- Plan Details Structured Heading Section -->
        <div class="glass p-6 rounded-2xl border border-purple-500/30 space-y-3">
            <h1 class="text-3xl font-black text-white">{{ plan.title }}</h1>
            <p class="text-purple-200/80 text-sm leading-relaxed">{{ plan.description }}</p>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-3 border-t border-purple-900/50 text-sm">
                <div class="flex flex-col"><span class="text-purple-400 text-xs font-bold uppercase">Plan</span><span class="text-white font-bold">{{ plan.title }}</span></div>
                <div class="flex flex-col"><span class="text-purple-400 text-xs font-bold uppercase">Videos</span><span class="text-white font-bold">{{ plan.videos_count }} Lessons</span></div>
                <div class="flex flex-col"><span class="text-purple-400 text-xs font-bold uppercase">Validity</span><span class="text-emerald-400 font-bold">{{ plan.validity }}</span></div>
            </div>
        </div>

        <!-- Dynamic Demo Videos Stacked Vertically -->
        {% if demo_list %}
        <div class="pt-6 border-t border-purple-900/40 flex flex-col gap-8">
            <h3 class="text-xl font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-play-circle text-red-500"></i> Course Demo Videos
            </h3>
            {% for v_url in demo_list %}
            {% if v_url %}
            <div class="flex flex-col gap-2">
                <span class="text-sm font-bold text-purple-300 uppercase tracking-wider">Demo {{ loop.index }}</span>
                <div class="w-full rounded-2xl overflow-hidden border border-purple-500/30 bg-black flex items-center justify-center shadow-2xl">
                    <video controls preload="metadata" class="w-full max-h-[500px] object-contain focus:outline-none">
                        <source src="{{ v_url }}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </div>
            </div>
            {% endif %}
            {% endfor %}
        </div>
        {% endif %}

        <div class="p-6 rounded-2xl bg-purple-950/40 border border-purple-500/20">
            <h4 class="font-bold text-purple-300 mb-3"><i class="fa-solid fa-circle-question mr-2"></i> Instructions</h4>
            <div class="text-sm text-purple-200/80 whitespace-pre-line leading-relaxed">{{ plan.demo_instructions }}</div>
        </div>

        <!-- Vertically Stacked Action Buttons -->
        <div class="pt-6 border-t border-purple-900/40 flex flex-col gap-4">
            <a href="{{ plan.telegram_url }}" target="_blank" class="w-full py-4 rounded-2xl bg-red-600 hover:bg-red-500 text-white text-center font-bold text-lg shadow-xl transition flex items-center justify-center gap-2">
                <i class="fa-solid fa-headset"></i> Contact Support / Telegram Demo
            </a>
            <a href="/payment/{{ plan.id }}" class="w-full py-4 rounded-2xl bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white text-center font-black text-lg shadow-xl glow-effect transition">
                BUY NOW — UNLOCK PREMIUM ACCESS (₹{{ plan.price }})
            </a>
        </div>
    </div>
</div>
""")

PAYMENT_HTML = BASE_HEAD.replace('{% block content %}{% endblock %}', """
<div class="max-w-2xl mx-auto px-4 py-12">
    <a href="/demo/{{ plan.id }}" class="inline-flex items-center gap-2 text-sm font-semibold text-purple-400 hover:text-purple-300 mb-6">
        <i class="fa-solid fa-arrow-left"></i> Back to Course
    </a>
    <div class="glass rounded-3xl p-6 md:p-8 border border-purple-900/50 glow-effect relative">
        <div class="text-center pb-6 border-b border-purple-900/40">
            <span class="px-3 py-1 rounded-full text-xs font-bold uppercase bg-emerald-950 text-emerald-300 border border-emerald-500/30">
                <i class="fa-solid fa-shield-halved mr-1"></i> SECURE UPI PAYMENT
            </span>
            <h1 class="text-2xl font-black text-white mt-3">{{ plan.title }}</h1>
            <p class="text-purple-300/70 text-sm mt-1">Amount Payable: <strong class="text-white text-lg">₹{{ plan.price }}</strong></p>
        </div>
        <div class="my-8 text-center bg-purple-950/60 p-6 rounded-2xl border border-purple-500/30">
            <p class="text-xs font-semibold text-purple-300 mb-4">Scan QR with any UPI App (GPay, PhonePe, Paytm)</p>
            <div class="inline-block bg-white p-3 rounded-2xl shadow-xl">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa={{ settings.upi_id }}&pn={{ settings.upi_name }}&am={{ plan.price }}&cu=INR" alt="UPI QR Code" class="w-48 h-48 mx-auto rounded-xl">
            </div>
            <div class="mt-4 flex items-center justify-center gap-2">
                <span class="text-sm font-mono text-purple-200 bg-purple-900/60 px-4 py-2 rounded-xl border border-purple-500/30">{{ settings.upi_id }}</span>
                <button onclick="navigator.clipboard.writeText('{{ settings.upi_id }}'); alert('UPI ID Copied!');" class="px-3 py-2 bg-purple-800 hover:bg-purple-700 text-white rounded-xl text-sm transition">
                    <i class="fa-solid fa-copy"></i>
                </button>
            </div>
        </div>
        <div class="mb-8 p-4 rounded-xl bg-purple-950/40 border border-purple-500/20 text-xs text-purple-300/80 leading-relaxed whitespace-pre-line">
            {{ settings.payment_instructions }}
        </div>
        
        <form id="payment-form" action="/payment/{{ plan.id }}" method="POST" enctype="multipart/form-data" class="space-y-6" onsubmit="showLoadingPopup()">
            <div>
                <label class="block text-sm font-bold text-purple-200 mb-2">Enter Your 12-Digit UTR / Transaction Reference Number *</label>
                <input type="text" name="utr" required placeholder="e.g. 432156789012" class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white focus:outline-none focus:border-purple-500 transition font-mono">
            </div>
            <div>
                <label class="block text-sm font-bold text-purple-200 mb-2">Upload Payment Screenshot (JPG, PNG, WebP) *</label>
                <input type="file" name="screenshot" accept="image/*" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-sm text-purple-300 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-purple-800 file:text-white hover:file:bg-purple-700 transition">
            </div>
            <button type="submit" class="w-full py-4 rounded-2xl bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white font-black text-lg shadow-xl glow-effect transition">
                SUBMIT PAYMENT DETAILS
            </button>
        </form>
    </div>
</div>

<!-- Glassmorphism Payment Submitting Popup -->
<div id="payment-loading-popup" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
    <div class="glass max-w-sm w-full rounded-3xl p-8 border border-purple-500/30 text-center flex flex-col items-center gap-4 glow-effect">
        <div class="w-16 h-16 border-4 border-purple-900 border-t-emerald-400 rounded-full animate-spin"></div>
        <h3 class="text-xl font-bold text-white">Payment Submitting...</h3>
        <p class="text-xs text-purple-300/80">Please wait while we verify and record your payment details.</p>
    </div>
</div>

<script>
function showLoadingPopup() {
    document.getElementById('payment-loading-popup').classList.remove('hidden');
}
</script>
""")

SUCCESS_HTML = BASE_HEAD.replace('{% block content %}{% endblock %}', """
<div class="max-w-xl mx-auto px-4 py-16 text-center">
    <div class="glass rounded-3xl p-8 border border-purple-900/50 glow-effect">
        <!-- Big Green Tick Badge -->
        <div class="w-20 h-20 bg-emerald-500/20 border-2 border-emerald-500 rounded-full flex items-center justify-center mx-auto text-emerald-400 text-4xl mb-6 shadow-xl">
            <i class="fa-solid fa-check"></i>
        </div>
        <h1 class="text-2xl font-black text-white">Payment Submitted!</h1>
        <p class="text-purple-300/80 text-sm mt-2">Your payment details and screenshot have been recorded successfully.</p>
        
        <!-- Plan & Order Details -->
        <div class="my-6 p-5 rounded-2xl bg-purple-950/60 border border-purple-500/30 text-left space-y-3 text-sm">
            <div class="flex justify-between border-b border-purple-900/40 pb-2"><span class="text-purple-400 font-semibold">Order ID:</span> <span class="font-mono text-white font-bold">{{ order.order_id }}</span></div>
            <div class="flex justify-between border-b border-purple-900/40 pb-2"><span class="text-purple-400 font-semibold">Course / Plan:</span> <span class="text-white font-bold">{{ order.course_name }}</span></div>
            <div class="flex justify-between border-b border-purple-900/40 pb-2"><span class="text-purple-400 font-semibold">Amount Paid:</span> <span class="text-white font-bold">₹{{ order.amount }}</span></div>
            <div class="flex justify-between border-b border-purple-900/40 pb-2"><span class="text-purple-400 font-semibold">UTR Number:</span> <span class="font-mono text-white">{{ order.utr }}</span></div>
            <div class="flex justify-between"><span class="text-purple-400 font-semibold">Status:</span> <span class="px-3 py-1 rounded-full text-xs font-bold bg-amber-950 text-amber-300 border border-amber-500/30">{{ order.status }}</span></div>
        </div>
        
        <a href="/" class="inline-block px-8 py-3.5 rounded-xl bg-purple-900 hover:bg-purple-800 text-white font-bold text-sm border border-purple-500/30 transition">
            Return to Homepage
        </a>
    </div>
</div>
""")

ADMIN_LOGIN_HTML = BASE_HEAD.replace('{% block content %}{% endblock %}', """
<div class="max-w-md mx-auto px-4 py-20">
    <div class="glass rounded-3xl p-8 border border-purple-900/50 glow-effect">
        <div class="text-center mb-8">
            <div class="w-16 h-16 bg-purple-900/50 border border-purple-500/30 rounded-2xl flex items-center justify-center mx-auto text-purple-300 text-2xl mb-4">
                <i class="fa-solid fa-lock"></i>
            </div>
            <h1 class="text-2xl font-black text-white">Admin Login</h1>
        </div>
        <form action="/admin/login" method="POST" class="space-y-6">
            <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Username</label>
                <input type="text" name="username" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white focus:outline-none focus:border-purple-500 transition">
            </div>
            <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Password</label>
                <input type="password" name="password" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white focus:outline-none focus:border-purple-500 transition">
            </div>
            <button type="submit" class="w-full py-3.5 rounded-xl bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white font-bold shadow-xl glow-effect transition">
                LOGIN TO DASHBOARD
            </button>
        </form>
    </div>
</div>
""")

ADMIN_DASHBOARD_HTML = BASE_HEAD.replace('{% block content %}{% endblock %}', """
<div class="max-w-7xl mx-auto px-4 py-8">
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-8">
        <div>
            <h1 class="text-3xl font-black text-white">Admin Dashboard</h1>
            <p class="text-purple-300/70 text-sm">Manage course plans, orders, and system settings.</p>
        </div>
        <div class="flex items-center gap-3">
            <a href="/admin/reset-stats" onclick="return confirm('Are you sure you want to reset all orders and statistics?');" class="px-4 py-2 rounded-xl bg-amber-950/80 hover:bg-amber-900 text-amber-200 text-sm font-semibold border border-amber-500/30 transition">
                <i class="fa-solid fa-rotate-right mr-1.5"></i> Reset Stats
            </a>
            <a href="/" class="px-4 py-2 rounded-xl bg-purple-900/60 hover:bg-purple-800 text-purple-200 text-sm font-semibold border border-purple-500/30 transition">
                <i class="fa-solid fa-arrow-left mr-1.5"></i> Back to Website
            </a>
            <a href="/admin/logout" class="px-4 py-2 rounded-xl bg-red-950/80 hover:bg-red-900 text-red-200 text-sm font-semibold border border-red-500/30 transition">
                <i class="fa-solid fa-right-from-bracket mr-1.5"></i> Logout
            </a>
        </div>
    </div>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        <div class="glass p-5 rounded-2xl border border-purple-900/50">
            <span class="text-xs text-purple-400 font-semibold uppercase">Total Visits</span>
            <h3 class="text-2xl font-black text-white mt-1">{{ stats.visits }}</h3>
        </div>
        <div class="glass p-5 rounded-2xl border border-purple-900/50">
            <span class="text-xs text-amber-400 font-semibold uppercase">Pending Payments</span>
            <h3 class="text-2xl font-black text-white mt-1">{{ stats.pending }}</h3>
        </div>
        <div class="glass p-5 rounded-2xl border border-purple-900/50">
            <span class="text-xs text-emerald-400 font-semibold uppercase">Approved Orders</span>
            <h3 class="text-2xl font-black text-white mt-1">{{ stats.approved }}</h3>
        </div>
        <div class="glass p-5 rounded-2xl border border-purple-900/50">
            <span class="text-xs text-blue-400 font-semibold uppercase">Verified Revenue</span>
            <h3 class="text-2xl font-black text-white mt-1">₹{{ stats.revenue }}</h3>
        </div>
    </div>
    <div class="flex gap-2 border-b border-purple-900/50 pb-4 mb-8 overflow-x-auto">
        <button onclick="switchTab('orders')" id="tab-btn-orders" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-purple-900 text-white shadow-md transition">Orders ({{ orders|length }})</button>
        <button onclick="switchTab('plans')" id="tab-btn-plans" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-purple-950/60 text-purple-300 hover:bg-purple-900/50 transition">Course Plans ({{ plans|length }})</button>
        <button onclick="switchTab('settings')" id="tab-btn-settings" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-purple-950/60 text-purple-300 hover:bg-purple-900/50 transition">Settings & Bot</button>
    </div>
    <div id="tab-orders" class="space-y-6">
        <div class="glass rounded-2xl border border-purple-900/50 overflow-hidden">
            <div class="p-5 border-b border-purple-900/50 font-bold text-white">Payment Orders & UTR Submissions</div>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse text-sm">
                    <thead>
                        <tr class="bg-purple-950/60 text-purple-300 text-xs uppercase border-b border-purple-900/50">
                            <th class="p-4">Order ID / Date</th>
                            <th class="p-4">Course</th>
                            <th class="p-4">Amount</th>
                            <th class="p-4">UTR Number</th>
                            <th class="p-4">Screenshot</th>
                            <th class="p-4">Status</th>
                            <th class="p-4 text-center">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-purple-900/30">
                        {% for order in orders %}
                        <tr class="hover:bg-purple-900/10 transition">
                            <td class="p-4">
                                <span class="font-mono font-bold text-white block">{{ order.order_id }}</span>
                                <span class="text-xs text-purple-400">{{ order.created_at.strftime('%Y-%m-%d %H:%M') }}</span>
                            </td>
                            <td class="p-4 font-semibold text-purple-200">{{ order.course_name }}</td>
                            <td class="p-4 font-bold text-white">₹{{ order.amount }}</td>
                            <td class="p-4 font-mono text-purple-300">{{ order.utr }}</td>
                            <td class="p-4">
                                {% if order.screenshot %}
                                <a href="/static/uploads/{{ order.screenshot }}" target="_blank" class="text-blue-400 hover:underline text-xs flex items-center gap-1 font-semibold">
                                    <i class="fa-solid fa-image"></i> View
                                </a>
                                {% else %}
                                <span class="text-xs text-purple-400/50">None</span>
                                {% endif %}
                            </td>
                            <td class="p-4">
                                <span class="px-2.5 py-1 rounded-full text-xs font-bold {% if order.status == 'Approved' %}bg-emerald-950 text-emerald-300 border border-emerald-500/30{% elif order.status == 'Rejected' %}bg-red-950 text-red-300 border border-red-500/30{% else %}bg-amber-950 text-amber-300 border border-amber-500/30{% endif %}">{{ order.status }}</span>
                            </td>
                            <td class="p-4 text-center">
                                <div class="flex items-center justify-center gap-2">
                                    <a href="/admin/order/status/{{ order.id }}/Approved" class="px-2.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition" title="Approve"><i class="fa-solid fa-check"></i></a>
                                    <a href="/admin/order/status/{{ order.id }}/Rejected" class="px-2.5 py-1.5 rounded-lg bg-red-600 hover:bg-red-500 text-white text-xs font-bold transition" title="Reject"><i class="fa-solid fa-xmark"></i></a>
                                </div>
                            </td>
                        </tr>
                        {% else %}
                        <tr><td colspan="7" class="p-8 text-center text-purple-400/60">No payment orders submitted yet.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <div id="tab-plans" class="hidden space-y-6">
        <div class="flex justify-between items-center">
            <h2 class="text-xl font-bold text-white">Manage Course Plans</h2>
            <button onclick="openPlanModal()" class="px-4 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-sm shadow-lg transition"><i class="fa-solid fa-plus mr-1.5"></i> Add New Plan</button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {% for plan in plans %}
            <div class="glass rounded-2xl overflow-hidden border border-purple-900/50 flex flex-col">
                <div class="relative h-44 bg-black/60 flex items-center justify-center p-2">
                    <img src="{{ plan.image_url }}" alt="{{ plan.title }}" class="w-full h-full object-contain" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400'">
                    <div class="absolute top-3 right-3 bg-purple-900/90 px-2.5 py-1 rounded-full text-xs font-bold text-purple-200">₹{{ plan.price }}</div>
                </div>
                <div class="p-5 flex flex-col flex-grow">
                    <h3 class="font-bold text-white text-lg">{{ plan.title }}</h3>
                    <p class="text-xs text-purple-300/70 mt-1 flex-grow line-clamp-2">{{ plan.description }}</p>
                    <div class="mt-4 pt-4 border-t border-purple-900/50 flex items-center justify-between">
                        <span class="text-xs {% if plan.enabled %}text-emerald-400{% else %}text-red-400{% endif %} font-semibold">● {% if plan.enabled %}Active{% else %}Disabled{% endif %}</span>
                        <div class="flex gap-2">
                            <button onclick='editPlan({{ {"id": plan.id, "title": plan.title, "description": plan.description, "price": plan.price, "videos_count": plan.videos_count, "validity": plan.validity, "image_url": plan.image_url, "demo_video_urls": plan.demo_video_urls or "", "telegram_url": plan.telegram_url, "demo_instructions": plan.demo_instructions, "enabled": plan.enabled}|tojson|safe }})' class="px-3 py-1.5 rounded-lg bg-purple-800 hover:bg-purple-700 text-white text-xs font-bold transition">Edit</button>
                            <a href="/admin/plan/delete/{{ plan.id }}" onclick="return confirm('Delete this plan?');" class="px-3 py-1.5 rounded-lg bg-red-950 hover:bg-red-900 text-red-200 text-xs font-bold transition">Delete</a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    <div id="tab-settings" class="hidden space-y-6">
        <div class="glass rounded-3xl p-6 md:p-8 border border-purple-900/50">
            <h2 class="text-xl font-bold text-white mb-6">Website, UPI & Telegram Bot Settings</h2>
            <form action="/admin/settings/update" method="POST" class="space-y-6">
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Website Name</label>
                    <input type="text" name="site_name" value="{{ settings.site_name }}" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Website Caption</label>
                    <input type="text" name="site_caption" value="{{ settings.site_caption }}" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white">
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">UPI ID</label>
                        <input type="text" name="upi_id" value="{{ settings.upi_id }}" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white font-mono">
                    </div>
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">UPI Account Name</label>
                        <input type="text" name="upi_name" value="{{ settings.upi_name }}" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white">
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-purple-900/50">
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Telegram Bot Token (For Notifications)</label>
                        <input type="text" name="telegram_bot_token" value="{{ settings.telegram_bot_token }}" placeholder="e.g. 123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ" class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white font-mono">
                    </div>
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Admin Telegram Chat ID</label>
                        <input type="text" name="telegram_chat_id" value="{{ settings.telegram_chat_id }}" placeholder="e.g. 987654321" class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white font-mono">
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Telegram Support Bot URL</label>
                    <input type="text" name="telegram_support" value="{{ settings.telegram_support }}" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Payment Instructions</label>
                    <textarea name="payment_instructions" rows="3" class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white">{{ settings.payment_instructions }}</textarea>
                </div>
                <button type="submit" class="px-8 py-3.5 rounded-xl bg-gradient-to-r from-purple-600 to-blue-600 text-white font-bold shadow-xl transition">SAVE CHANGES</button>
            </form>
        </div>
    </div>
</div>

<div id="plan-modal" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto">
    <div class="glass max-w-xl w-full rounded-3xl p-6 md:p-8 border border-purple-900/50 my-8">
        <div class="flex justify-between items-center mb-6">
            <h3 id="modal-title" class="text-xl font-bold text-white">Add New Course Plan</h3>
            <button onclick="closePlanModal()" class="text-purple-400 hover:text-white text-xl"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <form action="/admin/plan/save" method="POST" class="space-y-4">
            <input type="hidden" name="plan_id" id="modal_plan_id">
            <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-1">Course Title</label>
                <input type="text" name="title" id="modal_title" required class="w-full px-4 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white">
            </div>
            <div class="grid grid-cols-3 gap-3">
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-1">Price (₹)</label>
                    <input type="number" name="price" id="modal_price" required class="w-full px-4 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-1">Videos Count</label>
                    <input type="number" name="videos_count" id="modal_videos" required class="w-full px-4 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-1">Validity</label>
                    <input type="text" name="validity" id="modal_validity" value="Lifetime Access" required class="w-full px-4 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white">
                </div>
            </div>
            <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-1">Main Thumbnail Image URL</label>
                <input type="text" name="image_url" id="modal_image_url" oninput="updatePreview('modal_image_url', 'modal_img_preview')" required class="w-full px-4 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white">
                <div class="mt-3 w-full h-32 rounded-xl overflow-hidden border border-purple-500/30 bg-black/80 flex items-center justify-center p-2">
                    <img id="modal_img_preview" src="" alt="Preview" class="w-full h-full object-contain" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400'">
                </div>
            </div>
            <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-1">Demo Video URLs (Comma Separated)</label>
                <input type="text" name="demo_video_urls" id="modal_demo_video_urls" placeholder="https://..., https://..." class="w-full px-4 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-xs">
            </div>
            <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-1">Support / Contact Link</label>
                <input type="text" name="telegram_url" id="modal_telegram" required class="w-full px-4 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white">
            </div>
            <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-1">Course Description</label>
                <textarea name="description" id="modal_desc" rows="3" required class="w-full px-4 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white"></textarea>
            </div>
            <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-1">Instructions</label>
                <textarea name="demo_instructions" id="modal_instructions" rows="2" required class="w-full px-4 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white"></textarea>
            </div>
            <div class="flex items-center gap-3 pt-2">
                <input type="checkbox" name="enabled" id="modal_enabled" checked class="w-5 h-5 accent-purple-600 rounded">
                <label class="text-sm font-semibold text-purple-200">Enable this plan on homepage</label>
            </div>
            <div class="pt-4 flex gap-3">
                <button type="submit" class="flex-1 py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold transition">Save Plan</button>
                <button type="button" onclick="closePlanModal()" class="px-6 py-3 rounded-xl bg-purple-950 hover:bg-purple-900 text-purple-300 font-bold transition">Cancel</button>
            </div>
        </form>
    </div>
</div>

<script>
function switchTab(tab) {
    document.getElementById('tab-orders').classList.add('hidden');
    document.getElementById('tab-plans').classList.add('hidden');
    document.getElementById('tab-settings').classList.add('hidden');
    document.getElementById('tab-btn-orders').className = 'px-5 py-2.5 rounded-xl font-bold text-sm bg-purple-950/60 text-purple-300 hover:bg-purple-900/50 transition';
    document.getElementById('tab-btn-plans').className = 'px-5 py-2.5 rounded-xl font-bold text-sm bg-purple-950/60 text-purple-300 hover:bg-purple-900/50 transition';
    document.getElementById('tab-btn-settings').className = 'px-5 py-2.5 rounded-xl font-bold text-sm bg-purple-950/60 text-purple-300 hover:bg-purple-900/50 transition';
    document.getElementById('tab-' + tab).classList.remove('hidden');
    document.getElementById('tab-btn-' + tab).className = 'px-5 py-2.5 rounded-xl font-bold text-sm bg-purple-900 text-white shadow-md transition';
}
function updatePreview(inputId, previewId) {
    const url = document.getElementById(inputId).value;
    const preview = document.getElementById(previewId);
    if(url) { preview.src = url; }
}
function openPlanModal() {
    document.getElementById('modal-title').innerText = 'Add New Course Plan';
    document.getElementById('modal_plan_id').value = '';
    document.getElementById('modal_title').value = '';
    document.getElementById('modal_price').value = '199';
    document.getElementById('modal_videos').value = '25';
    document.getElementById('modal_validity').value = 'Lifetime Access';
    document.getElementById('modal_image_url').value = '';
    document.getElementById('modal_demo_video_urls').value = '';
    document.getElementById('modal_img_preview').src = '';
    document.getElementById('modal_telegram').value = 'https://t.me/NexusSupportBot';
    document.getElementById('modal_desc').value = '';
    document.getElementById('modal_instructions').value = '1. Neeche scroll karke saare demo videos dekhein\\n2. Stream smoothly without any lag\\n3. Click Buy Now to join full course';
    document.getElementById('modal_enabled').checked = true;
    document.getElementById('plan-modal').classList.remove('hidden');
}
function editPlan(plan) {
    document.getElementById('modal-title').innerText = 'Edit Course Plan';
    document.getElementById('modal_plan_id').value = plan.id;
    document.getElementById('modal_title').value = plan.title;
    document.getElementById('modal_price').value = plan.price;
    document.getElementById('modal_videos').value = plan.videos_count;
    document.getElementById('modal_validity').value = plan.validity || 'Lifetime Access';
    document.getElementById('modal_image_url').value = plan.image_url;
    document.getElementById('modal_demo_video_urls').value = plan.demo_video_urls || '';
    document.getElementById('modal_img_preview').src = plan.image_url;
    document.getElementById('modal_telegram').value = plan.telegram_url;
    document.getElementById('modal_desc').value = plan.description;
    document.getElementById('modal_instructions').value = plan.demo_instructions;
    document.getElementById('modal_enabled').checked = plan.enabled;
    document.getElementById('plan-modal').classList.remove('hidden');
}
function closePlanModal() {
    document.getElementById('plan-modal').classList.add('hidden');
}
</script>
""")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
