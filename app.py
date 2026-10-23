import os
import json
import requests
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, session, flash, send_from_directory
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
    price = db.Column(db.Integer, nullable=False, default=49)
    original_price = db.Column(db.Integer, nullable=False, default=90)
    videos_count = db.Column(db.String(50), nullable=False, default="50000+")
    validity = db.Column(db.String(100), nullable=False, default="180 days")
    image_url = db.Column(db.String(500), nullable=False)
    demo_video_urls = db.Column(db.Text, nullable=True)
    telegram_url = db.Column(db.String(500), default="https://t.me/NexusSupportBot")
    demo_instructions = db.Column(db.Text, default="You will get the Telegram channel link where all premium videos will be available.")
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
        default_caption = "1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 𝙎𝙐𝙉𝘿𝘼𝙔 ✅"
        initial_plans = [
            (
                "Ultimate Masterclass Pack 1", default_caption, 49, "50000+", "180 days",
                "https://i.ibb.co/Fb6S1mYg/course1.jpg",
                "https://videotourl.com/videos/1791607740001-dfef0130-88bb-4ca0-948d-b857ba8fc867.mp4,https://videotourl.com/videos/1791607674607-203922d8-e261-4085-90fc-4be2fd62a6fb.mp4,https://videotourl.com/videos/1791607662133-116f8c11-861a-4d4c-94a4-411fbd79a4f4.mp4,https://videotourl.com/videos/1791607553470-a87b7709-29e5-449b-89d2-49ce97c8e367.mp4,https://videotourl.com/videos/1791607607288-b1cc3341-7d49-473e-8544-840992806dab.mp4,https://videotourl.com/videos/1791607585444-8a7d8e39-2917-4d23-949e-c048fcbacb2f.mp4,https://videotourl.com/videos/1791607617748-9c8da0dd-313e-4a4d-862b-7ccf034383b7.mp4"
            ),
            (
                "Exclusive Video Bundle 2", default_caption, 49, "45000+", "180 days",
                "https://i.ibb.co/ZRqKVvRQ/course2.jpg",
                "https://videotourl.com/videos/1791609530271-d1845e11-78bd-4465-a0e3-3e0dd57fb424.mp4,https://videotourl.com/videos/1791610410648-c50ab2d2-b1b2-4998-8f5f-43a5f719b603.mp4,https://videotourl.com/videos/1791609652325-1646ca32-e73f-4a5a-9874-a0f4e401c6bb.mp4,https://videotourl.com/videos/1791609624603-358124e2-dbc4-43b2-9772-e18c1df57397.mp4,https://videotourl.com/videos/1791609569957-a7ce2e8a-e185-4dc6-893c-298a2d9c1b4c.mp4"
            ),
            (
                "Premium Creator Pack 3", default_caption, 49, "70000+", "180 days",
                "https://i.ibb.co/21H7BGM2/course3.jpg",
                "https://videotourl.com/videos/1791598226633-9d219b40-bf0b-4774-b493-6449c47d5ef1.mp4,https://videotourl.com/videos/1791598035486-79178a34-a631-49d2-870e-ff3425f1c058.mp4,https://videotourl.com/videos/1791611314862-1e0e5b81-0a04-436a-9749-4f5e9115404f.mp4,https://videotourl.com/videos/1791598059935-f6722923-e315-4b97-aaeb-e7b0af379f2b.mp4,https://videotourl.com/videos/1791598126801-a117ace0-e399-46e6-b697-0d3da6efeedd.mp4,https://videotourl.com/videos/1791598104865-7bca6c3f-db24-465d-9688-d153131af1e5.mp4,https://videotourl.com/videos/1791598207010-15f8101c-d87e-4e83-bd6a-43a333204662.mp4"
            ),
            (
                "Pro Video Collection 4", default_caption, 69, "40000+", "180 days",
                "https://i.ibb.co/QF2v05qK/course4.jpg",
                "https://videotourl.com/videos/1791598317965-12b2368c-6035-4e43-b708-df28bcd246b6.mp4,https://videotourl.com/videos/1791609986226-0b727823-bf05-42b7-80e8-c949f04b95ab.mp4,https://videotourl.com/videos/1791598333066-6d6fc74f-945c-4641-99d1-d862e59790d4.mp4,https://videotourl.com/videos/1791598348006-882fbe39-db59-4bb7-8636-1c2645fb93c0.mp4,https://videotourl.com/videos/1791611260635-789f7a13-25cd-4204-8ffc-455168319040.mp4,https://videotourl.com/videos/1791598360862-d0ddd962-c4e7-4c98-a860-d360bf6779f8.mp4,https://videotourl.com/videos/1791601968259-cb7b49a5-a8c5-45f9-9156-e08f71b052d0.mp4,https://videotourl.com/videos/1791598382840-4245fa8e-38f8-4737-8bb9-a2b8641a3d0f.mp4,https://videotourl.com/videos/1791598397313-ff9dd5ef-d489-4715-a2ca-a71c8923f162.mp4"
            ),
            (
                "Advanced Media Pack 5", default_caption, 58, "30000+", "180 days",
                "https://i.ibb.co/5X0hc5dd/course5.jpg",
                "https://videotourl.com/videos/1791609855846-9b6bac98-1fcf-4d60-b612-3e5abaf6be7e.mp4,https://videotourl.com/videos/1791614058029-1220e2df-44c4-467d-bbd7-755af32ada0c.mp4"
            ),
            (
                "Starter Creators Pack 6", default_caption, 39, "56000+", "180 days",
                "https://i.ibb.co/HLw36KQ4/course6.jpg",
                "https://videotourl.com/videos/1791611037316-4db456f2-f82c-4468-9f48-381341ed6e55.mp4,https://videotourl.com/videos/1791611085614-c863517b-d989-4d6f-b6ef-d23db0b73f5a.mp4,https://videotourl.com/videos/1791611220352-ba6538bc-4db1-401e-81f7-88c53824e27f.mp4,https://videotourl.com/videos/1791609479203-02acf86c-6132-4bc2-8041-9f43ab529748.mp4,https://videotourl.com/videos/1791611168222-86d679dd-8a24-46fb-8b06-d59cc97e84c2.mp4,https://videotourl.com/videos/1791611005214-c25159ac-d514-4eff-8061-a25465ff6eba.mp4"
            ),
            (
                "Mega Creator Bundle 7", default_caption, 49, "67000+", "180 days",
                "https://i.ibb.co/9kKCd6ZF/course7.jpg",
                "https://videotourl.com/videos/1791611423923-36dbbbf3-84c1-4754-a7e4-dc05798eaa03.mp4,https://videotourl.com/videos/1791611350514-052fe889-5ac7-4446-91ef-2f928070e131.mp4,https://videotourl.com/videos/1791609591492-b5b0f616-27c5-436f-9aa9-e70720337677.mp4,https://videotourl.com/videos/1791609952353-7ee9382f-6db6-4c43-86ed-c8f418a3282c.mp4,https://videotourl.com/videos/1791609450717-98fd3d4d-533c-46fc-a290-9f9f937b6721.mp4"
            ),
            (
                "Elite Video Library 8", "1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍", 49, "18000+", "180 days",
                "https://i.ibb.co/C5KZBm7f/course8.jpg",
                "https://videotourl.com/videos/1791611713436-2f106a4b-9ee1-4d9b-8e06-c30a0fe309e7.mp4,https://videotourl.com/videos/1791611779829-f05b75a9-65c7-441d-ad89-5d5f15301b01.mp4"
            ),
            (
                "Super Viral Pack 9", "1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 𝙁𝙍𝙄𝘿𝘼𝙔 ✅.", 69, "70000+", "180 days",
                "https://i.ibb.co/qFhKnzcH/course9.jpg",
                "https://videotourl.com/videos/1791611593469-187437c5-8f84-41c6-afa1-3d61feb9ff72.mp4,https://videotourl.com/videos/1791611552865-c2cf6f7d-1544-4c34-9bdb-5e5fb2092584.mp4"
            )
        ]
        for idx, (title, desc, price, vids, val, img, demo_vids) in enumerate(initial_plans):
            orig_price = round(price * 1.80)
            p = Plan(title=title, description=desc, price=price, original_price=orig_price, videos_count=vids, validity=val, image_url=img, demo_video_urls=demo_vids, order_index=idx)
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

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    if os.environ.get('VERCEL'):
        return send_from_directory('/tmp/uploads', filename)
    else:
        return send_from_directory('static/uploads', filename)

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
    price = int(request.form.get('price', 49))
    original_price = round(price * 1.80)
    videos_count = request.form.get('videos_count', '50000+')
    validity = request.form.get('validity', '180 days')
    image_url = request.form.get('image_url')
    demo_video_urls = request.form.get('demo_video_urls', '')
    demo_instructions = request.form.get('demo_instructions', 'You will get the Telegram channel link where all premium videos will be available.')
    enabled = True if request.form.get('enabled') == 'on' else False
    
    if plan_id:
        plan = Plan.query.get_or_404(plan_id)
        plan.title = title
        plan.description = description
        plan.price = price
        plan.original_price = original_price
        plan.videos_count = videos_count
        plan.validity = validity
        plan.image_url = image_url
        plan.demo_video_urls = demo_video_urls
        plan.demo_instructions = demo_instructions
        plan.enabled = enabled
    else:
        max_order = db.session.query(db.func.max(Plan.order_index)).scalar() or 0
        new_plan = Plan(
            title=title, description=description, price=price, original_price=original_price, videos_count=videos_count, validity=validity,
            image_url=image_url, demo_video_urls=demo_video_urls, demo_instructions=demo_instructions,
            enabled=enabled, order_index=max_order + 1
        )
        db.session.add(new_plan)
    db.session.commit()
    flash(' plan saved successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/plan/delete/<int:plan_id>')
