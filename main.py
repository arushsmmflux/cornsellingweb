<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NEXUS COURSES — Premium Learning Platform</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- FontAwesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              dark: '#07040D',
              surface: '#0F0920',
              card: '#150D2E',
              border: 'rgba(139, 92, 246, 0.2)',
              purple: '#7C3AED',
              purpleGlow: '#A855F7',
              blue: '#2563EB',
              cyan: '#06B6D4',
              accent: '#00F0FF'
            }
          },
          fontFamily: {
            sans: ['Plus Jakarta Sans', 'sans-serif'],
          },
          animation: {
            'pulse-glow': 'pulseGlow 3s infinite alternate',
            'float': 'float 4s ease-in-out infinite',
          },
          keyframes: {
            pulseGlow: {
              '0%': { boxShadow: '0 0 15px rgba(124, 58, 237, 0.2)' },
              '100%': { boxShadow: '0 0 35px rgba(0, 240, 255, 0.4)' }
            },
            float: {
              '0%, 100%': { transform: 'translateY(0px)' },
              '50%': { transform: 'translateY(-8px)' }
            }
          }
        }
      }
    }
  </script>

  <style>
    body {
      background-color: #07040D;
      color: #E2E8F0;
      font-family: 'Plus Jakarta Sans', sans-serif;
      overflow-x: hidden;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 8px;
    }
    ::-webkit-scrollbar-track {
      background: #07040D;
    }
    ::-webkit-scrollbar-thumb {
      background: #25124A;
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #7C3AED;
    }

    /* Glassmorphism */
    .glass-card {
      background: rgba(21, 13, 46, 0.7);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(139, 92, 246, 0.25);
    }
    
    .glass-card-hover {
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card-hover:hover {
      transform: translateY(-5px);
      border-color: rgba(0, 240, 255, 0.5);
      box-shadow: 0 10px 30px -10px rgba(124, 58, 237, 0.4);
    }

    .neon-text-purple {
      text-shadow: 0 0 12px rgba(168, 85, 247, 0.6);
    }
    .neon-text-blue {
      text-shadow: 0 0 12px rgba(0, 240, 255, 0.6);
    }
    
    .btn-gradient {
      background: linear-gradient(135deg, #7C3AED 0%, #2563EB 100%);
      transition: all 0.3s ease;
    }
    .btn-gradient:hover {
      background: linear-gradient(135deg, #9333EA 0%, #1D4ED8 100%);
      box-shadow: 0 0 20px rgba(124, 58, 237, 0.6);
      transform: scale(1.02);
    }

    .btn-cyan {
      background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%);
      transition: all 0.3s ease;
    }
    .btn-cyan:hover {
      box-shadow: 0 0 20px rgba(6, 182, 212, 0.6);
      transform: scale(1.02);
    }

    .toast-msg {
      animation: slideIn 0.3s forwards, fadeOut 0.5s 2.5s forwards;
    }
    @keyframes slideIn {
      from { transform: translateY(100%); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
    @keyframes fadeOut {
      from { opacity: 1; }
      to { opacity: 0; }
    }
  </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-brand-purple selection:text-white">

  <!-- BACKGROUND DECORATIONS -->
  <div class="fixed top-0 left-1/4 w-96 h-96 bg-brand-purple/20 rounded-full blur-[120px] pointer-events-none z-0"></div>
  <div class="fixed bottom-0 right-1/4 w-96 h-96 bg-brand-cyan/15 rounded-full blur-[120px] pointer-events-none z-0"></div>

  <!-- TOAST NOTIFICATION CONTAINER -->
  <div id="toast-container" class="fixed bottom-6 right-6 z-50 flex flex-col gap-3 pointer-events-none"></div>

  <!-- MAIN WRAPPER -->
  <div class="relative z-10 flex flex-col min-h-screen">
    
    <!-- HEADER -->
    <header class="sticky top-0 z-40 border-b border-brand-border/40 bg-brand-dark/80 backdrop-blur-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        <!-- Logo & Branding -->
        <div class="flex items-center gap-3 cursor-pointer" onclick="navigateTo('home')">
          <img id="site-logo-img" src="https://placehold.co/100x100/7C3AED/ffffff?text=NEXUS" alt="Logo" class="w-11 h-11 rounded-xl object-cover border border-brand-purpleGlow/40 shadow-lg shadow-brand-purple/30">
          <div>
            <h1 id="site-title-text" class="text-xl sm:text-2xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-white via-purple-200 to-brand-accent">
              NEXUS COURSES
            </h1>
            <p id="site-tagline-text" class="text-xs text-purple-300/70 font-medium">Elevate Your Skillsets</p>
          </div>
        </div>

        <!-- Right Action Nav -->
        <div class="flex items-center gap-3">
          <button onclick="navigateTo('home')" class="hidden md:flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-brand-surface/60 transition">
            <i class="fa-solid fa-house"></i> Home
          </button>
          <button id="admin-nav-btn" onclick="openAdminPortal()" class="flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold bg-brand-card hover:bg-brand-purple/30 border border-brand-purple/40 text-purple-200 transition shadow-md hover:shadow-brand-purple/20">
            <i class="fa-solid fa-user-shield text-brand-accent"></i> 
            <span id="admin-btn-label">Admin Panel</span>
          </button>
        </div>
      </div>
    </header>

    <!-- CONTENT VIEWS WRAPPER -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <!-- VIEW 1: HOMEPAGE -->
      <section id="view-home" class="view-section space-y-12">
        <!-- Hero Section -->
        <div class="text-center py-8 sm:py-12 relative">
          <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-brand-purpleGlow/30 bg-brand-purple/10 text-brand-accent text-xs font-semibold mb-4 animate-pulse-glow">
            <i class="fa-solid fa-sparkles"></i> Industry Verified Certification Courses
          </div>
          <h2 class="text-3xl sm:text-5xl lg:text-6xl font-black text-white tracking-tight leading-tight">
            Master High-Demand Tech & <br class="hidden sm:block">
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-purpleGlow via-brand-cyan to-white">Business Skills Today</span>
          </h2>
          <p class="mt-4 text-slate-400 max-w-2xl mx-auto text-sm sm:text-base">
            Gain instant access to top-tier, structured video masterclasses. Practical projects, expert support, and lifetime updates included with every plan.
          </p>
        </div>

        <!-- Course Cards Grid -->
        <div>
          <div class="flex items-center justify-between mb-8 border-b border-brand-border/30 pb-4">
            <h3 class="text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
              <i class="fa-solid fa-layer-group text-brand-purpleGlow"></i> Featured Course Plans
            </h3>
            <span id="course-count-badge" class="text-xs bg-brand-purple/20 text-brand-purpleGlow border border-brand-purple/30 px-3 py-1 rounded-full font-bold">10 Plans Available</span>
          </div>

          <!-- Vertical Layout on Mobile, Responsive Grid on Desktop -->
          <div id="course-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
            <!-- Dynamically populated course cards -->
          </div>
        </div>
      </section>

      <!-- VIEW 2: COURSE DEMO PAGE -->
      <section id="view-demo" class="view-section hidden space-y-8">
        <button onclick="navigateTo('home')" class="inline-flex items-center gap-2 text-sm text-purple-300 hover:text-white transition bg-brand-card/80 px-4 py-2 rounded-xl border border-brand-border/40">
          <i class="fa-solid fa-arrow-left"></i> Back to Courses
        </button>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <!-- Left Column: Details & Images -->
          <div class="lg:col-col-span-1 lg:col-span-7 space-y-6">
            <div class="glass-card p-6 rounded-2xl">
              <span id="demo-badge-videos" class="text-xs font-extrabold text-brand-accent bg-brand-cyan/10 border border-brand-cyan/30 px-3 py-1 rounded-full uppercase tracking-wider mb-3 inline-block">
                -- Videos Included
              </span>
              <h2 id="demo-title" class="text-2xl sm:text-4xl font-extrabold text-white mb-3">Course Title</h2>
              <p id="demo-description" class="text-slate-300 text-sm sm:text-base leading-relaxed">Detailed course overview will appear here.</p>
            </div>

            <!-- Preview Gallery -->
            <div class="glass-card p-6 rounded-2xl space-y-4">
              <h4 class="text-lg font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-images text-brand-purpleGlow"></i> Course Gallery & Screenshots
              </h4>
              <div class="rounded-xl overflow-hidden border border-brand-border/40 bg-black/40 aspect-video flex items-center justify-center">
                <img id="demo-main-image" src="" alt="Course Preview" class="w-full h-full object-cover">
              </div>
              <div id="demo-thumbs" class="grid grid-cols-4 gap-3">
                <!-- Additional gallery thumbs loaded dynamically -->
              </div>
            </div>

            <!-- Features list -->
            <div class="glass-card p-6 rounded-2xl space-y-4">
              <h4 class="text-lg font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-circle-check text-emerald-400"></i> What You'll Learn & Benefits
              </h4>
              <ul id="demo-features-list" class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm text-slate-300">
                <!-- Dynamic feature bullet points -->
              </ul>
            </div>
          </div>

          <!-- Right Column: Demo Instructions & Purchase Box -->
          <div class="lg:col-span-5 space-y-6">
            <!-- Telegram Demo Box -->
            <div class="glass-card p-6 rounded-2xl border-brand-cyan/30 space-y-5 text-center relative overflow-hidden">
              <div class="absolute -right-10 -top-10 w-32 h-32 bg-brand-cyan/20 rounded-full blur-2xl pointer-events-none"></div>
              
              <div class="w-16 h-16 bg-cyan-500/10 border border-cyan-400/30 text-cyan-400 rounded-2xl flex items-center justify-center mx-auto text-2xl shadow-lg">
                <i class="fa-brands fa-telegram"></i>
              </div>

              <div>
                <h3 class="text-xl font-bold text-white">Watch Free Course Demo</h3>
                <p class="text-xs text-slate-400 mt-1">Test drive sample lectures directly on Telegram before making your purchase decision.</p>
              </div>

              <a id="demo-tg-link" href="#" target="_blank" class="w-full py-3 px-6 rounded-xl font-bold text-white btn-cyan flex items-center justify-center gap-2 text-sm uppercase tracking-wide">
                <i class="fa-brands fa-telegram text-lg"></i> Watch Demo on Telegram
              </a>

              <!-- Step by Step Tutorial -->
              <div class="text-left bg-brand-dark/60 p-4 rounded-xl border border-brand-border/30 space-y-2">
                <h5 class="text-xs font-bold text-brand-accent uppercase tracking-wider flex items-center gap-1.5">
                  <i class="fa-solid fa-circle-info"></i> How to Watch the Demo
                </h5>
                <ol id="demo-tutorial-steps" class="text-xs text-slate-300 space-y-1.5 list-decimal list-inside pl-1">
                  <li>Click the "Watch Demo on Telegram" button above.</li>
                  <li>Open the official Telegram bot/channel link.</li>
                  <li>Follow the short prompt instructions in Telegram.</li>
                  <li>Access and watch the preliminary preview videos immediately.</li>
                </ol>
              </div>
            </div>

            <!-- Sticky Buy Now Box -->
            <div class="glass-card p-6 rounded-2xl border-brand-purpleGlow/40 space-y-5">
              <div class="flex items-center justify-between border-b border-brand-border/40 pb-4">
                <div>
                  <span class="text-xs text-slate-400 block">Total Investment</span>
                  <span id="demo-price-tag" class="text-3xl font-extrabold text-white neon-text-purple">₹0</span>
                </div>
                <span class="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs px-3 py-1 rounded-full font-semibold">Instant Access</span>
              </div>

              <button id="demo-buy-btn" onclick="" class="w-full py-4 rounded-xl font-extrabold text-white btn-gradient flex items-center justify-center gap-2 text-sm sm:text-base uppercase tracking-wider">
                <i class="fa-solid fa-bolt"></i> Buy Now — Unlock Premium Access
              </button>

              <div class="flex items-center justify-center gap-4 text-xs text-slate-400 pt-1">
                <span class="flex items-center gap-1"><i class="fa-solid fa-shield-halved text-emerald-400"></i> Secure Payment</span>
                <span class="flex items-center gap-1"><i class="fa-solid fa-clock text-brand-cyan"></i> Lifetime Validity</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- VIEW 3: SECURE PAYMENT PAGE -->
      <section id="view-payment" class="view-section hidden max-w-2xl mx-auto space-y-6">
        <button onclick="navigateTo('home')" class="inline-flex items-center gap-2 text-sm text-purple-300 hover:text-white transition bg-brand-card/80 px-4 py-2 rounded-xl border border-brand-border/40">
          <i class="fa-solid fa-arrow-left"></i> Cancel / Back
        </button>

        <div class="glass-card p-6 sm:p-8 rounded-2xl space-y-6 border-brand-purpleGlow/40 shadow-2xl">
          <!-- Heading -->
          <div class="text-center border-b border-brand-border/40 pb-5">
            <span class="inline-flex items-center gap-2 text-xs font-extrabold text-brand-accent bg-brand-purple/20 px-3 py-1 rounded-full border border-brand-purple/40 mb-2">
              <i class="fa-solid fa-lock"></i> SECURE UPI PAYMENT
            </span>
            <h2 class="text-2xl sm:text-3xl font-black text-white">UNLOCK NOW • COMPLETE ORDER</h2>
            <p class="text-xs sm:text-sm text-slate-400 mt-1">Scan QR code or copy UPI ID to transfer funds, then submit UTR details.</p>
          </div>

          <!-- Course & Amount Summary -->
          <div class="bg-brand-dark/80 p-4 rounded-xl border border-brand-border/40 flex items-center justify-between">
            <div>
              <span class="text-xs text-slate-400 block">Selected Course:</span>
              <h4 id="payment-course-title" class="text-base sm:text-lg font-bold text-white">Course Name</h4>
            </div>
            <div class="text-right">
              <span class="text-xs text-slate-400 block">Amount Payable:</span>
              <span id="payment-course-price" class="text-2xl font-black text-brand-accent">₹0</span>
            </div>
          </div>

          <!-- Dynamic QR Code & UPI Details -->
          <div class="flex flex-col items-center justify-center bg-brand-surface p-6 rounded-xl border border-brand-border/30 space-y-4">
            <div class="p-3 bg-white rounded-2xl shadow-xl border-2 border-brand-purpleGlow/50 relative group">
              <img id="payment-qr-img" src="" alt="UPI Payment QR" class="w-48 h-48 sm:w-56 sm:h-56 object-contain">
              <div class="absolute inset-0 bg-black/5 opacity-0 group-hover:opacity-100 transition rounded-xl flex items-center justify-center pointer-events-none"></div>
            </div>

            <!-- UPI ID copy field -->
            <div class="w-full max-w-sm space-y-1">
              <label class="text-xs text-slate-400 block text-center">Configured UPI ID:</label>
              <div class="flex items-center gap-2 bg-brand-dark px-3 py-2 rounded-xl border border-brand-border/50">
                <i class="fa-solid fa-wallet text-brand-purpleGlow text-sm"></i>
                <input id="payment-upi-id" type="text" readonly value="loading..." class="bg-transparent text-sm font-semibold text-white w-full outline-none">
                <button type="button" onclick="copyUPIId()" class="bg-brand-purple/30 hover:bg-brand-purple/60 text-xs text-brand-accent px-3 py-1.5 rounded-lg font-bold transition flex items-center gap-1 shrink-0">
                  <i class="fa-regular fa-copy"></i> Copy
                </button>
              </div>
            </div>

            <p id="payment-instructions-text" class="text-xs text-slate-400 text-center max-w-md">
              Pay the exact amount via Google Pay, PhonePe, Paytm or BHIM UPI to the ID above.
            </p>
          </div>

          <!-- UTR Submission Form -->
          <form id="payment-form" onsubmit="handlePaymentSubmit(event)" class="space-y-4 pt-2">
            <div>
              <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                12-Digit UTR / Transaction Reference Number <span class="text-rose-500">*</span>
              </label>
              <input id="payment-utr-input" type="text" maxlength="12" minlength="12" pattern="\d{12}" placeholder="e.g. 329182736412" required 
                class="w-full px-4 py-3 rounded-xl bg-brand-dark border border-brand-border/60 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-brand-accent focus:ring-1 focus:ring-brand-accent font-mono tracking-widest">
              <p class="text-[11px] text-slate-400 mt-1">Enter the 12-digit number found in your payment app transaction receipt.</p>
            </div>

            <!-- Optional Payment Screenshot Upload -->
            <div id="payment-screenshot-container">
              <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                Payment Screenshot (Optional / Recommended)
              </label>
              <div class="flex items-center gap-3">
                <input id="payment-screenshot-input" type="file" accept="image/png, image/jpeg, image/webp" onchange="handleScreenshotSelect(event)"
                  class="block w-full text-xs text-slate-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-purple/20 file:text-brand-purpleGlow hover:file:bg-brand-purple/40 cursor-pointer">
              </div>
              <!-- Preview thumbnail -->
              <div id="screenshot-preview-box" class="hidden mt-3 p-2 bg-brand-dark rounded-xl border border-brand-border/40 inline-flex items-center gap-3">
                <img id="screenshot-preview-img" src="" alt="Screenshot" class="w-12 h-12 object-cover rounded-lg">
                <div class="text-xs">
                  <p class="text-slate-200 font-medium">Screenshot attached</p>
                  <button type="button" onclick="removeScreenshot()" class="text-rose-400 hover:underline text-[11px]">Remove</button>
                </div>
              </div>
            </div>

            <button type="submit" class="w-full py-4 rounded-xl font-extrabold text-white btn-gradient flex items-center justify-center gap-2 text-sm uppercase tracking-wider shadow-lg">
              <i class="fa-solid fa-paper-plane"></i> SUBMIT PAYMENT DETAILS
            </button>
          </form>

          <!-- Awaiting Verification Modal/Notice (Hidden by default) -->
          <div id="payment-status-message" class="hidden p-6 bg-emerald-950/40 border border-emerald-500/40 rounded-2xl text-center space-y-3">
            <div class="w-12 h-12 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto text-xl">
              <i class="fa-solid fa-clock-rotate-left"></i>
            </div>
            <h4 class="text-lg font-bold text-white">Payment Details Submitted Successfully!</h4>
            <p class="text-xs text-emerald-200/80 leading-relaxed">
              "Your payment details have been submitted successfully. Your payment is currently awaiting manual verification by our administrators."
            </p>
            <div class="pt-2">
              <span id="submitted-order-id" class="text-xs font-mono bg-black/40 text-emerald-300 px-3 py-1 rounded-md border border-emerald-500/20">Order ID: --</span>
            </div>
            <button onclick="navigateTo('home')" class="mt-2 text-xs font-bold text-brand-accent hover:underline inline-block">Return to Homepage</button>
          </div>
        </div>
      </section>

      <!-- VIEW 4: ADMIN DASHBOARD & LOGIN -->
      <section id="view-admin" class="view-section hidden space-y-8">
        
        <!-- LOGIN MODAL / SCREEN (IF NOT AUTHENTICATED) -->
        <div id="admin-login-box" class="max-w-md mx-auto glass-card p-8 rounded-2xl border-brand-purpleGlow/50 shadow-2xl space-y-6">
          <div class="text-center space-y-2">
            <div class="w-14 h-14 bg-brand-purple/20 text-brand-purpleGlow rounded-2xl flex items-center justify-center mx-auto text-2xl border border-brand-purple/40">
              <i class="fa-solid fa-user-lock"></i>
            </div>
            <h2 class="text-2xl font-bold text-white">Admin Authentication</h2>
            <p class="text-xs text-slate-400">Enter administrator credentials to access management dashboard.</p>
          </div>

          <form onsubmit="handleAdminLogin(event)" class="space-y-4">
            <div>
              <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">Username</label>
              <input id="admin-user-input" type="text" placeholder="Username" required 
                class="w-full px-4 py-2.5 rounded-xl bg-brand-dark border border-brand-border/60 text-white text-sm focus:outline-none focus:border-brand-accent">
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">Password</label>
              <input id="admin-pass-input" type="password" placeholder="Password" required 
                class="w-full px-4 py-2.5 rounded-xl bg-brand-dark border border-brand-border/60 text-white text-sm focus:outline-none focus:border-brand-accent">
            </div>
            <button type="submit" class="w-full py-3 rounded-xl font-bold text-white btn-gradient text-sm uppercase tracking-wider shadow-lg">
              Login to Admin Panel
            </button>
          </form>
          <div class="text-center text-[11px] text-slate-500 border-t border-brand-border/30 pt-3">
            Initial Dev Auth: <code class="text-purple-300">arushdev</code> / <code class="text-purple-300">arush300</code>
          </div>
        </div>

        <!-- AUTHENTICATED ADMIN PANEL DASHBOARD -->
        <div id="admin-dashboard-box" class="hidden space-y-8">
          
          <!-- Top Bar & Navigation Tabs -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-card p-4 rounded-2xl">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-brand-purple/30 border border-brand-purpleGlow/40 flex items-center justify-center text-brand-accent font-bold">
                <i class="fa-solid fa-gauge-high"></i>
              </div>
              <div>
                <h2 class="text-lg font-extrabold text-white">Admin Control Center</h2>
                <p class="text-xs text-slate-400">Manage platform parameters, payments & courses persistent state</p>
              </div>
            </div>

            <div class="flex items-center gap-2">
              <button onclick="handleAdminLogout()" class="px-3 py-1.5 rounded-lg text-xs font-bold text-rose-300 bg-rose-500/10 border border-rose-500/30 hover:bg-rose-500/20 transition">
                <i class="fa-solid fa-right-from-bracket"></i> Logout
              </button>
            </div>
          </div>

          <!-- ADMIN NAVIGATION TABS -->
          <div class="flex items-center gap-2 border-b border-brand-border/40 overflow-x-auto pb-2">
            <button onclick="switchAdminTab('overview')" id="tab-btn-overview" class="admin-tab-btn px-4 py-2 rounded-xl text-xs font-bold text-white bg-brand-purple/40 border border-brand-purple/50 whitespace-nowrap">
              <i class="fa-solid fa-chart-pie mr-1.5"></i> Overview & Stats
            </button>
            <button onclick="switchAdminTab('orders')" id="tab-btn-orders" class="admin-tab-btn px-4 py-2 rounded-xl text-xs font-bold text-slate-400 hover:text-white hover:bg-brand-card whitespace-nowrap">
              <i class="fa-solid fa-receipt mr-1.5"></i> Payments & Orders <span id="admin-pending-badge" class="ml-1 px-1.5 py-0.5 rounded-full text-[10px] bg-amber-500 text-black font-extrabold">0</span>
            </button>
            <button onclick="switchAdminTab('courses')" id="tab-btn-courses" class="admin-tab-btn px-4 py-2 rounded-xl text-xs font-bold text-slate-400 hover:text-white hover:bg-brand-card whitespace-nowrap">
              <i class="fa-solid fa-book-open mr-1.5"></i> Course Plans CRUD
            </button>
            <button onclick="switchAdminTab('settings')" id="tab-btn-settings" class="admin-tab-btn px-4 py-2 rounded-xl text-xs font-bold text-slate-400 hover:text-white hover:bg-brand-card whitespace-nowrap">
              <i class="fa-solid fa-sliders mr-1.5"></i> Platform & UPI Settings
            </button>
          </div>

          <!-- TAB 1: OVERVIEW & STATS -->
          <div id="admin-tab-overview" class="admin-tab-content space-y-6">
            <!-- Analytics Cards -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div class="glass-card p-4 rounded-xl border-brand-purple/30">
                <span class="text-xs text-slate-400 block font-semibold">Total Revenue (Verified)</span>
                <span id="stat-revenue" class="text-2xl font-black text-emerald-400 neon-text-blue">₹0</span>
                <span class="text-[10px] text-slate-500 block mt-1">Excludes pending/rejected</span>
              </div>
              <div class="glass-card p-4 rounded-xl border-brand-purple/30">
                <span class="text-xs text-slate-400 block font-semibold">Total Website Visits</span>
                <span id="stat-visits" class="text-2xl font-black text-white">0</span>
                <span class="text-[10px] text-slate-500 block mt-1">Page impression counter</span>
              </div>
              <div class="glass-card p-4 rounded-xl border-brand-purple/30">
                <span class="text-xs text-slate-400 block font-semibold">Unique Visitors</span>
                <span id="stat-uniques" class="text-2xl font-black text-brand-accent">0</span>
                <span class="text-[10px] text-slate-500 block mt-1">Distinct user devices</span>
              </div>
              <div class="glass-card p-4 rounded-xl border-brand-purple/30">
                <span class="text-xs text-slate-400 block font-semibold">Pending Orders</span>
                <span id="stat-pending" class="text-2xl font-black text-amber-400">0</span>
                <span class="text-[10px] text-slate-500 block mt-1">Awaiting manual approval</span>
              </div>
            </div>

            <!-- Breakdown stats -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="glass-card p-4 rounded-xl flex items-center justify-between">
                <div>
                  <span class="text-xs text-slate-400">Approved Payments</span>
                  <p id="stat-approved" class="text-xl font-bold text-emerald-400">0</p>
                </div>
                <i class="fa-solid fa-circle-check text-emerald-400 text-2xl"></i>
              </div>
              <div class="glass-card p-4 rounded-xl flex items-center justify-between">
                <div>
                  <span class="text-xs text-slate-400">Rejected Payments</span>
                  <p id="stat-rejected" class="text-xl font-bold text-rose-400">0</p>
                </div>
                <i class="fa-solid fa-circle-xmark text-rose-400 text-2xl"></i>
              </div>
              <div class="glass-card p-4 rounded-xl flex items-center justify-between">
                <div>
                  <span class="text-xs text-slate-400">Active Course Plans</span>
                  <p id="stat-total-courses" class="text-xl font-bold text-brand-purpleGlow">10</p>
                </div>
                <i class="fa-solid fa-graduation-cap text-brand-purpleGlow text-2xl"></i>
              </div>
            </div>

            <!-- Activity Feed -->
            <div class="glass-card p-6 rounded-2xl space-y-4">
              <h3 class="text-sm font-bold text-white uppercase tracking-wider">Recent Activity & Submissions</h3>
              <div id="admin-recent-activity" class="space-y-3 text-xs">
                <!-- Populated dynamically -->
              </div>
            </div>
          </div>

          <!-- TAB 2: PAYMENTS & ORDERS MANAGEMENT -->
          <div id="admin-tab-orders" class="admin-tab-content hidden space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-bold text-white">Submitted Payment Verifications</h3>
              <button onclick="renderAdminOrders()" class="text-xs text-brand-accent hover:underline">
                <i class="fa-solid fa-rotate"></i> Refresh Table
              </button>
            </div>

            <div class="glass-card rounded-2xl overflow-hidden border-brand-border/40">
              <div class="overflow-x-auto">
                <table class="w-full text-left text-xs">
                  <thead class="bg-brand-dark/90 text-slate-400 border-b border-brand-border/40 uppercase tracking-wider font-semibold">
                    <tr>
                      <th class="p-4">Order ID & Date</th>
                      <th class="p-4">Course Plan</th>
                      <th class="p-4">Price</th>
                      <th class="p-4">Submitted UTR</th>
                      <th class="p-4">Screenshot</th>
                      <th class="p-4">Status</th>
                      <th class="p-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody id="orders-table-body" class="divide-y divide-brand-border/20 text-slate-300">
                    <!-- Populated dynamically -->
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- TAB 3: COURSE PLANS CRUD MANAGEMENT -->
          <div id="admin-tab-courses" class="admin-tab-content hidden space-y-6">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-lg font-bold text-white">Manage Course Plans</h3>
                <p class="text-xs text-slate-400">Add, edit, delete, or reorder courses dynamically without source code edits.</p>
              </div>
              <button onclick="openCourseModal(null)" class="px-4 py-2 rounded-xl text-xs font-bold text-white btn-gradient flex items-center gap-2">
                <i class="fa-solid fa-plus"></i> Add New Plan
              </button>
            </div>

            <div id="admin-courses-list" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <!-- Dynamically rendered admin course cards -->
            </div>
          </div>

          <!-- TAB 4: PLATFORM & UPI SETTINGS -->
          <div id="admin-tab-settings" class="admin-tab-content hidden space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              <!-- Payment & UPI Settings -->
              <div class="glass-card p-6 rounded-2xl space-y-4">
                <h3 class="text-base font-bold text-white border-b border-brand-border/30 pb-3 flex items-center gap-2">
                  <i class="fa-solid fa-qrcode text-brand-cyan"></i> UPI & Payment Gateway Configuration
                </h3>
                
                <form onsubmit="savePaymentSettings(event)" class="space-y-4">
                  <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">UPI ID (VPA)</label>
                    <input id="setting-upi-id" type="text" required class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white text-xs">
                  </div>
                  <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Account Display Name</label>
                    <input id="setting-upi-name" type="text" required class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white text-xs">
                  </div>
                  <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Payment Instructions</label>
                    <textarea id="setting-upi-instructions" rows="3" class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white text-xs"></textarea>
                  </div>
                  <div class="flex items-center gap-2">
                    <input id="setting-enable-screenshots" type="checkbox" class="rounded border-brand-border bg-brand-dark text-brand-purple focus:ring-0">
                    <label for="setting-enable-screenshots" class="text-xs text-slate-300">Enable Payment Screenshot Upload Field</label>
                  </div>
                  <button type="submit" class="px-4 py-2 rounded-xl text-xs font-bold text-white btn-cyan">
                    Save Payment Settings
                  </button>
                </form>
              </div>

              <!-- General Platform Settings -->
              <div class="glass-card p-6 rounded-2xl space-y-4">
                <h3 class="text-base font-bold text-white border-b border-brand-border/30 pb-3 flex items-center gap-2">
                  <i class="fa-solid fa-globe text-brand-purpleGlow"></i> Platform & Support Branding
                </h3>

                <form onsubmit="saveSiteSettings(event)" class="space-y-4">
                  <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Platform Name</label>
                    <input id="setting-site-title" type="text" required class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white text-xs">
                  </div>
                  <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Tagline / Subtitle</label>
                    <input id="setting-site-tagline" type="text" class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white text-xs">
                  </div>
                  <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Website Logo Image URL (ImgBB Supported)</label>
                    <input id="setting-site-logo" type="url" class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white text-xs">
                  </div>
                  <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Floating Telegram Support Link</label>
                    <input id="setting-tg-support" type="url" required class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white text-xs">
                  </div>
                  <button type="submit" class="px-4 py-2 rounded-xl text-xs font-bold text-white btn-gradient">
                    Save Branding Settings
                  </button>
                </form>
              </div>

              <!-- Admin Credentials Management -->
              <div class="glass-card p-6 rounded-2xl space-y-4 md:col-span-2">
                <h3 class="text-base font-bold text-white border-b border-brand-border/30 pb-3 flex items-center gap-2">
                  <i class="fa-solid fa-key text-amber-400"></i> Change Admin Credentials
                </h3>

                <form onsubmit="saveAdminSecurity(event)" class="grid grid-cols-1 sm:grid-cols-3 gap-4 items-end">
                  <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Admin Username</label>
                    <input id="setting-admin-username" type="text" required class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white text-xs">
                  </div>
                  <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">New Password</label>
                    <input id="setting-admin-password" type="password" required placeholder="Enter new password" class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white text-xs">
                  </div>
                  <div>
                    <button type="submit" class="w-full py-2 rounded-xl text-xs font-bold text-white bg-amber-600 hover:bg-amber-500 transition">
                      Update Security Credentials
                    </button>
                  </div>
                </form>
              </div>

            </div>
          </div>

        </div>
      </section>

    </main>

    <!-- FOOTER -->
    <footer class="border-t border-brand-border/30 bg-brand-dark/90 py-8 mt-12 text-center text-xs text-slate-500">
      <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p>© <span id="footer-year">2026</span> <span id="footer-site-name">NEXUS COURSES</span>. All rights reserved.</p>
        <p class="flex items-center gap-3">
          <span class="hover:text-slate-300 cursor-pointer" onclick="navigateTo('home')">Home</span> • 
          <span class="hover:text-slate-300 cursor-pointer" onclick="openAdminPortal()">Admin Login</span>
        </p>
      </div>
    </footer>

    <!-- FLOATING TELEGRAM SUPPORT BUTTON -->
    <a id="floating-tg-btn" href="https://t.me/" target="_blank" class="fixed bottom-6 right-6 z-40 w-14 h-14 bg-cyan-500 hover:bg-cyan-400 text-white rounded-full flex items-center justify-center text-2xl shadow-xl shadow-cyan-500/30 transition transform hover:scale-110">
      <i class="fa-brands fa-telegram"></i>
    </a>
  </div>

  <!-- COURSE EDIT/CREATE MODAL -->
  <div id="course-modal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="glass-card max-w-2xl w-full p-6 sm:p-8 rounded-2xl space-y-4 max-h-[90vh] overflow-y-auto border-brand-purpleGlow/50">
      <div class="flex items-center justify-between border-b border-brand-border/30 pb-3">
        <h3 id="course-modal-title" class="text-lg font-bold text-white">Add New Course Plan</h3>
        <button onclick="closeCourseModal()" class="text-slate-400 hover:text-white text-lg">&times;</button>
      </div>

      <form id="course-modal-form" onsubmit="saveCourseForm(event)" class="space-y-4 text-xs">
        <input type="hidden" id="course-form-id">
        
        <div>
          <label class="block font-semibold text-slate-300 mb-1">Course Title</label>
          <input id="course-form-title" type="text" required placeholder="e.g. Full Stack Web Development Mastery" class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white">
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block font-semibold text-slate-300 mb-1">Price (INR ₹)</label>
            <input id="course-form-price" type="number" required min="1" placeholder="199" class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white">
          </div>
          <div>
            <label class="block font-semibold text-slate-300 mb-1">Video Count</label>
            <input id="course-form-videos" type="number" required min="1" placeholder="35" class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white">
          </div>
        </div>

        <div>
          <label class="block font-semibold text-slate-300 mb-1">Short Description</label>
          <textarea id="course-form-desc" rows="3" required placeholder="Comprehensive description of what students will achieve..." class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white"></textarea>
        </div>

        <div>
          <label class="block font-semibold text-slate-300 mb-1">Thumbnail Image URL (ImgBB Supported)</label>
          <input id="course-form-thumb" type="url" required placeholder="https://i.ibb.co/..." class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white">
        </div>

        <div>
          <label class="block font-semibold text-slate-300 mb-1">Additional Gallery Image URLs (Comma separated)</label>
          <input id="course-form-gallery" type="text" placeholder="https://i.ibb.co/1, https://i.ibb.co/2" class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white">
        </div>

        <div>
          <label class="block font-semibold text-slate-300 mb-1">Telegram Demo Link / Bot URL</label>
          <input id="course-form-tg" type="url" required placeholder="https://t.me/your_demo_bot" class="w-full px-3 py-2 rounded-xl bg-brand-dark border border-brand-border/60 text-white">
        </div>

        <div class="flex items-center gap-2">
          <input id="course-form-active" type="checkbox" checked class="rounded bg-brand-dark border-brand-border text-brand-purple">
          <label for="course-form-active" class="text-slate-300 font-semibold">Enable Plan (Visible on Homepage)</label>
        </div>

        <div class="flex items-center justify-end gap-3 pt-3 border-t border-brand-border/30">
          <button type="button" onclick="closeCourseModal()" class="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 hover:text-white">Cancel</button>
          <button type="submit" class="px-5 py-2 rounded-xl text-white font-bold btn-gradient">Save Plan</button>
        </div>
      </form>
    </div>
  </div>

  <!-- SCREENSHOT PREVIEW MODAL -->
  <div id="screenshot-modal" class="fixed inset-0 z-50 bg-black/90 backdrop-blur-md hidden items-center justify-center p-4" onclick="closeScreenshotModal()">
    <div class="max-w-2xl w-full p-2 relative" onclick="event.stopPropagation()">
      <button onclick="closeScreenshotModal()" class="absolute -top-10 right-0 text-white text-2xl font-bold">&times; Close</button>
      <img id="screenshot-modal-img" src="" alt="Payment Proof" class="w-full h-auto max-h-[80vh] object-contain rounded-2xl border-2 border-brand-purpleGlow">
    </div>
  </div>


  <!-- JAVASCRIPT APPLICATION LOGIC -->
  <script>
    /* ==========================================================================
       1. DEFAULT SEED DATA & INITIALIZATION
       ========================================================================== */
    
    const INITIAL_COURSES = [
      {
        id: "plan-01",
        title: "Full Stack Web Development Pro",
        desc: "Master HTML5, CSS3, Tailwind, React, Node.js, and MongoDB from scratch with 10 real-world deployment projects.",
        videos: 45,
        price: 199,
        thumb: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=600&q=80",
        gallery: ["https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=600&q=80"],
        tgLink: "https://t.me/NexusDemoBot",
        active: true,
        order: 1
      },
      {
        id: "plan-02",
        title: "AI & Prompt Engineering Masterclass",
        desc: "Learn ChatGPT 4o, Claude 3.5, Midjourney, and Custom LLM API integrations to automate workflow tasks.",
        videos: 30,
        price: 249,
        thumb: "https://images.unsplash.com/photo-1677442136019-21780efad99a?auto=format&fit=crop&w=600&q=80",
        gallery: ["https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=600&q=80"],
        tgLink: "https://t.me/NexusDemoBot",
        active: true,
        order: 2
      },
      {
        id: "plan-03",
        title: "Ethical Hacking & Cyber Security",
        desc: "Complete penetration testing, network sniffing, Wireshark, Metasploit, and bug bounty hunting blueprint.",
        videos: 50,
        price: 299,
        thumb: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=600&q=80",
        gallery: ["https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=600&q=80"],
        tgLink: "https://t.me/NexusDemoBot",
        active: true,
        order: 3
      },
      {
        id: "plan-04",
        title: "Crypto, Forex & Stock Trading Bootcamp",
        desc: "Technical analysis, price action strategies, candlestick patterns, risk management, and live market breakdown.",
        videos: 35,
        price: 199,
        thumb: "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=600&q=80",
        gallery: ["https://images.unsplash.com/photo-1642543492481-44e81e3914a7?auto=format&fit=crop&w=600&q=80"],
        tgLink: "https://t.me/NexusDemoBot",
        active: true,
        order: 4
      },
      {
        id: "plan-05",
        title: "Android & iOS Flutter App Development",
        desc: "Build cross-platform mobile apps with Dart, Flutter, Firebase authentication, and Play Store publishing.",
        videos: 40,
        price: 249,
        thumb: "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=600&q=80",
        gallery: ["https://images.unsplash.com/photo-1551650975-87deedd944c3?auto=format&fit=crop&w=600&q=80"],
        tgLink: "https://t.me/NexusDemoBot",
        active: true,
        order: 5
      },
      {
        id: "plan-06",
        title: "Cloud Computing & AWS Architecture",
        desc: "Prepare for AWS Certified Solutions Architect exam. EC2, S3, Lambda, Docker, Kubernetes, and DevOps pipelines.",
        videos: 38,
        price: 299,
        thumb: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&q=80",
        gallery: ["https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=600&q=80"],
        tgLink: "https://t.me/NexusDemoBot",
        active: true,
        order: 6
      },
      {
        id: "plan-07",
        title: "Digital Marketing & Traffic Mastery",
        desc: "Facebook Ads, Google PPC, SEO optimization, email copywriting, and high-converting sales funnels.",
        videos: 28,
        price: 149,
        thumb: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=600&q=80",
        gallery: ["https://images.unsplash.com/photo-1533750349088-cd871a92f312?auto=format&fit=crop&w=600&q=80"],
        tgLink: "https://t.me/NexusDemoBot",
        active: true,
        order: 7
      },
      {
        id: "plan-08",
        title: "UI/UX Design with Figma Pro",
        desc: "Master wireframing, interactive prototyping, design systems, typography, and client handoff workflows.",
        videos: 32,
        price: 199,
        thumb: "https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?auto=format&fit=crop&w=600&q=80",
        gallery: ["https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=600&q=80"],
        tgLink: "https://t.me/NexusDemoBot",
        active: true,
        order: 8
      },
      {
        id: "plan-09",
        title: "Data Science & Machine Learning with Python",
        desc: "Pandas, NumPy, Matplotlib, Scikit-Learn, Deep Learning with TensorFlow, and data analysis pipelines.",
        videos: 48,
        price: 299,
        thumb: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=600&q=80",
        gallery: ["https://images.unsplash.com/photo-1527474305487-b87b222841cc?auto=format&fit=crop&w=600&q=80"],
        tgLink: "https://t.me/NexusDemoBot",
        active: true,
        order: 9
      },
      {
        id: "plan-10",
        title: "Python Automation & Web Scraping",
        desc: "Automate repetitive tasks, build Selenium bots, scrape dynamic sites with BeautifulSoup, and construct REST APIs.",
        videos: 25,
        price: 149,
        thumb: "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?auto=format&fit=crop&w=600&q=80",
        gallery: ["https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=600&q=80"],
        tgLink: "https://t.me/NexusDemoBot",
        active: true,
        order: 10
      }
    ];

    const DEFAULT_SETTINGS = {
      siteTitle: "NEXUS COURSES",
      siteTagline: "Elevate Your Skillsets",
      siteLogo: "https://placehold.co/100x100/7C3AED/ffffff?text=NEXUS",
      telegramSupport: "https://t.me/NexusSupportAdmin",
      upiId: "nexuspay@upi",
      upiName: "NEXUS ENTERPRISES",
      paymentInstructions: "Pay the exact amount via GPay, PhonePe, Paytm, or BHIM. Enter your 12-digit UTR below for manual verification.",
      enableScreenshots: true,
      adminUser: "arushdev",
      adminPassHash: "arush300" // Stored simply for demo persistence
    };

    /* State Variables */
    let courses = [];
    let settings = {};
    let orders = [];
    let analytics = { visits: 0, uniques: 0 };
    let currentSelectedCourse = null;
    let selectedScreenshotBase64 = null;
    let isAdminLoggedIn = false;

    /* Initialize Application on DOM Load */
    window.addEventListener('DOMContentLoaded', () => {
      loadStorageData();
      trackAnalytics();
      applyBranding();
      renderCoursesHomepage();
      
      // Auto-update footer year
      document.getElementById('footer-year').textContent = new Date().getFullYear();
    });

    /* ==========================================================================
       2. LOCAL STORAGE PERSISTENCE HELPERS
       ========================================================================== */
    function loadStorageData() {
      // Courses
      const savedCourses = localStorage.getItem('nexus_courses');
      courses = savedCourses ? JSON.parse(savedCourses) : INITIAL_COURSES;

      // Settings
      const savedSettings = localStorage.getItem('nexus_settings');
      settings = savedSettings ? JSON.parse(savedSettings) : DEFAULT_SETTINGS;

      // Orders
      const savedOrders = localStorage.getItem('nexus_orders');
      orders = savedOrders ? JSON.parse(savedOrders) : [];

      // Analytics
      const savedAnalytics = localStorage.getItem('nexus_analytics');
      analytics = savedAnalytics ? JSON.parse(savedAnalytics) : { visits: 0, uniques: 0 };

      // Auth state
      isAdminLoggedIn = sessionStorage.getItem('nexus_admin_auth') === 'true';
    }

    function saveCoursesToStorage() {
      localStorage.setItem('nexus_courses', JSON.stringify(courses));
    }

    function saveSettingsToStorage() {
      localStorage.setItem('nexus_settings', JSON.stringify(settings));
    }

    function saveOrdersToStorage() {
      localStorage.setItem('nexus_orders', JSON.stringify(orders));
    }

    function trackAnalytics() {
      analytics.visits += 1;
      
      // Unique user tracking via simple localStorage token
      if (!localStorage.getItem('nexus_visitor_token')) {
        localStorage.setItem('nexus_visitor_token', 'visitor_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5));
        analytics.uniques += 1;
      }
      
      localStorage.setItem('nexus_analytics', JSON.stringify(analytics));
    }

    function applyBranding() {
      document.getElementById('site-title-text').textContent = settings.siteTitle;
      document.getElementById('footer-site-name').textContent = settings.siteTitle;
      document.getElementById('site-tagline-text').textContent = settings.siteTagline;
      document.getElementById('site-logo-img').src = settings.siteLogo;
      document.getElementById('floating-tg-btn').href = settings.telegramSupport;
    }

    /* ==========================================================================
       3. NAVIGATION & VIEW SWITCHING
       ========================================================================== */
    function navigateTo(viewId) {
      document.querySelectorAll('.view-section').forEach(sec => sec.classList.add('hidden'));
      const target = document.getElementById('view-' + viewId);
      if (target) {
        target.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }

    function openAdminPortal() {
      navigateTo('admin');
      if (isAdminLoggedIn) {
        document.getElementById('admin-login-box').classList.add('hidden');
        document.getElementById('admin-dashboard-box').classList.remove('hidden');
        renderAdminDashboard();
      } else {
        document.getElementById('admin-login-box').classList.remove('hidden');
        document.getElementById('admin-dashboard-box').classList.add('hidden');
      }
    }

    /* ==========================================================================
       4. HOMEPAGE & DEMO PAGE RENDERING
       ========================================================================== */
    function renderCoursesHomepage() {
      const container = document.getElementById('course-grid');
      container.innerHTML = '';

      const activeCourses = courses.filter(c => c.active);
      document.getElementById('course-count-badge').textContent = `${activeCourses.length} Plans Available`;

      if (activeCourses.length === 0) {
        container.innerHTML = `<div class="col-span-full text-center py-12 text-slate-400">No active course plans available right now.</div>`;
        return;
      }

      activeCourses.forEach(plan => {
        const card = document.createElement('div');
        card.className = "glass-card glass-card-hover rounded-2xl overflow-hidden flex flex-col justify-between border-brand-border/30";
        card.innerHTML = `
          <div>
            <div class="relative aspect-video overflow-hidden bg-black/50">
              <img src="${plan.thumb}" alt="${plan.title}" class="w-full h-full object-cover transition transform hover:scale-105 duration-500" onerror="this.src='https://placehold.co/600x400/150D2E/ffffff?text=Course+Preview'">
              <span class="absolute top-3 right-3 bg-brand-dark/90 backdrop-blur-md border border-brand-purpleGlow/40 text-brand-accent text-[11px] font-bold px-2.5 py-1 rounded-lg">
                <i class="fa-solid fa-play-circle text-brand-purpleGlow mr-1"></i> ${plan.videos} Videos
              </span>
            </div>

            <div class="p-5 sm:p-6 space-y-3">
              <h3 class="text-lg font-bold text-white leading-snug line-clamp-2 hover:text-brand-purpleGlow transition">
                ${plan.title}
              </h3>
              <p class="text-xs text-slate-300 line-clamp-3 leading-relaxed">
                ${plan.desc}
              </p>
            </div>
          </div>

          <div class="p-5 sm:p-6 pt-0 space-y-3 border-t border-brand-border/20 mt-2">
            <div class="flex items-center justify-between pt-3">
              <span class="text-xs text-slate-400 font-medium">One-Time Fee</span>
              <span class="text-xl font-extrabold text-white neon-text-purple">₹${plan.price}</span>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <button onclick="openCourseDemo('${plan.id}')" class="py-2.5 px-3 rounded-xl text-xs font-bold text-cyan-300 bg-cyan-500/10 border border-cyan-500/30 hover:bg-cyan-500/20 transition flex items-center justify-center gap-1.5">
                <i class="fa-solid fa-eye"></i> View Demo
              </button>
              <button onclick="openPaymentPage('${plan.id}')" class="py-2.5 px-3 rounded-xl text-xs font-bold text-white btn-gradient flex items-center justify-center gap-1.5">
                <i class="fa-solid fa-cart-shopping"></i> Buy Now — ₹${plan.price}
              </button>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
    }

    function openCourseDemo(courseId) {
      const plan = courses.find(c => c.id === courseId);
      if (!plan) return;

      currentSelectedCourse = plan;

      document.getElementById('demo-title').textContent = plan.title;
      document.getElementById('demo-description').textContent = plan.desc;
      document.getElementById('demo-badge-videos').textContent = `${plan.videos} HD Videos Included`;
      document.getElementById('demo-price-tag').textContent = `₹${plan.price}`;
      document.getElementById('demo-main-image').src = plan.thumb;
      document.getElementById('demo-tg-link').href = plan.tgLink;

      // Render thumbs
      const thumbsBox = document.getElementById('demo-thumbs');
      thumbsBox.innerHTML = '';
      const gallery = [plan.thumb, ...(plan.gallery || [])];
      gallery.forEach((imgUrl, idx) => {
        const thumb = document.createElement('img');
        thumb.src = imgUrl;
        thumb.className = `w-full h-14 object-cover rounded-lg border cursor-pointer ${idx === 0 ? 'border-brand-accent' : 'border-brand-border/40'}`;
        thumb.onclick = () => {
          document.getElementById('demo-main-image').src = imgUrl;
          document.querySelectorAll('#demo-thumbs img').forEach(t => t.classList.replace('border-brand-accent', 'border-brand-border/40'));
          thumb.classList.replace('border-brand-border/40', 'border-brand-accent');
        };
        thumbsBox.appendChild(thumb);
      });

      // Render dynamic bullet highlights
      const featuresBox = document.getElementById('demo-features-list');
      featuresBox.innerHTML = `
        <li class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-400"></i> Lifetime unlimited access</li>
        <li class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-400"></i> Downloadable source codes & assets</li>
        <li class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-400"></i> ${plan.videos} Video modules in 1080p</li>
        <li class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-400"></i> Direct mentor assistance in Telegram</li>
      `;

      // Set Buy Now click
      document.getElementById('demo-buy-btn').onclick = () => openPaymentPage(plan.id);

      navigateTo('demo');
    }

    /* ==========================================================================
       5. PAYMENT & UTR SUBMISSION LOGIC
       ========================================================================== */
    function openPaymentPage(courseId) {
      const plan = courses.find(c => c.id === courseId);
      if (!plan) return;

      currentSelectedCourse = plan;
      selectedScreenshotBase64 = null;

      // Populate UI details
      document.getElementById('payment-course-title').textContent = plan.title;
      document.getElementById('payment-course-price').textContent = `₹${plan.price}`;
      document.getElementById('payment-upi-id').value = settings.upiId;
      document.getElementById('payment-instructions-text').textContent = settings.paymentInstructions;

      // Handle Screenshot option toggle
      const screenshotContainer = document.getElementById('payment-screenshot-container');
      if (settings.enableScreenshots) {
        screenshotContainer.classList.remove('hidden');
      } else {
        screenshotContainer.classList.add('hidden');
      }

      // Generate Live Dynamic UPI QR Code URL
      // Format: upi://pay?pa=UPI_ID&pn=NAME&am=AMOUNT&cu=INR
      const upiUrl = `upi://pay?pa=${encodeURIComponent(settings.upiId)}&pn=${encodeURIComponent(settings.upiName)}&am=${plan.price}&cu=INR`;
      const qrApiUrl = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(upiUrl)}`;
      document.getElementById('payment-qr-img').src = qrApiUrl;

      // Reset Form State
      document.getElementById('payment-form').reset();
      document.getElementById('payment-form').classList.remove('hidden');
      document.getElementById('payment-status-message').classList.add('hidden');
      removeScreenshot();

      navigateTo('payment');
    }

    function copyUPIId() {
      const upiInput = document.getElementById('payment-upi-id');
      upiInput.select();
      document.execCommand('copy');
      showToast('UPI ID copied to clipboard!');
    }

    function handleScreenshotSelect(e) {
      const file = e.target.files[0];
      if (!file) return;

      if (file.size > 5 * 1024 * 1024) {
        showToast('Image file must be smaller than 5MB', 'error');
        e.target.value = '';
        return;
      }

      const reader = new FileReader();
      reader.onload = function(evt) {
        selectedScreenshotBase64 = evt.target.result;
        document.getElementById('screenshot-preview-img').src = selectedScreenshotBase64;
        document.getElementById('screenshot-preview-box').classList.remove('hidden');
      };
      reader.readAsDataURL(file);
    }

    function removeScreenshot() {
      selectedScreenshotBase64 = null;
      document.getElementById('payment-screenshot-input').value = '';
      document.getElementById('screenshot-preview-box').classList.add('hidden');
    }

    function handlePaymentSubmit(e) {
      e.preventDefault();

      const utr = document.getElementById('payment-utr-input').value.trim();

      if (!/^\d{12}$/.test(utr)) {
        showToast('Please enter a valid 12-digit numeric UTR number', 'error');
        return;
      }

      // Check duplicate UTR
      const duplicate = orders.find(o => o.utr === utr);
      if (duplicate) {
        showToast('This UTR number has already been submitted previously', 'error');
        return;
      }

      const newOrder = {
        id: 'ORD-' + Math.floor(100000 + Math.random() * 900000),
        courseId: currentSelectedCourse.id,
        courseTitle: currentSelectedCourse.title,
        price: currentSelectedCourse.price,
        utr: utr,
        screenshot: selectedScreenshotBase64,
        date: new Date().toLocaleString(),
        status: 'Pending' // Pending, Approved, Rejected
      };

      orders.unshift(newOrder);
      saveOrdersToStorage();

      // Update Form View
      document.getElementById('payment-form').classList.add('hidden');
      document.getElementById('submitted-order-id').textContent = `Order Reference: ${newOrder.id}`;
      document.getElementById('payment-status-message').classList.remove('hidden');

      showToast('Payment details submitted successfully!');
    }

    /* ==========================================================================
       6. ADMIN PANEL DASHBOARD LOGIC & AUTHENTICATION
       ========================================================================== */
    function handleAdminLogin(e) {
      e.preventDefault();
      const user = document.getElementById('admin-user-input').value.trim();
      const pass = document.getElementById('admin-pass-input').value.trim();

      if (user === settings.adminUser && pass === settings.adminPassHash) {
        isAdminLoggedIn = true;
        sessionStorage.setItem('nexus_admin_auth', 'true');
        showToast('Logged in as Administrator');
        openAdminPortal();
      } else {
        showToast('Invalid Username or Password', 'error');
      }
    }

    function handleAdminLogout() {
      isAdminLoggedIn = false;
      sessionStorage.removeItem('nexus_admin_auth');
      showToast('Logged out successfully');
      openAdminPortal();
    }

    function switchAdminTab(tabName) {
      document.querySelectorAll('.admin-tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.admin-tab-btn').forEach(btn => {
        btn.classList.remove('bg-brand-purple/40', 'border-brand-purple/50', 'text-white');
        btn.classList.add('text-slate-400');
      });

      const activeContent = document.getElementById(`admin-tab-${tabName}`);
      const activeBtn = document.getElementById(`tab-btn-${tabName}`);

      if (activeContent && activeBtn) {
        activeContent.classList.remove('hidden');
        activeBtn.classList.add('bg-brand-purple/40', 'border-brand-purple/50', 'text-white');
      }
    }

    function renderAdminDashboard() {
      // 1. STATS OVERVIEW
      const approvedOrders = orders.filter(o => o.status === 'Approved');
      const pendingOrders = orders.filter(o => o.status === 'Pending');
      const rejectedOrders = orders.filter(o => o.status === 'Rejected');

      const verifiedRevenue = approvedOrders.reduce((acc, curr) => acc + Number(curr.price), 0);

      document.getElementById('stat-revenue').textContent = `₹${verifiedRevenue}`;
      document.getElementById('stat-visits').textContent = analytics.visits;
      document.getElementById('stat-uniques').textContent = analytics.uniques;
      document.getElementById('stat-pending').textContent = pendingOrders.length;
      document.getElementById('admin-pending-badge').textContent = pendingOrders.length;
      document.getElementById('stat-approved').textContent = approvedOrders.length;
      document.getElementById('stat-rejected').textContent = rejectedOrders.length;
      document.getElementById('stat-total-courses').textContent = courses.length;

      // Activity Feed
      const feedBox = document.getElementById('admin-recent-activity');
      feedBox.innerHTML = '';
      if (orders.length === 0) {
        feedBox.innerHTML = `<p class="text-slate-500 italic">No activity recorded yet.</p>`;
      } else {
        orders.slice(0, 5).forEach(o => {
          const item = document.createElement('div');
          item.className = "flex items-center justify-between p-3 rounded-xl bg-brand-dark/50 border border-brand-border/20";
          item.innerHTML = `
            <div>
              <span class="font-bold text-white">${o.courseTitle}</span>
              <p class="text-[11px] text-slate-400">UTR: ${o.utr} • ${o.date}</p>
            </div>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold ${
              o.status === 'Approved' ? 'bg-emerald-500/20 text-emerald-400' :
              o.status === 'Rejected' ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'
            }">${o.status}</span>
          `;
          feedBox.appendChild(item);
        });
      }

      // 2. ORDERS TABLE
      renderAdminOrders();

      // 3. COURSES MANAGEMENT LIST
      renderAdminCourses();

      // 4. POPULATE SETTINGS FIELDS
      document.getElementById('setting-upi-id').value = settings.upiId;
      document.getElementById('setting-upi-name').value = settings.upiName;
      document.getElementById('setting-upi-instructions').value = settings.paymentInstructions;
      document.getElementById('setting-enable-screenshots').checked = settings.enableScreenshots;

      document.getElementById('setting-site-title').value = settings.siteTitle;
      document.getElementById('setting-site-tagline').value = settings.siteTagline;
      document.getElementById('setting-site-logo').value = settings.siteLogo;
      document.getElementById('setting-tg-support').value = settings.telegramSupport;

      document.getElementById('setting-admin-username').value = settings.adminUser;
      document.getElementById('setting-admin-password').value = '';
    }

    /* Admin Orders Management */
    function renderAdminOrders() {
      const tbody = document.getElementById('orders-table-body');
      tbody.innerHTML = '';

      if (orders.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="p-6 text-center text-slate-500">No payment submissions received yet.</td></tr>`;
        return;
      }

      orders.forEach(o => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-brand-purple/10 transition";
        tr.innerHTML = `
          <td class="p-4">
            <span class="font-mono font-bold text-brand-accent block">${o.id}</span>
            <span class="text-[10px] text-slate-400">${o.date}</span>
          </td>
          <td class="p-4 font-semibold text-white">${o.courseTitle}</td>
          <td class="p-4 font-bold text-emerald-400">₹${o.price}</td>
          <td class="p-4 font-mono text-slate-200">${o.utr}</td>
          <td class="p-4">
            ${o.screenshot ? 
              `<button onclick="viewScreenshot('${o.id}')" class="text-xs text-brand-cyan hover:underline flex items-center gap-1">
                <i class="fa-solid fa-image"></i> View Proof
               </button>` : `<span class="text-slate-600 text-[11px]">None</span>`}
          </td>
          <td class="p-4">
            <span class="px-2.5 py-1 rounded-full text-[10px] font-extrabold ${
              o.status === 'Approved' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
              o.status === 'Rejected' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
            }">${o.status}</span>
          </td>
          <td class="p-4 text-right space-x-1">
            ${o.status === 'Pending' ? `
              <button onclick="updateOrderStatus('${o.id}', 'Approved')" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[11px] font-bold transition">Approve</button>
              <button onclick="updateOrderStatus('${o.id}', 'Rejected')" class="px-2.5 py-1 bg-rose-600 hover:bg-rose-500 text-white rounded text-[11px] font-bold transition">Reject</button>
            ` : `<button onclick="updateOrderStatus('${o.id}', 'Pending')" class="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[10px]">Reset</button>`}
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function updateOrderStatus(orderId, newStatus) {
      const order = orders.find(o => o.id === orderId);
      if (order) {
        order.status = newStatus;
        saveOrdersToStorage();
        renderAdminDashboard();
        showToast(`Order ${orderId} marked as ${newStatus}`);
      }
    }

    function viewScreenshot(orderId) {
      const order = orders.find(o => o.id === orderId);
      if (order && order.screenshot) {
        document.getElementById('screenshot-modal-img').src = order.screenshot;
        document.getElementById('screenshot-modal').classList.remove('hidden');
        document.getElementById('screenshot-modal').classList.add('flex');
      }
    }

    function closeScreenshotModal() {
      document.getElementById('screenshot-modal').classList.add('hidden');
      document.getElementById('screenshot-modal').classList.remove('flex');
    }

    /* Admin Course Plans CRUD */
    function renderAdminCourses() {
      const container = document.getElementById('admin-courses-list');
      container.innerHTML = '';

      courses.forEach(plan => {
        const item = document.createElement('div');
        item.className = `glass-card p-4 rounded-xl border flex flex-col justify-between ${plan.active ? 'border-brand-border/40' : 'border-rose-900/40 opacity-60'}`;
        item.innerHTML = `
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-mono text-brand-accent">ID: ${plan.id}</span>
              <span class="text-[10px] px-2 py-0.5 rounded ${plan.active ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'} font-bold">
                ${plan.active ? 'Enabled' : 'Disabled'}
              </span>
            </div>
            <h4 class="font-bold text-white text-sm line-clamp-1">${plan.title}</h4>
            <p class="text-xs text-emerald-400 font-extrabold">Price: ₹${plan.price} | Videos: ${plan.videos}</p>
          </div>

          <div class="flex items-center justify-between border-t border-brand-border/20 pt-3 mt-3">
            <button onclick="toggleCourseActive('${plan.id}')" class="text-xs ${plan.active ? 'text-amber-400' : 'text-emerald-400'} hover:underline">
              ${plan.active ? 'Disable' : 'Enable'}
            </button>
            <div class="space-x-2">
              <button onclick="openCourseModal('${plan.id}')" class="px-2.5 py-1 bg-brand-purple/40 text-purple-200 hover:bg-brand-purple rounded text-xs">Edit</button>
              <button onclick="deleteCourse('${plan.id}')" class="px-2.5 py-1 bg-rose-500/20 text-rose-300 hover:bg-rose-500/40 rounded text-xs">Delete</button>
            </div>
          </div>
        `;
        container.appendChild(item);
      });
    }

    function toggleCourseActive(id) {
      const plan = courses.find(c => c.id === id);
      if (plan) {
        plan.active = !plan.active;
        saveCoursesToStorage();
        renderAdminCourses();
        renderCoursesHomepage();
        showToast(`Course status updated`);
      }
    }

    function deleteCourse(id) {
      if (confirm('Are you sure you want to permanently delete this course plan?')) {
        courses = courses.filter(c => c.id !== id);
        saveCoursesToStorage();
        renderAdminCourses();
        renderCoursesHomepage();
        showToast('Course plan deleted');
      }
    }

    /* Course Modal Handlers */
    function openCourseModal(courseId = null) {
      const modal = document.getElementById('course-modal');
      const form = document.getElementById('course-modal-form');
      
      if (courseId) {
        const plan = courses.find(c => c.id === courseId);
        document.getElementById('course-modal-title').textContent = 'Edit Course Plan';
        document.getElementById('course-form-id').value = plan.id;
        document.getElementById('course-form-title').value = plan.title;
        document.getElementById('course-form-price').value = plan.price;
        document.getElementById('course-form-videos').value = plan.videos;
        document.getElementById('course-form-desc').value = plan.desc;
        document.getElementById('course-form-thumb').value = plan.thumb;
        document.getElementById('course-form-gallery').value = (plan.gallery || []).join(', ');
        document.getElementById('course-form-tg').value = plan.tgLink;
        document.getElementById('course-form-active').checked = plan.active;
      } else {
        document.getElementById('course-modal-title').textContent = 'Add New Course Plan';
        form.reset();
        document.getElementById('course-form-id').value = '';
        document.getElementById('course-form-active').checked = true;
      }

      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }

    function closeCourseModal() {
      const modal = document.getElementById('course-modal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }

    function saveCourseForm(e) {
      e.preventDefault();

      const id = document.getElementById('course-form-id').value;
      const title = document.getElementById('course-form-title').value.trim();
      const price = Number(document.getElementById('course-form-price').value);
      const videos = Number(document.getElementById('course-form-videos').value);
      const desc = document.getElementById('course-form-desc').value.trim();
      const thumb = document.getElementById('course-form-thumb').value.trim();
      const galleryRaw = document.getElementById('course-form-gallery').value.trim();
      const tgLink = document.getElementById('course-form-tg').value.trim();
      const active = document.getElementById('course-form-active').checked;

      const gallery = galleryRaw ? galleryRaw.split(',').map(s => s.trim()) : [];

      if (id) {
        // Edit
        const plan = courses.find(c => c.id === id);
        if (plan) {
          plan.title = title;
          plan.price = price;
          plan.videos = videos;
          plan.desc = desc;
          plan.thumb = thumb;
          plan.gallery = gallery;
          plan.tgLink = tgLink;
          plan.active = active;
        }
      } else {
        // Create
        const newPlan = {
          id: 'plan-' + Date.now(),
          title,
          price,
          videos,
          desc,
          thumb,
          gallery,
          tgLink,
          active,
          order: courses.length + 1
        };
        courses.push(newPlan);
      }

      saveCoursesToStorage();
      renderCoursesHomepage();
      renderAdminCourses();
      closeCourseModal();
      showToast('Course plan saved successfully');
    }

    /* Admin Settings Forms */
    function savePaymentSettings(e) {
      e.preventDefault();
      settings.upiId = document.getElementById('setting-upi-id').value.trim();
      settings.upiName = document.getElementById('setting-upi-name').value.trim();
      settings.paymentInstructions = document.getElementById('setting-upi-instructions').value.trim();
      settings.enableScreenshots = document.getElementById('setting-enable-screenshots').checked;

      saveSettingsToStorage();
      showToast('Payment settings saved');
    }

    function saveSiteSettings(e) {
      e.preventDefault();
      settings.siteTitle = document.getElementById('setting-site-title').value.trim();
      settings.siteTagline = document.getElementById('setting-site-tagline').value.trim();
      settings.siteLogo = document.getElementById('setting-site-logo').value.trim();
      settings.telegramSupport = document.getElementById('setting-tg-support').value.trim();

      saveSettingsToStorage();
      applyBranding();
      showToast('Site branding updated');
    }

    function saveAdminSecurity(e) {
      e.preventDefault();
      const newUsername = document.getElementById('setting-admin-username').value.trim();
      const newPassword = document.getElementById('setting-admin-password').value.trim();

      settings.adminUser = newUsername;
      if (newPassword) {
        settings.adminPassHash = newPassword;
      }

      saveSettingsToStorage();
      showToast('Admin security credentials updated successfully!');
    }

    /* ==========================================================================
       7. TOAST NOTIFICATIONS HELPER
       ========================================================================== */
    function showToast(message, type = 'success') {
      const container = document.getElementById('toast-container');
      const toast = document.createElement('div');
      
      const isError = type === 'error';
      toast.className = `toast-msg flex items-center gap-3 px-4 py-3 rounded-xl shadow-2xl text-xs font-bold border pointer-events-auto ${
        isError ? 'bg-rose-950 text-rose-200 border-rose-500/50' : 'bg-brand-surface text-brand-accent border-brand-purpleGlow/50'
      }`;

      toast.innerHTML = `
        <i class="fa-solid ${isError ? 'fa-circle-exclamation text-rose-400' : 'fa-circle-check text-emerald-400'} text-base"></i>
        <span>${message}</span>
      `;

      container.appendChild(toast);

      setTimeout(() => {
        toast.remove();
      }, 3000);
    }
  </script>
</body>
</html>
