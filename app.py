import streamlit as st
import streamlit.components.v1 as components
import datetime
from zoneinfo import ZoneInfo
import time
import threading

# ==============================================================================================================================

# ==========================================
# 1. ระบบนับจำนวนผู้เข้าชม
# ==========================================
if 'visitor_count' not in st.session_state:
    st.session_state.visitor_count = 1
    now = datetime.datetime.now(ZoneInfo("Asia/Bangkok")).strftime('%H:%M:%S')
    print(f"[{now}] 👤 มีผู้เข้าชมใหม่! จำนวนผู้เข้าชมรวม: {st.session_state.visitor_count}")
else:
    # เพิ่มตัวเลขทุกครั้งที่มีการรันหน้าเว็บใหม่ (หรือเปลี่ยนเลขตามต้องการ)
    pass 

if 'logger_running' not in st.session_state:
    # ส่งค่า st.session_state.visitor_count เข้าไปในฟังก์ชัน
    t = threading.Thread(target=log_monitor, args=(st.session_state.visitor_count,), daemon=True)
    t.start()
    st.session_state.logger_running = True

# ==========================================
# 2. ระบบ Log เบื้องหลัง (ไม่รีเฟรชหน้าเว็บ)
# ==========================================
def log_monitor(visitor_count): # ส่งค่า count เข้าไปเป็น Parameter แทนการดึงจาก session_state
    while True:
        now = datetime.datetime.now(ZoneInfo("Asia/Bangkok")).strftime('%H:%M:%S')
        # ใช้ค่า visitor_count ที่ส่งเข้ามา
        print(f"[{now}] 🟢 สถานะ: ระบบทำงานปกติ | ผู้ใช้งานปัจจุบัน: {visitor_count} คน")
        time.sleep(10)

if 'logger_running' not in st.session_state:
    t = threading.Thread(target=log_monitor, daemon=True)
    t.start()
    st.session_state.logger_running = True

# ==========================================
# 3. ตรวจจับการออกจากหน้าเว็บ
# ==========================================
# หมายเหตุ: Streamlit เป็นแบบ Server-side การตรวจจับการ "ปิดหน้าเว็บ" ทันทีทำได้ยาก
# แต่เราสามารถแสดงใน Log ได้เมื่อมีการ Refresh หรือเปลี่ยนหน้า
now_exit = datetime.datetime.now(ZoneInfo("Asia/Bangkok")).strftime('%H:%M:%S')
# ข้อความนี้จะถูกพิมพ์เมื่อมีการโหลดหน้าเว็บใหม่
print(f"[{now_exit}] ℹ️ กำลังโหลดหน้าแอป Maths Studio... ยินดีต้อนรับครับ")


# ==============================================================================================================================

# ==========================================
# 1. การตั้งค่าหน้าจอ
# ==========================================

st.set_page_config(page_title="Maths Studio", page_icon="🔢", layout="wide")

