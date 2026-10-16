from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

# ==========================================
# 1. TERA EXTRACT KIYA HUA RAW JSON DATA
# ==========================================
# Future me tu isko database se connect kar sakta hai
RAW_JSON_DATA = """
{
  "success": true,
  "responseCode": 3006,
  "message": "Course Content",
  "data": [
    {"type": "folder", "title": "Limits and Derivatives", "data": {"content_counts": {"pdf": {"free": 0, "paid": 5}, "video": {"free": 0, "paid": 6}}}},
    {"type": "folder", "title": "Conic Section", "data": {"content_counts": {"pdf": {"free": 0, "paid": 5}, "video": {"free": 0, "paid": 6}}}},
    {"type": "folder", "title": "Introduction to 3D", "data": {"content_counts": {"pdf": {"free": 0, "paid": 3}, "video": {"free": 0, "paid": 2}}}},
    {"type": "folder", "title": "Straight Lines", "data": {"content_counts": {"pdf": {"free": 0, "paid": 6}, "video": {"free": 0, "paid": 6}}}},
    {"type": "folder", "title": "Sequence And Series", "data": {"content_counts": {"pdf": {"free": 0, "paid": 7}, "video": {"free": 0, "paid": 6}}}},
    {"type": "folder", "title": "Binomial Theorem", "data": {"content_counts": {"pdf": {"free": 0, "paid": 4}, "video": {"free": 0, "paid": 3}}}},
    {"type": "folder", "title": "Permutation and Combination", "data": {"content_counts": {"pdf": {"free": 0, "paid": 7}, "video": {"free": 0, "paid": 6}}}},
    {"type": "folder", "title": "Linear Inequalities", "data": {"content_counts": {"pdf": {"free": 0, "paid": 3}, "video": {"free": 0, "paid": 4}}}},
    {"type": "folder", "title": "Complex Number", "data": {"content_counts": {"pdf": {"free": 0, "paid": 6}, "video": {"free": 0, "paid": 5}}}},
    {"type": "folder", "title": "Trignometric Function", "data": {"content_counts": {"pdf": {"free": 0, "paid": 10}, "video": {"free": 0, "paid": 9}}}},
    {"type": "folder", "title": "Relations and Functions", "data": {"content_counts": {"pdf": {"free": 0, "paid": 9}, "video": {"free": 0, "paid": 8}}}},
    {"type": "folder", "title": "Sets", "data": {"content_counts": {"pdf": {"free": 0, "paid": 9}, "video": {"free": 0, "paid": 8}}}}
  ]
}
"""

# ==========================================
# 2. CUSTOM API VAULT UI ENDPOINT
# ==========================================
@app.get("/nt-vault")
async def custom_api_vault():
    # Parse the JSON string into a Python dictionary
    parsed_data = json.loads(RAW_JSON_DATA)
    
    # Dynamic HTML Cards Generate karna
    cards_html = ""
    for item in parsed_data["data"]:
        title = item.get("title", "Unknown Chapter")
        
        # Safe extraction of counts
        try:
            pdf_count = item["data"]["content_counts"]["pdf"]["paid"] + item["data"]["content_counts"]["pdf"]["free"]
            vid_count = item["data"]["content_counts"]["video"]["paid"] + item["data"]["content_counts"]["video"]["free"]
        except KeyError:
            pdf_count = 0
            vid_count = 0

        # Injecting data into UI component
        cards_html += f"""
        <div class="card">
            <div class="thumb">
                <svg viewBox="0 0 24 24" fill="none" stroke="#00ff88" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 40px; height: 40px; opacity: 0.8;">
                    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                </svg>
            </div>
            <div class="info">
                <div class="title">{title}</div>
                <div class="stats">
                    <span class="badge">🎬 {vid_count} Videos</span>
                    <span class="badge" style="background: rgba(255,255,255,0.1); color: #ccc;">📄 {pdf_count} PDFs</span>
                </div>
            </div>
        </div>
        """

    # Main HTML Skeleton
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Master Vault</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Poppins', sans-serif; -webkit-tap-highlight-color: transparent; }}
            body {{ background-color: #050505; color: #fff; padding-bottom: 30px; }}
            
            .header {{ 
                padding: 20px; 
                background: linear-gradient(180deg, #111 0%, #050505 100%); 
                text-align: center; 
                border-bottom: 1px solid #222; 
                position: sticky; 
                top: 0; 
                z-index: 10; 
            }}
            .header h1 {{ font-size: 22px; color: #00ff88; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; }}
            .header p {{ font-size: 11px; color: #888; margin-top: 5px; }}
            
            .grid {{ 
                display: grid; 
                grid-template-columns: repeat(2, 1fr); 
                gap: 15px; 
                padding: 20px; 
            }}
            .card {{ 
                background: #121212; 
                border-radius: 12px; 
                overflow: hidden; 
                border: 1px solid #222; 
                transition: transform 0.2s, border-color 0.2s; 
                cursor: pointer; 
                display: flex;
                flex-direction: column;
            }}
            .card:active {{ transform: scale(0.96); border-color: #00ff88; }}
            
            .thumb {{ 
                width: 100%; 
                height: 90px; 
                background: #1a1a1a; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                border-bottom: 1px solid #222;
            }}
            .info {{ padding: 12px; display: flex; flex-direction: column; justify-content: space-between; flex-grow: 1; }}
            
            .title {{ 
                font-size: 13px; 
                font-weight: 600; 
                color: #fff; 
                margin-bottom: 10px; 
                display: -webkit-box; 
                -webkit-line-clamp: 2; 
                -webkit-box-orient: vertical; 
                overflow: hidden; 
            }}
            .stats {{ display: flex; flex-direction: column; gap: 5px; }}
            .badge {{ 
                display: inline-block; 
                background: rgba(0,255,136,0.1); 
                color: #00ff88; 
                font-size: 10px; 
                padding: 4px 8px; 
                border-radius: 4px; 
                font-weight: 600; 
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>API VAULT</h1>
            <p>100% Ad-Free | Direct Server Render</p>
        </div>

        <div class="grid">
            {cards_html}
        </div>

        <script>
            // Telegram Mini App Initialization
            const tg = window.Telegram.WebApp;
            tg.expand();
            tg.setHeaderColor('#111111');
            tg.setBackgroundColor('#050505');
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=full_html)

# ==========================================
# 3. ROOT DASHBOARD (Home Page)
# ==========================================
@app.get("/")
async def home_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Study Panda Home</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&display=swap" rel="stylesheet">
        <style>
            body { background: #000; color: #fff; font-family: 'Poppins', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .btn { background: #00ff88; color: #000; padding: 15px 30px; border-radius: 8px; font-weight: 700; text-decoration: none; font-size: 16px; margin-top: 20px; transition: transform 0.2s; }
            .btn:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <h1 style="color: #00ff88; font-size: 32px;">Study Panda</h1>
        <p style="color: #888;">Select your module</p>
        <a href="/nt-vault" class="btn">🚀 Enter Next Toppers Vault</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    # Local me test karne ke liye: python main.py
    uvicorn.run(app, host="0.0.0.0", port=8000)
