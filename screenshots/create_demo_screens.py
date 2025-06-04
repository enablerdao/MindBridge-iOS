#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw, ImageFont
import platform

# Create screenshots directory
os.makedirs("screenshots", exist_ok=True)

# iPhone 14 Pro dimensions
WIDTH = 393
HEIGHT = 852
SAFE_AREA_TOP = 59
SAFE_AREA_BOTTOM = 34

# Colors
COLORS = {
    'bg_primary': "#0A0A0A",
    'bg_secondary': "#1C1C1E", 
    'card_dark': "#2C2C2E",
    'accent_blue': "#007AFF",
    'accent_purple': "#AF52DE",
    'accent_green': "#30D158",
    'text_primary': "#FFFFFF",
    'text_secondary': "#8E8E93",
    'user_bubble': "#007AFF",
    'ai_bubble': "#2C2C2E",
}

def get_font(size=16, bold=False):
    """Get appropriate font for the system"""
    try:
        if bold:
            return ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", size)
        else:
            return ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", size)
    except:
        return ImageFont.load_default()

def create_gradient(width, height, start_color, end_color):
    """Create gradient background"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    
    for i in range(height):
        progress = i / height
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * progress)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * progress)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * progress)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    return img

def create_ai_thinking_screen():
    """AI thinking animation screen"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "Qwen3-4B Chat", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(18, bold=True))
    
    y_pos = SAFE_AREA_TOP + 80
    
    # User message
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 80)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 20), "複雑な数学の問題を解いて", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 40), "f(x) = x³ - 2x² + x - 1 の", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 60), "極値を求めてください", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    
    y_pos += 100
    
    # AI thinking bubble
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 120)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_purple'], width=1)
    
    # AI avatar
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_purple'])
    draw.text((35, y_pos + 20), "🧠", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    # Thinking animation
    draw.text((55, y_pos + 20), "Qwen3 は考えています...", fill=COLORS['accent_purple'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Thinking process
    draw.text((30, y_pos + 50), "📝 微分を計算中", fill=COLORS['text_secondary'], 
              anchor="lt", font=get_font(12))
    draw.text((30, y_pos + 70), "🔍 極値を特定中", fill=COLORS['text_secondary'], 
              anchor="lt", font=get_font(12))
    draw.text((30, y_pos + 90), "✨ 解を整理中", fill=COLORS['text_secondary'], 
              anchor="lt", font=get_font(12))
    
    # Thinking dots animation
    for i, dot in enumerate(['●', '●', '○']):
        x_pos = WIDTH - 80 + i * 15
        color = COLORS['accent_purple'] if dot == '●' else COLORS['text_secondary']
        draw.text((x_pos, y_pos + 90), dot, fill=color, anchor="mm", font=get_font(16))
    
    bg.save("screenshots/ai_thinking.png")
    print("✅ Created ai_thinking.png")

def create_performance_metrics():
    """Performance metrics screen"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "パフォーマンス", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(18, bold=True))
    
    y_pos = SAFE_AREA_TOP + 70
    
    # Real-time metrics
    draw.text((25, y_pos), "📊 リアルタイムメトリクス", fill=COLORS['accent_blue'], 
              anchor="lt", font=get_font(16, bold=True))
    y_pos += 40
    
    # Speed metrics
    metrics = [
        ("⚡ 推論速度", "42.3 トークン/秒", COLORS['accent_green']),
        ("🧠 メモリ使用量", "2.1GB / 8.0GB", COLORS['accent_blue']),
        ("🔥 GPU使用率", "67%", COLORS['accent_purple']),
        ("⏱️ 平均応答時間", "0.8秒", COLORS['accent_green']),
        ("🔋 バッテリー効率", "92%", COLORS['accent_green']),
        ("📈 処理精度", "99.2%", COLORS['accent_blue'])
    ]
    
    for metric, value, color in metrics:
        draw.rounded_rectangle([(20, y_pos), (WIDTH - 20, y_pos + 50)], 
                              radius=12, fill=COLORS['card_dark'])
        
        draw.text((30, y_pos + 15), metric, fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(14))
        draw.text((WIDTH - 30, y_pos + 15), value, fill=color, 
                  anchor="rt", font=get_font(14, bold=True))
        
        # Progress bar for some metrics
        if "%" in value:
            percentage = float(value.replace("%", "")) / 100
            bar_width = WIDTH - 100
            draw.rounded_rectangle([(30, y_pos + 32), (WIDTH - 30, y_pos + 37)], 
                                  radius=3, fill=COLORS['text_secondary'])
            draw.rounded_rectangle([(30, y_pos + 32), (30 + bar_width * percentage, y_pos + 37)], 
                                  radius=3, fill=color)
        
        y_pos += 65
    
    bg.save("screenshots/performance_metrics.png")
    print("✅ Created performance_metrics.png")

def create_multilingual_chat():
    """Multilingual conversation demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "多言語対応", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(18, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # English conversation
    draw.rounded_rectangle([(80, y_pos), (WIDTH - 20, y_pos + 40)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 20), "Hello! Can you speak English?", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 60
    
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 80, y_pos + 60)], 
                          radius=18, fill=COLORS['ai_bubble'])
    draw.text((30, y_pos + 15), "🇺🇸 Yes! I can communicate in", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(13))
    draw.text((30, y_pos + 35), "multiple languages fluently.", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(13))
    y_pos += 80
    
    # Chinese conversation
    draw.rounded_rectangle([(80, y_pos), (WIDTH - 20, y_pos + 40)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 20), "你好！你会说中文吗？", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 60
    
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 80, y_pos + 60)], 
                          radius=18, fill=COLORS['ai_bubble'])
    draw.text((30, y_pos + 15), "🇨🇳 当然可以！我可以用中文", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(13))
    draw.text((30, y_pos + 35), "进行自然的对话。", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(13))
    y_pos += 80
    
    # Korean conversation
    draw.rounded_rectangle([(80, y_pos), (WIDTH - 20, y_pos + 40)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 20), "한국어도 할 수 있나요?", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 60
    
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 80, y_pos + 60)], 
                          radius=18, fill=COLORS['ai_bubble'])
    draw.text((30, y_pos + 15), "🇰🇷 네! 한국어로도 대화가", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(13))
    draw.text((30, y_pos + 35), "가능합니다.", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(13))
    
    bg.save("screenshots/multilingual_chat.png")
    print("✅ Created multilingual_chat.png")

