import os
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"

import cv2
import numpy as np
import mediapipe as mp
import random
import math
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, WebRtcMode

# ── 1. ULTRA HIGH-END NEON STUDIO UI ──────────────────────────────────────────
st.set_page_config(
    page_title="Hand AR Magic Studio Pro",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Premium Cyberpunk & Glassmorphism Styling
st.markdown("""
    <style>
    /* Animated Tech Matrix Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0b0f19 0%, #05070c 100%);
        color: #ffffff;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Glowing Industry Header */
    .studio-title {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-background-fill-color: transparent;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        font-size: 2.6rem;
        margin-top: -20px;
        margin-bottom: 2px;
        letter-spacing: -0.5px;
        filter: drop-shadow(0px 0px 15px rgba(0, 242, 254, 0.4));
    }
    .subtitle { 
        text-align: center; 
        color: #64748b; 
        font-size: 1rem; 
        margin-bottom: 25px;
        font-weight: 400;
    }

    /* Premium Glassmorphism Dropdown Widget */
    div[data-testid="stSelectbox"] {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(0, 242, 254, 0.25) !important;
        padding: 15px !important;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.5) !important;
    }
    div[data-testid="stSelectbox"] label p { 
        color: #00f2fe !important; 
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        font-size: 0.85rem !important;
    }
    div[data-testid="stSelectbox"] > div { 
        background-color: #090d16 !important; 
        color: white !important; 
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    /* Video Frame Border Glow */
    div[data-testid="stVideo"] video, iframe, .element-container video {
        border-radius: 16px !important;
        border: 2px solid rgba(0, 242, 254, 0.3) !important;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.15) !important;
    }

    /* Custom Modern Recording Buttons */
    .rec-btn-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 20px 0;
    }
    .btn-rec {
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
        font-size: 0.95rem;
    }
    .btn-start {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
    }
    .btn-stop {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    .btn-rec:hover { transform: translateY(-2px); filter: brightness(1.1); }

    /* Ultra Premium Footer */
    .footer { 
        text-align: center; 
        margin-top: 60px; 
        padding: 25px; 
        color: #475569; 
        font-size: 0.9rem; 
        border-top: 1px solid rgba(255, 255, 255, 0.03); 
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .footer strong { 
        color: #00f2fe; 
        text-shadow: 0 0 12px rgba(0, 242, 254, 0.6);
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='studio-title'>HAND AR MAGIC STUDIO PRO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Next-Gen Real-Time Hand Tracking & Special Effects Platform</p>", unsafe_allow_html=True)

# Effect Dictionary
EFFECTS = ["fire", "superman", "lightning", "ice", "galaxy", "magic", "ironman"]
LABELS = {
    "fire": "🔥 Pyro Fire Blast", 
    "superman": "⚡ Krypton Energy", 
    "lightning": "⚡ Electric Storm",
    "ice": "❄ Glacial Frost", 
    "galaxy": "🌌 Cosmic Nebula", 
    "magic": "✨ Sorcerer Mystic", 
    "ironman": "🤖 Repulsor Beam"
}

selected_effect = st.selectbox(
    "🔮 सेलेक्ट स्पेशल इफ़ेक्ट Engine:", 
    EFFECTS, 
    format_func=lambda x: LABELS[x],
    index=0
)

# ── 2. MEDIAPEPIE SETUP ───────────────────────────────────────────────────────
@st.cache_resource
def load_mediapipe():
    mp_hands = mp.solutions.hands
    return mp_hands.Hands(
        max_num_hands=2, 
        min_detection_confidence=0.55, 
        min_tracking_confidence=0.55
    )
hands = load_mediapipe()

# ── 3. OPTIMIZED PARTICLE SYSTEM ──────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, effect):
        self.reset(x, y, effect)

    def reset(self, x, y, effect):
        self.x = x + random.randint(-12, 12)
        self.y = y + random.randint(-12, 12)
        self.effect = effect
        angle = random.uniform(0, 2 * math.pi)
        
        if effect == "fire":
            self.vx, self.vy = random.uniform(-1.2, 1.2), random.uniform(-4, -1.5)
            self.life = self.max_life = random.randint(15, 30)
            self.size = random.randint(4, 10)
        elif effect == "superman":
            speed = random.uniform(2, 4.5)
            self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed
            self.life = self.max_life = random.randint(12, 25)
            self.size = random.randint(3, 6)
        elif effect == "lightning":
            self.vx, self.vy = random.uniform(-2.5, 2.5), random.uniform(-3.5, -1)
            self.life = self.max_life = random.randint(8, 16)
            self.size = random.randint(2, 5)
        elif effect == "ice":
            speed = random.uniform(1, 2.5)
            self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed - 0.3
            self.life = self.max_life = random.randint(18, 30)
            self.size = random.randint(3, 6)
        elif effect == "galaxy":
            speed = random.uniform(0.4, 2.2)
            self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed
            self.life = self.max_life = random.randint(20, 35)
            self.size = random.randint(1, 4)
        elif effect == "magic":
            speed = random.uniform(1, 3.5)
            self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed
            self.life = self.max_life = random.randint(15, 28)
            self.size = random.randint(3, 7)
        elif effect == "ironman":
            speed = random.uniform(2, 7)
            self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed
            self.life = self.max_life = random.randint(10, 20)
            self.size = random.randint(4, 12)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        if self.effect in ["fire", "ironman"]:
            self.vx *= 0.94
            self.size = max(1, self.size - 0.25)
        elif self.effect == "lightning":
            self.vx += random.uniform(-0.8, 0.8)

    def is_alive(self):
        return self.life > 0

    def draw(self, overlay):
        ratio = self.life / self.max_life
        ix, iy = int(self.x), int(self.y)
        s = max(1, int(self.size))
        alpha = ratio

        if self.effect == "fire":
            color = (0, 180, 255) if ratio > 0.6 else ((0, 90, 255) if ratio > 0.3 else (0, 20, 180))
        elif self.effect == "superman":
            color = (255, 40, 40) if random.random() > 0.5 else (40, 40, 255)
        elif self.effect == "lightning":
            color = (255, 255, 170)
        elif self.effect == "ice":
            color = (255, 210, 130)
        elif self.effect == "galaxy":
            color = random.choice([(255, 80, 180), (180, 80, 255), (80, 180, 255)])
        elif self.effect == "magic":
            color = [(0, 255, 180), (255, 0, 180), (255, 180, 0)][int(ratio * 10) % 3]
        elif self.effect == "ironman":
            color = (255, 255, 255) if ratio > 0.6 else ((0, 180, 255) if ratio > 0.3 else (0, 40, 255))

        c = (int(color[0]*alpha), int(color[1]*alpha), int(color[2]*alpha))
        cv2.circle(overlay, (ix, iy), s, c, -1)

# ── 4. VIDEO PROCESSING THREAD ────────────────────────────────────────────────
class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.particles = []
        self.max_particles = 400  
        self.spawn_per_frame = 5
        self.current_effect = "fire"  

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        h, w = img.shape[:2]

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        tip_points = []
        palm_points = []
        is_hand_open = False

        if result.multi_hand_landmarks:
            for hand_lm in result.multi_hand_landmarks:
                wrist = hand_lm.landmark[0]
                tips_open = 0
                for tip_idx, mcp_idx in [(8, 5), (12, 9), (16, 13), (20, 17)]:
                    tip = hand_lm.landmark[tip_idx]
                    mcp = hand_lm.landmark[mcp_idx]
                    if math.hypot(tip.x - wrist.x, tip.y - wrist.y) > math.hypot(mcp.x - wrist.x, mcp.y - wrist.y) * 1.2:
                        tips_open += 1
                
                if tips_open >= 3:
                    is_hand_open = True
                    palm = hand_lm.landmark[9]
                    palm_points.append((int(palm.x * w), int(palm.y * h)))

                for tip_id in [4, 8, 12, 16, 20]:
                    lm = hand_lm.landmark[tip_id]
                    tip_points.append((int(lm.x * w), int(lm.y * h)))

        eff = self.current_effect

        if len(self.particles) < self.max_particles:
            if eff == "ironman" and is_hand_open:
                for (px, py) in palm_points:
                    for _ in range(self.spawn_per_frame * 3):
                        self.particles.append(Particle(px, py, eff))
            else:
                for (cx, cy) in tip_points:
                    for _ in range(self.spawn_per_frame):
                        self.particles.append(Particle(cx, cy, eff))

        alive = []
        particle_overlay = np.zeros_like(img)
        for p in self.particles:
            p.update()
            if p.is_alive():
                p.draw(particle_overlay)
                alive.append(p)
        self.particles = alive

        if len(self.particles) > 0:
            img = cv2.add(img, particle_overlay)

        return img

# ── 5. STREAMER & CONTROLLER ──────────────────────────────────────────────────
RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

ctx = webrtc_streamer(
    key="hand-ar-core",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=VideoProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={
        "video": {"width": {"ideal": 640}, "height": {"ideal": 480}, "frameRate": {"ideal": 30}}, 
        "audio": False
    },
    async_processing=True,
)

if ctx.video_processor:
    ctx.video_processor.current_effect = selected_effect

# ── 6. INDUSTRY-GRADE BROWSER VIDEO RECORDER (JAVASCRIPT INTEGRATION) ─────────
st.markdown("""
    <div class="rec-btn-container">
        <button class="btn-rec btn-start" onclick="startStudioRecording()">🔴 Start Recording</button>
        <button class="btn-rec btn-stop" onclick="stopStudioRecording()"> Regency ⏹️ Stop & Download</button>
    </div>

    <script>
    var studioMediaRecorder;
    var studioRecordedChunks = [];

    async function startStudioRecording() {
        studioRecordedChunks = [];
        // Target the WebRTC output video element rendered on screen
        var videoEl = document.querySelector('video');
        if (!videoEl) {
            alert('कैमरा एक्टिव नहीं है! कृपया पहले START बटन दबाएं।');
            return;
        }
        
        var stream = videoEl.captureStream ? videoEl.captureStream() : videoEl.mozCaptureStream();
        studioMediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm;codecs=vp9' });
        
        studioMediaRecorder.ondataavailable = function(e) {
            if (e.data.size > 0) studioRecordedChunks.push(e.data);
        };
        
        studioMediaRecorder.onstop = function() {
            var blob = new Blob(studioRecordedChunks, { type: 'video/webm' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'Hand_AR_Magic_Clip.webm';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        };
        
        studioMediaRecorder.start();
        alert('🔴 Recording started! Start performing your magic!');
    }

    function stopStudioRecording() {
        if (studioMediaRecorder && studioMediaRecorder.state !== 'inactive') {
            studioMediaRecorder.stop();
            alert('⏹️ Recording stopped! Your clip is being downloaded!');
        } else {
            alert('No active recording found.');
        }
    }
    </script>
""", unsafe_allow_html=True)

st.info("💡 Usage Method: First click 'START' to turn on the camera. Then click 'Start Recording' below to record your magic!")

# ── 7. BRANDING FOOTER ────────────────────────────────────────────────────────
st.markdown("<div class='footer'>Designed & Deep Engineered by <strong>Dheeraj Prajapat</strong></div>", unsafe_allow_html=True)