def admin_delete_plan(plan_id):
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    plan = Plan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    flash(' plan deleted successfully!', 'success')
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
        body { background-color: #06010f; color: #f3f4f6; font-family: system-ui, -apple-system, sans-serif; overflow-x: hidden; }
        .glass { background: rgba(18, 5, 38, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(168, 85, 247, 0.18); }
        .glass-card { background: rgba(24, 8, 52, 0.65); backdrop-filter: blur(12px); border: 1px solid rgba(168, 85, 247, 0.15); }
        .glow-effect { box-shadow: 0 0 30px rgba(168, 85, 247, 0.22); }
        .glow-blue { box-shadow: 0 0 30px rgba(59, 130, 246, 0.22); }
        
        @keyframes shine {
            0% { transform: translateX(-100%); }
            20% { transform: translateX(100%); }
            100% { transform: translateX(100%); }
        }
        .shiny-btn { background: linear-gradient(135deg, #9333ea 0%, #4f46e5 100%); position: relative; overflow: hidden; transition: all 0.3s ease; }
        .shiny-btn::after { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent); animation: shine 3s infinite; }
        
        .shiny-red-btn { background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); position: relative; overflow: hidden; transition: all 0.3s ease; }
        .shiny-red-btn::after { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent); animation: shine 3s infinite; }
    </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-purple-500 selection:text-white">
    <header class="glass sticky top-0 z-50 border-b border-purple-900/40">
        <div class="max-w-7xl mx-auto px-4 py-3.5 flex items-center justify-between">
            <a href="/" class="flex items-center gap-2.5">
                <span class="text-xl md:text-2xl font-black bg-gradient-to-r from-purple-400 via-indigo-300 to-blue-400 bg-clip-text text-transparent tracking-tight">{{ settings.site_name }}</span>
            </a>
            <a href="/admin/login" class="px-4 py-2 text-xs md:text-sm font-bold rounded-xl bg-purple-600/80 hover:bg-purple-600 text-white shadow-lg glow-effect transition flex items-center gap-1.5">
                <i class="fa-solid fa-lock text-xs"></i> Admin
            </a>
        </div>
    </header>
    <main class="flex-grow">{% block content %}{% endblock %}</main>
    <a href="{{ settings.telegram_support }}" target="_blank" class="fixed bottom-5 right-5 z-50 bg-blue-600 hover:bg-blue-500 text-white w-12 h-12 md:w-14 md:h-14 rounded-full flex items-center justify-center text-xl md:text-2xl shadow-2xl glow-blue transition transform hover:scale-110">
        <i class="fa-brands fa-telegram"></i>
    </a>
    <footer class="glass border-t border-purple-900/40 py-8 mt-16 text-center text-xs md:text-sm text-purple-300/60">
        <p>&copy; 2026 {{ settings.site_name }}. All rights reserved.</p>
    </footer>
</body>
</html>
"""

INDEX_HTML = BASE_HEAD.replace('{% block content %}{% endblock %}', """
<section class="py-10 md:py-14 px-4 text-center">
    <div class="max-w-4xl mx-auto space-y-3">
        <span class="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider bg-purple-950 text-purple-300 border border-purple-500/30 shadow-inner">
            <i class="fa-solid fa-bolt text-amber-400"></i> premium porn store 
        </span>
        <h1 class="text-3xl sm:text-4xl md:text-6xl font-black tracking-tight bg-gradient-to-r from-white via-purple-200 to-blue-300 bg-clip-text text-transparent px-2">
            {{ settings.site_name }}
        </h1>
        <p class="text-sm md:text-base text-purple-200/70 max-w-2xl mx-auto px-4">
            {{ settings.site_caption }}
        </p>
    </div>
</section>

<section class="max-w-7xl mx-auto px-4 pb-20">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
        {% for plan in plans %}
        <div class="glass-card rounded-3xl overflow-hidden border border-purple-900/50 hover:border-purple-500/50 transition duration-300 flex flex-col group shadow-xl">
            <!-- Un-cropped Image Frame with Special Offer & 70% Off Badge -->
            <div class="relative w-full h-56 sm:h-60 bg-black/90 flex items-center justify-center p-3 overflow-hidden border-b border-purple-950">
                <img src="{{ plan.image_url }}" alt="{{ plan.title }}" class="w-full h-full object-contain group-hover:scale-105 transition duration-500 drop-shadow-md" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600'">
                
                <div class="absolute top-3 left-3 bg-gradient-to-r from-amber-500 to-orange-600 text-white text-[10px] font-black uppercase px-2.5 py-1 rounded-lg shadow-lg tracking-wider flex items-center gap-1">
                    <i class="fa-solid fa-tag"></i> 70% OFF
                </div>

                <div class="absolute top-3 right-3 bg-purple-950/90 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold text-purple-200 border border-purple-500/30">
                    <i class="fa-solid fa-video text-purple-400 mr-1"></i> {{ plan.videos_count }}
                </div>
            </div>

            <!-- Content Area -->
            <div class="p-5 sm:p-6 flex flex-col flex-grow">
                <h3 class="text-lg sm:text-xl font-black text-white group-hover:text-purple-300 transition line-clamp-1">{{ plan.title }}</h3>
                <div class="mt-2 text-xs sm:text-sm text-purple-200/70 flex-grow line-clamp-3 leading-relaxed whitespace-pre-line">{{ plan.description }}</div>
                
                <!-- Telegram Channel Info Box -->
                <div class="mt-3 p-2.5 rounded-xl bg-blue-950/40 border border-blue-500/30 text-[11px] text-blue-200 flex items-center gap-2">
                    <i class="fa-brands fa-telegram text-blue-400 text-base shrink-0"></i>
                    <span>You will get the Telegram channel link where all premium videos will be available.</span>
                </div>

                <!-- Pricing Section -->
                <div class="mt-4 mb-4 flex items-center justify-between border-t border-purple-900/40 pt-3">
                    <div>
                        <span class="text-[10px] text-purple-400 font-bold uppercase tracking-wider block">Special Price</span>
                        <div class="flex items-center gap-2 mt-0.5">
                            <span class="text-2xl font-black text-white">₹{{ plan.price }}</span>
                            <span class="text-xs text-purple-400/60 line-through font-semibold">₹{{ plan.original_price }}</span>
                        </div>
                    </div>
                    <span class="px-2.5 py-1 rounded-lg bg-emerald-950/80 text-emerald-400 text-xs font-bold border border-emerald-500/30">
                        Validity: {{ plan.validity }}
                    </span>
                </div>

                <!-- Stacked Buttons: View Demo (Red Top) & Buy Now (Gradient Bottom) with Shining Animation -->
                <div class="flex flex-col gap-2.5 mt-auto">
                    <a href="/demo/{{ plan.id }}" class="w-full py-3.5 rounded-xl shiny-red-btn text-white text-center text-xs sm:text-sm font-bold shadow-lg flex items-center justify-center gap-2 tracking-wide">
                        <i class="fa-solid fa-circle-play text-sm"></i> VIEW DEMO & DETAILS
                    </a>
                    <a href="/payment/{{ plan.id }}" class="w-full py-3.5 rounded-xl shiny-btn text-white text-center text-xs sm:text-sm font-black shadow-lg glow-effect flex items-center justify-center gap-2 tracking-wide">
                        <i class="fa-solid fa-bolt text-amber-300 text-sm"></i> BUY NOW (₹{{ plan.price }})
                    </a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</section>
""")

DEMO_HTML = BASE_HEAD.replace('{% block content %}{% endblock %}', """
<div class="max-w-4xl mx-auto px-4 py-8 sm:py-12">
    <a href="/" class="inline-flex items-center gap-2 text-xs sm:text-sm font-semibold text-purple-400 hover:text-purple-300 mb-6 transition">
        <i class="fa-solid fa-arrow-left"></i> Back to Courses
    </a>
    <div class="glass rounded-3xl p-5 sm:p-8 md:p-10 border border-purple-900/50 glow-effect flex flex-col gap-8 shadow-2xl">
        
        <!-- Main Thumbnail Frame (Un-cropped) -->
        <div class="w-full rounded-2xl overflow-hidden border border-purple-500/30 h-72 sm:h-96 bg-black/90 flex items-center justify-center p-3 relative">
            <img src="{{ plan.image_url }}" alt="{{ plan.title }}" class="w-full h-full object-contain drop-shadow-2xl" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800'">
            <div class="absolute top-4 left-4 bg-gradient-to-r from-amber-500 to-orange-600 text-white text-xs font-black uppercase px-3 py-1.5 rounded-xl shadow-lg">
                <i class="fa-solid fa-tag mr-1"></i> 70% OFF Deal
            </div>
        </div>

        <!-- Structured Plan Details Box -->
        <div class="glass-card p-5 sm:p-6 rounded-2xl border border-purple-500/30 space-y-4">
            <h1 class="text-2xl sm:text-3xl font-black text-white leading-tight">{{ plan.title }}</h1>
            <div class="text-purple-200/80 text-xs sm:text-sm leading-relaxed whitespace-pre-line">{{ plan.description }}</div>
            
            <!-- Telegram Channel Notice Box -->
            <div class="p-3 rounded-xl bg-blue-950/50 border border-blue-500/30 text-xs text-blue-200 flex items-center gap-3">
                <i class="fa-brands fa-telegram text-blue-400 text-xl shrink-0"></i>
                <span>You will get the Telegram channel link where all premium videos will be available.</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-4 border-t border-purple-900/50 text-xs sm:text-sm">
                <div class="flex flex-col bg-purple-950/50 p-3 rounded-xl border border-purple-900/40">
                    <span class="text-purple-400 text-[10px] font-bold uppercase tracking-wider">Total Videos</span>
                    <span class="text-white font-bold mt-0.5">{{ plan.videos_count }} HD Lessons</span>
                </div>
                <div class="flex flex-col bg-purple-950/50 p-3 rounded-xl border border-purple-900/40">
                    <span class="text-purple-400 text-[10px] font-bold uppercase tracking-wider">Validity</span>
                    <span class="text-emerald-400 font-bold mt-0.5 flex items-center gap-1"><i class="fa-solid fa-calendar-days"></i> {{ plan.validity }}</span>
                </div>
                <div class="flex flex-col bg-purple-950/50 p-3 rounded-xl border border-purple-900/40">
                    <span class="text-purple-400 text-[10px] font-bold uppercase tracking-wider">Access Type</span>
                    <span class="text-blue-400 font-bold mt-0.5">Instant Delivery</span>
                </div>
            </div>

            <div class="flex items-center justify-between pt-2">
                <div>
                    <span class="text-xs text-purple-400 font-semibold">Special Discount Price</span>
                    <div class="flex items-center gap-3">
                        <span class="text-3xl font-black text-white">₹{{ plan.price }}</span>
                        <span class="text-sm text-purple-400/60 line-through font-semibold">₹{{ plan.original_price }}</span>
                    </div>
                </div>
                <span class="px-3 py-1 rounded-xl bg-emerald-950 text-emerald-400 text-xs font-black border border-emerald-500/30">
                    Save ₹{{ plan.original_price - plan.price }}
                </span>
            </div>
        </div>

        <!-- Dynamic Demo Videos Stacked Vertically -->
        {% if demo_list %}
        <div class="pt-4 border-t border-purple-900/40 flex flex-col gap-6">
            <h3 class="text-lg sm:text-xl font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-play-circle text-red-500"></i>  Demo Videos
            </h3>
            {% for v_url in demo_list %}
            {% if v_url %}
            <div class="flex flex-col gap-2">
                <span class="text-xs font-bold text-purple-300 uppercase tracking-wider">Demo Video {{ loop.index }}</span>
                <div class="w-full rounded-2xl overflow-hidden border border-purple-500/30 bg-black flex items-center justify-center shadow-2xl">
                    <video controls preload="metadata" class="w-full max-h-[450px] object-contain focus:outline-none">
                        <source src="{{ v_url }}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </div>
            </div>
            {% endif %}
            {% endfor %}
        </div>
        {% endif %}

        <div class="p-5 rounded-2xl bg-purple-950/40 border border-purple-500/20">
            <h4 class="font-bold text-purple-300 mb-2 text-sm sm:text-base flex items-center gap-2">
                <i class="fa-solid fa-circle-question text-purple-400"></i> Quick Instructions
            </h4>
            <div class="text-xs sm:text-sm text-purple-200/80 whitespace-pre-line leading-relaxed">{{ plan.demo_instructions }}</div>
        </div>

        <!-- Vertically Stacked Action Buttons with Shining Animation -->
        <div class="pt-4 border-t border-purple-900/40 flex flex-col gap-3.5">
            <a href="{{ plan.telegram_url }}" target="_blank" class="w-full py-4 rounded-2xl shiny-red-btn text-white text-center font-bold text-sm sm:text-base shadow-xl flex items-center justify-center gap-2">
                <i class="fa-solid fa-headset text-lg"></i> Telegram Support 
            </a>
            <a href="/payment/{{ plan.id }}" class="w-full py-4 rounded-2xl shiny-btn text-white text-center font-black text-sm sm:text-base shadow-xl glow-effect flex items-center justify-center gap-2">
                <i class="fa-solid fa-bolt text-amber-300"></i> BUY NOW — UNLOCK INSTANT ACCESS (₹{{ plan.price }})
            </a>
        </div>
    </div>
</div>
""")

PAYMENT_HTML = BASE_HEAD.replace('{% block content %}{% endblock %}', """
<div class="max-w-xl mx-auto px-4 py-8 sm:py-12">
    <a href="/demo/{{ plan.id }}" class="inline-flex items-center gap-2 text-xs sm:text-sm font-semibold text-purple-400 hover:text-purple-300 mb-6">
        <i class="fa-solid fa-arrow-left"></i> Back to Course
    </a>
    <div class="glass rounded-3xl p-5 sm:p-8 border border-purple-900/50 glow-effect relative">
        <div class="text-center pb-6 border-b border-purple-900/40">
            <span class="px-3 py-1 rounded-full text-[11px] font-bold uppercase bg-emerald-950 text-emerald-300 border border-emerald-500/30">
                <i class="fa-solid fa-shield-halved mr-1"></i> SECURE UPI PAYMENT
            </span>
            <h1 class="text-xl sm:text-2xl font-black text-white mt-3">{{ plan.title }}</h1>
            <p class="text-purple-300/70 text-xs sm:text-sm mt-1">Amount Payable: <strong class="text-white text-base">₹{{ plan.price }}</strong></p>
        </div>

        <div class="my-6 text-center bg-purple-950/60 p-5 rounded-2xl border border-purple-500/30">
            <p class="text-xs font-semibold text-purple-300 mb-3">Scan QR code using GPay, PhonePe, or Paytm</p>
            <div class="inline-block bg-white p-3 rounded-2xl shadow-xl">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=upi://pay?pa={{ settings.upi_id }}&pn={{ settings.upi_name }}&am={{ plan.price }}&cu=INR" alt="UPI QR Code" class="w-40 h-40 sm:w-48 sm:h-48 mx-auto rounded-xl">
            </div>
            <div class="mt-3 flex items-center justify-center gap-2">
                <span class="text-xs sm:text-sm font-mono text-purple-200 bg-purple-900/60 px-3 py-2 rounded-xl border border-purple-500/30 truncate max-w-[220px]">{{ settings.upi_id }}</span>
                <button onclick="navigator.clipboard.writeText('{{ settings.upi_id }}'); alert('UPI ID Copied!');" class="px-3 py-2 bg-purple-800 hover:bg-purple-700 text-white rounded-xl text-xs transition">
                    <i class="fa-solid fa-copy"></i>
                </button>
            </div>
        </div>

        <div class="mb-6 p-4 rounded-xl bg-purple-950/40 border border-purple-500/20 text-xs text-purple-300/80 leading-relaxed whitespace-pre-line">
            {{ settings.payment_instructions }}
        </div>

        <form id="payment-form" action="/payment/{{ plan.id }}" method="POST" enctype="multipart/form-data" class="space-y-5" onsubmit="showLoadingPopup()">
            <div>
                <label class="block text-xs sm:text-sm font-bold text-purple-200 mb-2">12-Digit UTR / Transaction Reference Number *</label>
                <input type="text" name="utr" required placeholder="e.g. 432156789012" class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm focus:outline-none focus:border-purple-500 transition font-mono">
            </div>
            <div>
                <label class="block text-xs sm:text-sm font-bold text-purple-200 mb-2">Upload Payment Screenshot *</label>
                <input type="file" name="screenshot" accept="image/*" required class="w-full px-3 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-xs text-purple-300 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-purple-800 file:text-white hover:file:bg-purple-700 transition">
            </div>
            <button type="submit" class="w-full py-4 rounded-2xl shiny-btn text-white font-black text-sm sm:text-base shadow-xl glow-effect transition flex items-center justify-center gap-2">
                <i class="fa-solid fa-check-circle text-amber-300"></i> SUBMIT PAYMENT DETAILS
            </button>
        </form>
    </div>
</div>

<!-- Glassmorphism Payment Submitting Popup -->
<div id="payment-loading-popup" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
    <div class="glass max-w-sm w-full rounded-3xl p-8 border border-purple-500/30 text-center flex flex-col items-center gap-4 glow-effect shadow-2xl">
        <div class="w-14 h-14 border-4 border-purple-900 border-t-emerald-400 rounded-full animate-spin"></div>
        <h3 class="text-xl font-bold text-white">Payment Submitting...</h3>
        <p class="text-xs text-purple-300/80">Please wait while we record and verify your transaction.</p>
    </div>
</div>

<script>
function showLoadingPopup() {
    document.getElementById('payment-loading-popup').classList.remove('hidden');
}
</script>
""")

SUCCESS_HTML = BASE_HEAD.replace('{% block content %}{% endblock %}', """
<div class="max-w-xl mx-auto px-4 py-12 sm:py-16 text-center">
    <div class="glass rounded-3xl p-6 sm:p-8 border border-purple-900/50 glow-effect">
        <!-- Big Green Tick Badge -->
        <div class="w-20 h-20 bg-emerald-500/20 border-2 border-emerald-500 rounded-full flex items-center justify-center mx-auto text-emerald-400 text-4xl mb-6 shadow-2xl animate-bounce">
            <i class="fa-solid fa-check"></i>
        </div>
        <h1 class="text-2xl font-black text-white">Payment Submitted!</h1>
        <p class="text-purple-300/80 text-xs sm:text-sm mt-2">Your payment details and screenshot have been recorded successfully.</p>
        
        <!-- Plan & Order Details -->
        <div class="my-6 p-5 rounded-2xl bg-purple-950/60 border border-purple-500/30 text-left space-y-3 text-xs sm:text-sm">
            <div class="flex justify-between border-b border-purple-900/40 pb-2"><span class="text-purple-400 font-semibold">Order ID:</span> <span class="font-mono text-white font-bold">{{ order.order_id }}</span></div>
            <div class="flex justify-between border-b border-purple-900/40 pb-2"><span class="text-purple-400 font-semibold">Course / Plan:</span> <span class="text-white font-bold">{{ order.course_name }}</span></div>
            <div class="flex justify-between border-b border-purple-900/40 pb-2"><span class="text-purple-400 font-semibold">Amount Paid:</span> <span class="text-white font-bold">₹{{ order.amount }}</span></div>
            <div class="flex justify-between border-b border-purple-900/40 pb-2"><span class="text-purple-400 font-semibold">UTR Number:</span> <span class="font-mono text-white">{{ order.utr }}</span></div>
            <div class="flex justify-between"><span class="text-purple-400 font-semibold">Status:</span> <span class="px-3 py-1 rounded-full text-xs font-bold bg-amber-950 text-amber-300 border border-amber-500/30">{{ order.status }}</span></div>
        </div>
        
        <a href="/" class="inline-block px-8 py-3.5 rounded-xl shiny-btn text-white font-bold text-xs sm:text-sm shadow-lg transition">
            Return to Homepage
        </a>
    </div>
</div>
""")

ADMIN_LOGIN_HTML = BASE_HEAD.replace('{% block content %}{% endblock %}', """
<div class="max-w-md mx-auto px-4 py-16 sm:py-20">
    <div class="glass rounded-3xl p-6 sm:p-8 border border-purple-900/50 glow-effect">
        <div class="text-center mb-6">
            <div class="w-16 h-16 bg-purple-900/50 border border-purple-500/30 rounded-2xl flex items-center justify-center mx-auto text-purple-300 text-2xl mb-4 shadow-inner">
                <i class="fa-solid fa-lock"></i>
            </div>
            <h1 class="text-xl sm:text-2xl font-black text-white">Admin Login</h1>
        </div>
        <form action="/admin/login" method="POST" class="space-y-5">
            <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Username</label>
                <input type="text" name="username" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm focus:outline-none focus:border-purple-500 transition">
            </div>
            <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Password</label>
                <input type="password" name="password" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm focus:outline-none focus:border-purple-500 transition">
            </div>
            <button type="submit" class="w-full py-3.5 rounded-xl shiny-btn text-white font-bold text-sm shadow-xl glow-effect transition">
                LOGIN TO DASHBOARD
            </button>
        </form>
    </div>
</div>
""")

ADMIN_DASHBOARD_HTML = BASE_HEAD.replace('{% block content %}{% endblock %}', """
<div class="max-w-7xl mx-auto px-4 py-8 overflow-hidden">
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-8">
        <div>
            <h1 class="text-2xl sm:text-3xl font-black text-white">Admin Dashboard</h1>
            <p class="text-purple-300/70 text-xs sm:text-sm">Manage course plans, orders, and system settings.</p>
        </div>
        <div class="flex flex-wrap items-center gap-2.5">
            <a href="/admin/reset-stats" onclick="return confirm('Are you sure you want to reset all orders and statistics?');" class="px-3.5 py-2 rounded-xl bg-amber-950/80 hover:bg-amber-900 text-amber-200 text-xs font-semibold border border-amber-500/30 transition">
                <i class="fa-solid fa-rotate-right mr-1"></i> Reset Stats
            </a>
            <a href="/" class="px-3.5 py-2 rounded-xl bg-purple-900/60 hover:bg-purple-800 text-purple-200 text-xs font-semibold border border-purple-500/30 transition">
                <i class="fa-solid fa-arrow-left mr-1"></i> Website
            </a>
            <a href="/admin/logout" class="px-3.5 py-2 rounded-xl bg-red-950/80 hover:bg-red-900 text-red-200 text-xs font-semibold border border-red-500/30 transition">
                <i class="fa-solid fa-right-from-bracket mr-1"></i> Logout
            </a>
        </div>
    </div>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4 mb-8">
        <div class="glass p-4 sm:p-5 rounded-2xl border border-purple-900/50">
            <span class="text-[11px] text-purple-400 font-semibold uppercase">Total Visits</span>
            <h3 class="text-xl sm:text-2xl font-black text-white mt-1">{{ stats.visits }}</h3>
        </div>
        <div class="glass p-4 sm:p-5 rounded-2xl border border-purple-900/50">
            <span class="text-[11px] text-amber-400 font-semibold uppercase">Pending</span>
            <h3 class="text-xl sm:text-2xl font-black text-white mt-1">{{ stats.pending }}</h3>
        </div>
        <div class="glass p-4 sm:p-5 rounded-2xl border border-purple-900/50">
            <span class="text-[11px] text-emerald-400 font-semibold uppercase">Approved</span>
            <h3 class="text-xl sm:text-2xl font-black text-white mt-1">{{ stats.approved }}</h3>
        </div>
        <div class="glass p-4 sm:p-5 rounded-2xl border border-purple-900/50">
            <span class="text-[11px] text-blue-400 font-semibold uppercase">Revenue</span>
            <h3 class="text-xl sm:text-2xl font-black text-white mt-1">₹{{ stats.revenue }}</h3>
        </div>
    </div>

    <div class="flex gap-2 border-b border-purple-900/50 pb-4 mb-8 overflow-x-auto">
        <button onclick="switchTab('orders')" id="tab-btn-orders" class="px-4 py-2 rounded-xl font-bold text-xs sm:text-sm bg-purple-900 text-white shadow-md transition whitespace-nowrap">Orders ({{ orders|length }})</button>
        <button onclick="switchTab('plans')" id="tab-btn-plans" class="px-4 py-2 rounded-xl font-bold text-xs sm:text-sm bg-purple-950/60 text-purple-300 hover:bg-purple-900/50 transition whitespace-nowrap">Course Plans ({{ plans|length }})</button>
        <button onclick="switchTab('settings')" id="tab-btn-settings" class="px-4 py-2 rounded-xl font-bold text-xs sm:text-sm bg-purple-950/60 text-purple-300 hover:bg-purple-900/50 transition whitespace-nowrap">Settings & Bot</button>
    </div>

    <div id="tab-orders" class="space-y-6">
        <div class="glass rounded-2xl border border-purple-900/50 overflow-hidden">
            <div class="p-4 sm:p-5 border-b border-purple-900/50 font-bold text-white text-sm">Payment Orders & UTR Submissions</div>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse text-xs sm:text-sm">
                    <thead>
                        <tr class="bg-purple-950/60 text-purple-300 text-[10px] sm:text-xs uppercase border-b border-purple-900/50">
                            <th class="p-3 sm:p-4">Order ID / Date</th>
                            <th class="p-3 sm:p-4">Course</th>
                            <th class="p-3 sm:p-4">Amount</th>
                            <th class="p-3 sm:p-4">UTR Number</th>
                            <th class="p-3 sm:p-4">Screenshot</th>
                            <th class="p-3 sm:p-4">Status</th>
                            <th class="p-3 sm:p-4 text-center">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-purple-900/30">
                        {% for order in orders %}
                        <tr class="hover:bg-purple-900/10 transition">
                            <td class="p-3 sm:p-4">
                                <span class="font-mono font-bold text-white block">{{ order.order_id }}</span>
                                <span class="text-[10px] text-purple-400">{{ order.created_at.strftime('%Y-%m-%d %H:%M') }}</span>
                            </td>
                            <td class="p-3 sm:p-4 font-semibold text-purple-200">{{ order.course_name }}</td>
                            <td class="p-3 sm:p-4 font-bold text-white">₹{{ order.amount }}</td>
                            <td class="p-3 sm:p-4 font-mono text-purple-300">{{ order.utr }}</td>
                            <td class="p-3 sm:p-4">
                                {% if order.screenshot %}
                                <a href="/static/uploads/{{ order.screenshot }}" target="_blank" class="text-blue-400 hover:underline text-xs flex items-center gap-1 font-semibold">
                                    <i class="fa-solid fa-image"></i> View
                                </a>
                                {% else %}
                                <span class="text-xs text-purple-400/50">None</span>
                                {% endif %}
                            </td>
                            <td class="p-3 sm:p-4">
                                <span class="px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-bold {% if order.status == 'Approved' %}bg-emerald-950 text-emerald-300 border border-emerald-500/30{% elif order.status == 'Rejected' %}bg-red-950 text-red-300 border border-red-500/30{% else %}bg-amber-950 text-amber-300 border border-amber-500/30{% endif %}">{{ order.status }}</span>
                            </td>
                            <td class="p-3 sm:p-4 text-center">
                                <div class="flex items-center justify-center gap-1.5">
                                    <a href="/admin/order/status/{{ order.id }}/Approved" class="px-2 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition" title="Approve"><i class="fa-solid fa-check"></i></a>
                                    <a href="/admin/order/status/{{ order.id }}/Rejected" class="px-2 py-1 rounded-lg bg-red-600 hover:bg-red-500 text-white text-xs font-bold transition" title="Reject"><i class="fa-solid fa-xmark"></i></a>
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
            <h2 class="text-lg sm:text-xl font-bold text-white">Manage Course Plans</h2>
            <button onclick="openPlanModal()" class="px-4 py-2 rounded-xl shiny-btn text-white font-bold text-xs sm:text-sm shadow-lg transition"><i class="fa-solid fa-plus mr-1"></i> Add New Plan</button>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {% for plan in plans %}
            <div class="glass rounded-2xl overflow-hidden border border-purple-900/50 flex flex-col">
                <div class="relative h-40 bg-black/80 flex items-center justify-center p-2">
                    <img src="{{ plan.image_url }}" alt="{{ plan.title }}" class="w-full h-full object-contain" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400'">
                    <div class="absolute top-2 right-2 bg-purple-900/90 px-2 py-0.5 rounded-lg text-xs font-bold text-purple-200">₹{{ plan.price }}</div>
                </div>
                <div class="p-4 sm:p-5 flex flex-col flex-grow">
                    <h3 class="font-bold text-white text-base truncate">{{ plan.title }}</h3>
                    <div class="text-xs text-purple-300/70 mt-1 flex-grow line-clamp-2 whitespace-pre-line">{{ plan.description }}</div>
                    <div class="mt-4 pt-3 border-t border-purple-900/50 flex items-center justify-between">
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
        <div class="glass rounded-3xl p-5 sm:p-8 border border-purple-900/50">
            <h2 class="text-lg sm:text-xl font-bold text-white mb-6">Website, UPI & Telegram Bot Settings</h2>
            <form action="/admin/settings/update" method="POST" class="space-y-5">
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Website Name</label>
                    <input type="text" name="site_name" value="{{ settings.site_name }}" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Website Caption</label>
                    <input type="text" name="site_caption" value="{{ settings.site_caption }}" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm">
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">UPI ID</label>
                        <input type="text" name="upi_id" value="{{ settings.upi_id }}" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white font-mono text-sm">
                    </div>
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">UPI Account Name</label>
                        <input type="text" name="upi_name" value="{{ settings.upi_name }}" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm">
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-5 pt-3 border-t border-purple-900/50">
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Telegram Bot Token</label>
                        <input type="text" name="telegram_bot_token" value="{{ settings.telegram_bot_token }}" placeholder="e.g. 123456789:ABC..." class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white font-mono text-sm">
                    </div>
                    <div>
                        <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Admin Telegram Chat ID</label>
                        <input type="text" name="telegram_chat_id" value="{{ settings.telegram_chat_id }}" placeholder="e.g. 987654321" class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white font-mono text-sm">
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Telegram Support Bot URL</label>
                    <input type="text" name="telegram_support" value="{{ settings.telegram_support }}" required class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-purple-300 mb-2">Payment Instructions</label>
                    <textarea name="payment_instructions" rows="3" class="w-full px-4 py-3 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm">{{ settings.payment_instructions }}</textarea>
                </div>
                <button type="submit" class="px-8 py-3 rounded-xl shiny-btn text-white font-bold text-sm shadow-xl transition">SAVE CHANGES</button>
            </form>
        </div>
    </div>
</div>

<!-- Plan Modal (Fixed Overflow & Screen Fit) -->
<div id="plan-modal" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-2 sm:p-4 overflow-y-auto">
    <div class="glass max-w-xl w-full rounded-3xl p-5 sm:p-8 border border-purple-900/50 my-6 max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-4">
            <h3 id="modal-title" class="text-lg sm:text-xl font-bold text-white">Add New Course Plan</h3>
            <button onclick="closePlanModal()" class="text-purple-400 hover:text-white text-xl"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <form action="/admin/plan/save" method="POST" class="space-y-3.5">
            <input type="hidden" name="plan_id" id="modal_plan_id">
            <div>
                <label class="block text-[11px] font-bold uppercase tracking-wider text-purple-300 mb-1">Course Title</label>
                <input type="text" name="title" id="modal_title" required class="w-full px-3.5 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm">
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
                <div>
                    <label class="block text-[11px] font-bold uppercase tracking-wider text-purple-300 mb-1">Price (₹)</label>
                    <input type="number" name="price" id="modal_price" required class="w-full px-3 py-2 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm">
                </div>
                <div>
                    <label class="block text-[11px] font-bold uppercase tracking-wider text-purple-300 mb-1">Videos</label>
                    <input type="text" name="videos_count" id="modal_videos" required class="w-full px-3 py-2 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm">
                </div>
                <div>
                    <label class="block text-[11px] font-bold uppercase tracking-wider text-purple-300 mb-1">Validity</label>
                    <input type="text" name="validity" id="modal_validity" value="180 days" required class="w-full px-3 py-2 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm">
                </div>
            </div>
            <div>
                <label class="block text-[11px] font-bold uppercase tracking-wider text-purple-300 mb-1">Thumbnail Image URL</label>
                <input type="text" name="image_url" id="modal_image_url" oninput="updatePreview('modal_image_url', 'modal_img_preview')" required class="w-full px-3.5 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm">
                <div class="mt-2 w-full h-28 rounded-xl overflow-hidden border border-purple-500/30 bg-black/90 flex items-center justify-center p-2">
                    <img id="modal_img_preview" src="" alt="Preview" class="w-full h-full object-contain" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400'">
                </div>
            </div>
            <div>
                <label class="block text-[11px] font-bold uppercase tracking-wider text-purple-300 mb-1">Demo Video URLs (Comma Separated)</label>
                <input type="text" name="demo_video_urls" id="modal_demo_video_urls" placeholder="https://..., https://..." class="w-full px-3.5 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-xs font-mono">
            </div>
            <div>
                <label class="block text-[11px] font-bold uppercase tracking-wider text-purple-300 mb-1">Support Link</label>
                <input type="text" name="telegram_url" id="modal_telegram" required class="w-full px-3.5 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm">
            </div>
            <div>
                <label class="block text-[11px] font-bold uppercase tracking-wider text-purple-300 mb-1">Caption / Description</label>
                <textarea name="description" id="modal_desc" rows="3" required class="w-full px-3.5 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm"></textarea>
            </div>
            <div>
                <label class="block text-[11px] font-bold uppercase tracking-wider text-purple-300 mb-1">Instructions</label>
                <textarea name="demo_instructions" id="modal_instructions" rows="2" required class="w-full px-3.5 py-2.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-white text-sm"></textarea>
            </div>
            <div class="flex items-center gap-2.5 pt-1">
                <input type="checkbox" name="enabled" id="modal_enabled" checked class="w-4 h-4 accent-purple-600 rounded">
                <label class="text-xs font-semibold text-purple-200">Enable this plan on homepage</label>
            </div>
            <div class="pt-3 flex gap-2.5">
                <button type="submit" class="flex-1 py-3 rounded-xl shiny-btn text-white font-bold text-sm transition">Save Plan</button>
                <button type="button" onclick="closePlanModal()" class="px-5 py-3 rounded-xl bg-purple-950 hover:bg-purple-900 text-purple-300 font-bold text-sm transition">Cancel</button>
            </div>
        </form>
    </div>
</div>

<script>
function switchTab(tab) {
    document.getElementById('tab-orders').classList.add('hidden');
    document.getElementById('tab-plans').classList.add('hidden');
    document.getElementById('tab-settings').classList.add('hidden');
    document.getElementById('tab-btn-orders').className = 'px-4 py-2 rounded-xl font-bold text-xs sm:text-sm bg-purple-950/60 text-purple-300 hover:bg-purple-900/50 transition whitespace-nowrap';
    document.getElementById('tab-btn-plans').className = 'px-4 py-2 rounded-xl font-bold text-xs sm:text-sm bg-purple-950/60 text-purple-300 hover:bg-purple-900/50 transition whitespace-nowrap';
    document.getElementById('tab-btn-settings').className = 'px-4 py-2 rounded-xl font-bold text-xs sm:text-sm bg-purple-950/60 text-purple-300 hover:bg-purple-900/50 transition whitespace-nowrap';
    document.getElementById('tab-' + tab).classList.remove('hidden');
    document.getElementById('tab-btn-' + tab).className = 'px-4 py-2 rounded-xl font-bold text-xs sm:text-sm bg-purple-900 text-white shadow-md transition whitespace-nowrap';
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
    document.getElementById('modal_price').value = '49';
    document.getElementById('modal_videos').value = '50000+';
    document.getElementById('modal_validity').value = '180 days';
    document.getElementById('modal_image_url').value = '';
    document.getElementById('modal_demo_video_urls').value = '';
    document.getElementById('modal_img_preview').src = '';
    document.getElementById('modal_telegram').value = 'https://t.me/NexusSupportBot';
    document.getElementById('modal_desc').value = '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\\n2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\\n3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\\n4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 𝙎𝙐𝙉𝘿𝘼𝙔 ✅';
    document.getElementById('modal_instructions').value = 'You will get the Telegram channel link where all premium videos will be available.';
    document.getElementById('modal_enabled').checked = true;
    document.getElementById('plan-modal').classList.remove('hidden');
}
function editPlan(plan) {
    document.getElementById('modal-title').innerText = 'Edit Course Plan';
    document.getElementById('modal_plan_id').value = plan.id;
    document.getElementById('modal_title').value = plan.title;
    document.getElementById('modal_price').value = plan.price;
    document.getElementById('modal_videos').value = plan.videos_count;
    document.getElementById('modal_validity').value = plan.validity || '180 days';
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