def create_math_solver():
    """Math problem solving demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "数学問題解決", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(18, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # Math problem
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 60)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "∫(2x + 3)dx を計算して", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "ステップごとに教えて", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 80
    
    # AI solution
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 280)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_blue'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_blue'])
    draw.text((35, y_pos + 20), "📊", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "数学解法ステップ", fill=COLORS['accent_blue'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Step by step solution
    steps = [
        "ステップ1: 積分の基本公式を適用",
        "∫(2x + 3)dx = ∫2x dx + ∫3 dx",
        "",
        "ステップ2: 各項を個別に積分",
        "∫2x dx = 2 ∫x dx = 2 · x²/2 = x²",
        "∫3 dx = 3x",
        "",
        "ステップ3: 結果をまとめる",
        "∫(2x + 3)dx = x² + 3x + C",
        "",
        "答え: x² + 3x + C"
    ]
    
    text_y = y_pos + 50
    for step in steps:
        if step == "":
            text_y += 10
            continue
        elif step.startswith("ステップ"):
            color = COLORS['accent_green']
            font = get_font(12, bold=True)
        elif step.startswith("答え"):
            color = COLORS['accent_purple']
            font = get_font(13, bold=True)
        else:
            color = COLORS['text_primary']
            font = get_font(12)
        
        draw.text((30, text_y), step, fill=color, anchor="lt", font=font)
        text_y += 20
    
    bg.save("screenshots/math_solver.png")
    print("✅ Created math_solver.png")

# Generate demo screens
create_ai_thinking_screen()
create_performance_metrics()
create_multilingual_chat()
create_math_solver()

print("\n🎯 All demo screens generated!")