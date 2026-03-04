import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. การตั้งค่าหน้าจอ Streamlit
# ==========================================
st.set_page_config(
    page_title="Maths Studio",
    page_icon="🔢",
    layout="wide"
)

# Custom CSS สำหรับหน้า Streamlit 
st.markdown("""
<style>
    /* 1. บังคับพื้นหลังให้เป็นสีสว่าง (แบบรูปที่ 1) เสมอ */
    .stApp { background-color: #f8f9fa; }[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e0e0e0; }
    [data-testid="stSidebar"] * { color: #000000 !important; }
    [data-testid="stSidebar"] h1 { font-weight: 800 !important; }
    .stRadio label p { color: #000000 !important; font-weight: 600 !important; font-size: 1.1rem !important; }

    /* 2. สร้างคลาสให้ชื่อโรงเรียนลอยขึ้นไปอยู่ตรงแถบ Header ด้านบนสุด */
    .school-title {
        position: fixed;
        top: 14px; /* ดันลงมาให้อยู่กึ่งกลางแถบ Header พอดี */
        left: 50%;
        transform: translateX(-50%); /* จัดให้อยู่กึ่งกลางหน้าจอเป๊ะๆ */
        z-index: 999999; /* ให้อยู่ชั้นบนสุด */
        font-size: 26px;
        font-weight: 800;
        pointer-events: none; /* ไม่ให้ไปขัดขวางการคลิกเมาส์ */
        /* ข้อความจะดึงสีมาจากระบบ Streamlit อัตโนมัติ (แถบดำ=อักษรขาว, แถบขาว=อักษรดำ) */
    }
</style>

<!-- แสดงชื่อโรงเรียนบนแถบ Header -->
<div class="school-title">🏫 โรงเรียนเทศบาล 6 นครเชียงราย</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. เมนู Sidebar แถบด้านข้าง (ซ้ายบน)
# ==========================================
with st.sidebar:
    # แบ่งพื้นที่ 3 ส่วน เพื่อให้รูปภาพในคอลัมน์ที่ 2 อยู่กึ่งกลาง
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("IMAGE/logo_CRMS6.png", use_container_width=True)
    
    st.header("🔢 Maths Studio")
    
    grid_choice = st.radio(
        "เลือกขนาดตาราง:",["2x2 (Basic)", "3x3 (Standard)", "4x4 (Advanced)", "5x5 (Expert)"],
        index=0
    )
    st.markdown("---")
    st.info("💡 วิธีใช้: พิมพ์ตัวเลขหรือพหุนาม (เช่น x, 2x^2) ลงในช่องสีขาว ผลลัพธ์จะคำนวณและจัดกลุ่มให้อัตโนมัติ")

# กำหนดขนาดตารางตามที่เลือก
size = 2
if "3x3" in grid_choice: size = 3
if "4x4" in grid_choice: size = 4
if "5x5" in grid_choice: size = 5

# ==========================================
# 3. สร้าง HTML Elements แบบ Dynamic (ด้วย Python)
# ==========================================
vlines = "".join([f'<div class="line vline" style="left: {80 + (i * 100)}px;"></div>' for i in range(size)])
hlines = "".join([f'<div class="line hline" style="top: {80 + (i * 100)}px;"></div>' for i in range(size)])

top_inputs = "".join([f'<div class="input-cell"><input id="top{i}" class="gamebox" placeholder="T{i+1}" autocomplete="off"></div>' for i in range(size)])

left_and_results = ""
for j in range(size):
    left_and_results += f'<div class="input-cell"><input id="left{j}" class="gamebox" placeholder="L{j+1}" autocomplete="off"></div>'
    for i in range(size):
        left_and_results += f'<div class="result-cell" id="res_{j}_{i}"></div>'

# ==========================================
# 4. โค้ด HTML / CSS / JS (ฝั่ง Front-end ตาราง)
# ==========================================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600&family=Roboto+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #0d6efd;
            --result-color: #dc3545;
            --grid-line: #000000;
        }}
        body {{
            font-family: 'Sarabun', sans-serif;
            background-color: transparent; 
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0;
            padding-top: 30px;
            padding-bottom: 50px; 
        }}

        .app-container {{
            background: #ffffff;
            color: #000000;
            padding: 50px;
            border-radius: 24px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.08);
            position: relative;
        }}

        .grid-wrapper {{
            display: grid;
            grid-template-columns: 80px repeat({size}, 100px);
            grid-template-rows: 80px repeat({size}, 100px);
            position: relative;
            z-index: 2;
        }}

        .input-cell {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        input.gamebox {{
            width: 55px;
            height: 38px;
            text-align: center;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            background: #ffffff;
            color: #000000;
            transition: 0.2s;
        }}
        input.gamebox:focus {{
            border-color: var(--primary);
            outline: none;
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(13,110,253,0.1);
        }}

        .result-cell {{
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 20px;
            font-weight: 700;
            color: var(--result-color);
            font-family: 'Roboto Mono', monospace;
        }}

        .lines-container {{
            position: absolute;
            top: 50px;
            left: 50px;
            right: 50px;
            bottom: 50px;
            pointer-events: none;
            z-index: 1;
        }}
        .line {{
            position: absolute;
            background-color: var(--grid-line);
        }}
        .vline {{ width: 2px; top: 0; bottom: 0; }}
        .hline {{ height: 2px; left: 0; right: 0; }}

        #finalResultBox {{
            margin-top: 80px;
            padding: 20px 50px;
            background: linear-gradient(135deg, #0d6efd, #0056b3);
            color: white;
            border-radius: 100px;
            font-size: 26px;
            font-weight: 600;
            display: none;
            box-shadow: 0 10px 25px rgba(13,110,253,0.3);
            text-align: center;
            min-width: 350px;
        }}
    </style>
</head>
<body>

<div class="app-container">
    <div class="lines-container">
        {vlines}
        {hlines}
    </div>

    <div class="grid-wrapper">
        <div></div>
        {top_inputs}
        {left_and_results}
    </div>
</div>

<div id="finalResultBox"></div>

<script>
    const size = {size};
    const supMap = {{'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'}};

    function parse(s) {{
        s = s.toLowerCase().replace(/\\s/g, '');
        if (!s) return {{ c: 0, p: 0 }};
        if (!s.includes('x')) return {{ c: parseFloat(s) || 0, p: 0 }};
        let parts = s.split('x');
        let c = parts[0] === '' ? 1 : (parts[0] === '-' ? -1 : parseFloat(parts[0]));
        let p = 1;
        if (parts[1] && parts[1].startsWith('^')) p = parseInt(parts[1].slice(1)) || 0;
        return {{ c, p }};
    }}

    function fmt(c, p) {{
        if (c === 0) return "";
        if (p === 0) return c;
        let res = (c === 1) ? "x" : (c === -1 ? "-x" : c + "x");
        if (p > 1) {{
            res += String(p).split('').map(d => supMap[d]).join('');
        }}
        return res;
    }}

    function update() {{
        let tops = [], lefts =[], allFilled = true;

        for(let i = 0; i < size; i++) {{
            let v = document.getElementById('top'+i).value;
            if(!v) allFilled = false;
            tops.push(parse(v));
        }}
        for(let j = 0; j < size; j++) {{
            let v = document.getElementById('left'+j).value;
            if(!v) allFilled = false;
            lefts.push(parse(v));
        }}

        if (!allFilled) {{
            document.getElementById('finalResultBox').style.display = 'none';
            return;
        }}

        let finalMap = {{}};
        for(let j = 0; j < size; j++) {{
            for(let i = 0; i < size; i++) {{
                let c = tops[i].c * lefts[j].c;
                let p = tops[i].p + lefts[j].p;
                document.getElementById(`res_${{j}}_${{i}}`).innerText = fmt(c, p);
                finalMap[p] = (finalMap[p] || 0) + c;
            }}
        }}

        let terms = Object.keys(finalMap).map(Number).sort((a,b) => b-a)
            .filter(p => finalMap[p] !== 0)
            .map((p, i) => {{
                let c = finalMap[p], s = fmt(c, p);
                if (i > 0 && c > 0) return " + " + s;
                if (c < 0) return " " + s;
                return s;
            }});

        const box = document.getElementById('finalResultBox');
        box.innerText = terms.join('') || "0";
        box.style.display = 'block';
    }}

    document.querySelectorAll('input').forEach(el => el.addEventListener('input', update));
</script>

</body>
</html>
"""

# ==========================================
# 5. แสดงผลผ่าน Streamlit Component
# ==========================================
components.html(html_code, height=950)