# บังคับพื้นหลังให้เป็นแบบสว่าง (Light Theme) เพื่อให้กล่องสีขาวเด่นขึ้นมา
st.markdown("""
<style>
    .stApp, .stApp > header { background-color: #f8f9fa !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e0e0e0; }
    [data-testid="stSidebar"] * { color: #000000 !important; }
    
    .school-title { 
        position: fixed; 
        top: 14px; 
        left: 50%; 
        transform: translateX(-50%); 
        z-index: 999999; 
        font-size: 26px; 
        font-weight: 800; 
        color: var(--text-color) !important; 
        pointer-events: none; 
    }
</style>
<div class="school-title">🏫 โรงเรียนเทศบาล 6 นครเชียงราย</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. แถบเครื่องมือด้านข้าง (Sidebar)
# ==========================================
with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2: 
        # ใส่ try-except ไว้กัน Error กรณีไม่มีไฟล์รูปภาพ
        try:
            st.image("IMAGE/logo_CRMS6.png", use_container_width=True)
        except:
            pass
            
    st.header("🔢 Maths Studio")
    grid_choice = st.radio("เลือกขนาดตาราง:",["2x2 (Basic)", "3x3 (Standard)", "4x4 (Advanced)", "5x5 (Expert)"], index=0)
    st.markdown("---")
    st.info("💡 วิธีใช้: พิมพ์ตัวเลขหรือพหุนาม (เช่น x, 2x^2) ลงในช่องสีขาวตามตัวเลขที่กำหนด ผลลัพธ์จะคำนวณและจัดกลุ่มให้อัตโนมัติ ")

# กำหนดขนาด size ตามตัวเลือก
size = 2
if "3x3" in grid_choice: size = 3
if "4x4" in grid_choice: size = 4
if "5x5" in grid_choice: size = 5

# ==========================================
# 3. สร้าง HTML ส่วนประกอบ
# ==========================================
# สร้างเส้นให้อยู่ตรงขอบของ Grid พอดี
vlines = "".join([f'<div class="line vline" style="left: {80 + (i * 100)}px;"></div>' for i in range(size)])
hlines = "".join([f'<div class="line hline" style="top: {80 + (i * 100)}px;"></div>' for i in range(size)])
top_inputs = "".join([f'<div class="input-cell"><input id="top{i}" class="gamebox" placeholder="T{i+1}" autocomplete="off"></div>' for i in range(size)])

# ให้ L เรียงจาก size ลงไปหา 1 (L1 อยู่ล่างสุด)
left_and_results = ""
for j in range(size - 1, -1, -1):
    left_and_results += f'<div class="input-cell"><input id="left{j}" class="gamebox" placeholder="L{j+1}" autocomplete="off"></div>'
    for i in range(size):
        left_and_results += f'<div class="result-cell" id="res_{j}_{i}"></div>'

# ==========================================
# 4. โค้ด HTML/JS
# ==========================================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@500;700&family=Sarabun:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ 
            font-family: 'Sarabun', sans-serif; 
            display: flex; 
            justify-content: center; 
            padding-top: 40px; 
            margin: 0;
            background: transparent; /* ให้โปร่งใสเพื่อกลืนไปกับ Streamlit */
        }}
        .app-container {{ 
            background: #ffffff; 
            padding: 50px; 
            border-radius: 24px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.08); 
            display: inline-flex;
            flex-direction: column;
            align-items: center;
        }}
        .grid-wrapper {{ 
            display: grid; 
            grid-template-columns: 80px repeat({size}, 100px); 
            grid-template-rows: 80px repeat({size}, 100px); 
            position: relative; /* สำคัญมาก: ให้เส้นใช้อ้างอิงตำแหน่งจากกล่องนี้ */
            z-index: 2; 
        }}
        .lines-container {{ 
            position: absolute; 
            top: 0; left: 0; right: 0; bottom: 0; 
            pointer-events: none; 
            z-index: 1; 
        }}
        .line {{ position: absolute; background-color: #000; }}
        .vline {{ width: 2px; top: 10px; bottom: 10px; }}
        .hline {{ height: 2px; left: 10px; right: 10px; }}
        
        .input-cell, .result-cell {{ 
            display: flex; justify-content: center; align-items: center; z-index: 2;
        }}
        input.gamebox {{ 
            width: 60px; height: 40px; text-align: center; 
            border: 1px solid #ced4da; border-radius: 8px; 
            font-family: 'Sarabun', sans-serif; font-weight: 600; font-size: 15px; 
            outline: none; transition: all 0.2s ease; 
        }}
        input.gamebox:focus {{ 
            border-color: #0d6efd; box-shadow: 0 0 0 3px rgba(13,110,253,0.25); 
        }}
        .result-cell {{ 
            font-size: 20px; font-weight: 700; color: #dc3545; font-family: 'Roboto Mono', monospace; 
        }}
        #finalResultBox {{ 
            margin-top: 50px; padding: 15px 50px; 
            background: linear-gradient(135deg, #0d6efd, #0056b3); color: white; 
            border-radius: 100px; font-size: 26px; font-weight: 600; display: none; 
            text-align: center; box-shadow: 0 5px 15px rgba(13,110,253,0.3);
        }}
        sup {{ font-size: 0.65em; vertical-align: super; }}
    </style>
</head>
<body>
    <div class="app-container">
        <div class="grid-wrapper">
            <div class="lines-container">{vlines}{hlines}</div>
            <div></div> <!-- ช่องว่างซ้ายบน -->
            {top_inputs}
            {left_and_results}
        </div>
        <div id="finalResultBox"></div>
    </div>
<script>
    const size = {size};
    function parse(s) {{ s = s.toLowerCase().replace(/\\s/g, ''); if(!s) return {{c:0, p:0}}; if(!s.includes('x')) return {{c:parseFloat(s)||0, p:0}}; let parts = s.split('x'); let c = parts[0]==='' ? 1 : (parts[0]==='-' ? -1 : parseFloat(parts[0])); let p = 1; if(parts[1] && parts[1].startsWith('^')) p = parseInt(parts[1].slice(1)) || 0; return {{c, p}}; }}
    function fmt(c, p) {{ if(c===0) return ""; if(p===0) return c; let res = (c===1) ? "x" : (c===-1 ? "-x" : c+"x"); if(p!==1) res += "<sup>"+p+"</sup>"; return res; }}
    function update() {{
        let tops=[], lefts=[], allFilled=true;
        for(let i=0; i<size; i++) {{ let v = document.getElementById('top'+i).value; if(!v) allFilled=false; tops.push(parse(v)); }}
        for(let j=0; j<size; j++) {{ let v = document.getElementById('left'+j).value; if(!v) allFilled=false; lefts.push(parse(v)); }}
        if(!allFilled) {{ document.getElementById('finalResultBox').style.display='none'; return; }}
        let finalMap={{}};
        for(let j=0; j<size; j++) {{
            for(let i=0; i<size; i++) {{
                let c = tops[i].c * lefts[j].c; let p = tops[i].p + lefts[j].p;
                document.getElementById(`res_${{j}}_${{i}}`).innerHTML = fmt(c, p);
                finalMap[p] = (finalMap[p]||0) + c;
            }}
        }}
        let terms = Object.keys(finalMap).map(Number).sort((a,b)=>b-a).filter(p=>finalMap[p]!==0).map((p,i)=>{{ let c=finalMap[p], s=fmt(c, p); if(i>0 && c>0) return " + "+s; if(c<0) return " "+s; return s; }});
        const box = document.getElementById('finalResultBox');
        box.innerHTML = terms.join('') || "0"; box.style.display='block';
    }}
    document.querySelectorAll('input').forEach(el => el.addEventListener('input', update));
</script>
</body>
</html>
"""
components.html(html_code, height=900)

# ==============================================================================================================================

# ==========================================
# 5. เวลา
# ==========================================
# สร้างพื้นที่สำหรับเวลา
time_placeholder = st.empty()

# ดึงเวลาไทย
bangkok_now = datetime.datetime.now(ZoneInfo("Asia/Bangkok"))
time_str = bangkok_now.strftime('%d/%m/%Y %H:%M:%S')

# แสดงเวลาในพื้นที่ที่กำหนด
time_placeholder.markdown(f"<p style='text-align: center; color: gray;'>เข้าเมื่อ: {time_str}</p>", unsafe_allow_html=True)