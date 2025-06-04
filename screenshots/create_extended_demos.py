#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw, ImageFont
import platform
import math

# Create screenshots directory
os.makedirs("screenshots", exist_ok=True)

# iPhone 14 Pro dimensions
WIDTH = 393
HEIGHT = 852
SAFE_AREA_TOP = 59
SAFE_AREA_BOTTOM = 34

# Premium Colors
COLORS = {
    'bg_primary': "#0A0A0A",
    'bg_secondary': "#1C1C1E", 
    'card_dark': "#2C2C2E",
    'card_light': "#3A3A3C",
    'accent_blue': "#007AFF",
    'accent_purple': "#AF52DE",
    'accent_green': "#30D158",
    'accent_orange': "#FF9F0A",
    'accent_red': "#FF453A",
    'accent_pink': "#FF2D92",
    'accent_cyan': "#32D74B",
    'text_primary': "#FFFFFF",
    'text_secondary': "#8E8E93",
    'text_tertiary': "#48484A",
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

def create_gradient(width, height, start_color, end_color, direction='vertical'):
    """Create gradient background"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    
    for i in range(height if direction == 'vertical' else width):
        progress = i / (height if direction == 'vertical' else width)
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * progress)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * progress)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * progress)
        
        if direction == 'vertical':
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        else:
            draw.line([(i, 0), (i, height)], fill=(r, g, b))
    
    return img

def create_creative_writing_demo():
    """Creative writing assistance demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "クリエイティブライティング", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(16, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User request
    draw.rounded_rectangle([(40, y_pos), (WIDTH - 20, y_pos + 80)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "桜をテーマにした", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "美しい俳句を作って", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 55), "ください 🌸", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 100
    
    # AI creative response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 220)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_pink'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_pink'])
    draw.text((35, y_pos + 20), "🌸", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "詩人モード", fill=COLORS['accent_pink'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Haiku with beautiful formatting
    draw.text((30, y_pos + 50), "桜咲く", fill=COLORS['accent_pink'], 
              anchor="lt", font=get_font(18, bold=True))
    draw.text((30, y_pos + 75), "風に舞い散る", fill=COLORS['accent_pink'], 
              anchor="lt", font=get_font(18, bold=True))
    draw.text((30, y_pos + 100), "花びらかな", fill=COLORS['accent_pink'], 
              anchor="lt", font=get_font(18, bold=True))
    
    # Translation and explanation
    draw.text((30, y_pos + 140), "【解釈】", fill=COLORS['accent_cyan'], 
              anchor="lt", font=get_font(12, bold=True))
    draw.text((30, y_pos + 160), "春の訪れと共に咲く桜の花が", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(12))
    draw.text((30, y_pos + 180), "風に舞い踊り、散りゆく様子を", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(12))
    draw.text((30, y_pos + 200), "表現した季節感あふれる一句", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(12))
    
    bg.save("screenshots/creative_writing.png")
    print("✅ Created creative_writing.png")

def create_language_learning_demo():
    """Language learning demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "語学学習アシスタント", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(16, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User question
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 60)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "英語の現在完了形を", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "わかりやすく教えて", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 80
    
    # AI teaching response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 300)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_green'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_green'])
    draw.text((35, y_pos + 20), "📚", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "英語講師モード", fill=COLORS['accent_green'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Grammar explanation
    draw.text((30, y_pos + 50), "現在完了形の基本構造：", fill=COLORS['accent_orange'], 
              anchor="lt", font=get_font(14, bold=True))
    
    # Formula
    draw.rounded_rectangle([(30, y_pos + 75), (WIDTH - 70, y_pos + 95)], 
                          radius=8, fill=COLORS['bg_primary'])
    draw.text((40, y_pos + 80), "have/has + 過去分詞", fill=COLORS['accent_cyan'], 
              anchor="lt", font=get_font(13, bold=True))
    
    # Examples with different colors
    draw.text((30, y_pos + 110), "📝 例文：", fill=COLORS['accent_blue'], 
              anchor="lt", font=get_font(13, bold=True))
    
    examples = [
        ("I have studied English.", "英語を勉強したことがある"),
        ("She has lived in Tokyo.", "彼女は東京に住んだことがある"),
        ("We have finished homework.", "私たちは宿題を終えた")
    ]
    
    example_y = y_pos + 135
    for english, japanese in examples:
        draw.text((40, example_y), english, fill=COLORS['accent_green'], 
                  anchor="lt", font=get_font(12))
        draw.text((40, example_y + 15), f"→ {japanese}", fill=COLORS['text_secondary'], 
                  anchor="lt", font=get_font(11))
        example_y += 40
    
    # Usage note
    draw.text((30, y_pos + 260), "💡 使い方のコツ：", fill=COLORS['accent_purple'], 
              anchor="lt", font=get_font(12, bold=True))
    draw.text((30, y_pos + 280), "過去の経験や完了した動作を表現", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(11))
    
    bg.save("screenshots/language_learning.png")
    print("✅ Created language_learning.png")

def create_cooking_assistant():
    """Cooking assistant demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "料理アシスタント", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(16, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User request
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 60)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "簡単な親子丼の", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "作り方を教えて 🍳", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 80
    
    # AI cooking response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 320)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_orange'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_orange'])
    draw.text((35, y_pos + 20), "👨‍🍳", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "料理シェフモード", fill=COLORS['accent_orange'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Ingredients
    draw.text((30, y_pos + 50), "🥘 材料（2人分）：", fill=COLORS['accent_green'], 
              anchor="lt", font=get_font(13, bold=True))
    
    ingredients = [
        "• 鶏もも肉 200g",
        "• 玉ねぎ 1個",
        "• 卵 4個",
        "• ご飯 2杯分",
        "• だし汁 200ml"
    ]
    
    ing_y = y_pos + 75
    for ingredient in ingredients:
        draw.text((40, ing_y), ingredient, fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(11))
        ing_y += 18
    
    # Cooking steps
    draw.text((30, y_pos + 170), "👨‍🍳 作り方：", fill=COLORS['accent_blue'], 
              anchor="lt", font=get_font(13, bold=True))
    
    steps = [
        "1. 鶏肉と玉ねぎを切る",
        "2. フライパンで鶏肉を炒める",
        "3. だし汁を加えて煮る",
        "4. 溶き卵を回し入れる",
        "5. ご飯にのせて完成！"
    ]
    
    step_y = y_pos + 195
    for step in steps:
        draw.text((40, step_y), step, fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(11))
        step_y += 20
    
    # Cooking tip
    draw.text((30, y_pos + 295), "💡 コツ：卵は半熟に仕上げると美味！", fill=COLORS['accent_pink'], 
              anchor="lt", font=get_font(11))
    
    bg.save("screenshots/cooking_assistant.png")
    print("✅ Created cooking_assistant.png")

def create_travel_planner():
    """Travel planning demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "旅行プランナー", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(16, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User request
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 60)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "京都の2泊3日", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "おすすめプランは？", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 80
    
    # AI travel response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 350)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_cyan'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_cyan'])
    draw.text((35, y_pos + 20), "✈️", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "旅行ガイドモード", fill=COLORS['accent_cyan'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Day by day itinerary
    days = [
        {
            'day': '1日目',
            'morning': '清水寺 → 二年坂・三年坂',
            'afternoon': '祇園 → 花見小路',
            'evening': '京料理ディナー'
        },
        {
            'day': '2日目', 
            'morning': '金閣寺 → 龍安寺',
            'afternoon': '嵐山 → 竹林の小径',
            'evening': '温泉でリラックス'
        },
        {
            'day': '3日目',
            'morning': '伏見稲荷大社',
            'afternoon': '錦市場でお土産',
            'evening': '京都駅から帰路'
        }
    ]
    
    day_y = y_pos + 50
    for day_plan in days:
        # Day header
        draw.text((30, day_y), f"📅 {day_plan['day']}", fill=COLORS['accent_purple'], 
                  anchor="lt", font=get_font(13, bold=True))
        day_y += 25
        
        # Schedule items
        schedule_items = [
            (f"🌅 午前: {day_plan['morning']}", COLORS['accent_green']),
            (f"☀️ 午後: {day_plan['afternoon']}", COLORS['accent_blue']),
            (f"🌙 夜: {day_plan['evening']}", COLORS['accent_orange'])
        ]
        
        for item, color in schedule_items:
            draw.text((40, day_y), item, fill=color, anchor="lt", font=get_font(11))
            day_y += 18
        
        day_y += 10
    
    # Travel tip
    draw.text((30, y_pos + 320), "🎫 京都市バス1日券がお得です！", fill=COLORS['accent_pink'], 
              anchor="lt", font=get_font(11, bold=True))
    
    bg.save("screenshots/travel_planner.png")
    print("✅ Created travel_planner.png")

def create_fitness_coach():
    """Fitness coaching demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "フィットネスコーチ", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(16, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User request
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 60)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "初心者向けの", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "筋トレメニューを教えて", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 80
    
    # AI fitness response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 280)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_green'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_green'])
    draw.text((35, y_pos + 20), "💪", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "パーソナルトレーナー", fill=COLORS['accent_green'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Workout plan
    draw.text((30, y_pos + 50), "🏋️ 初心者向け全身メニュー", fill=COLORS['accent_blue'], 
              anchor="lt", font=get_font(13, bold=True))
    
    exercises = [
        ("腕立て伏せ", "10回 × 3セット", COLORS['accent_red']),
        ("スクワット", "15回 × 3セット", COLORS['accent_orange']),
        ("プランク", "30秒 × 3セット", COLORS['accent_purple']),
        ("腹筋", "10回 × 3セット", COLORS['accent_pink']),
        ("背筋", "10回 × 3セット", COLORS['accent_cyan'])
    ]
    
    exercise_y = y_pos + 80
    for exercise, reps, color in exercises:
        draw.text((40, exercise_y), f"• {exercise}", fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(12))
        draw.text((WIDTH - 80, exercise_y), reps, fill=color, 
                  anchor="rt", font=get_font(11, bold=True))
        exercise_y += 25
    
    # Rest periods
    draw.text((30, y_pos + 210), "⏰ セット間休憩：60秒", fill=COLORS['accent_blue'], 
              anchor="lt", font=get_font(12))
    draw.text((30, y_pos + 230), "📅 頻度：週3回（1日おき）", fill=COLORS['accent_green'], 
              anchor="lt", font=get_font(12))
    
    # Motivation
    draw.text((30, y_pos + 260), "🔥 継続は力なり！頑張って！", fill=COLORS['accent_orange'], 
              anchor="lt", font=get_font(12, bold=True))
    
    bg.save("screenshots/fitness_coach.png")
    print("✅ Created fitness_coach.png")

def create_business_advisor():
    """Business consulting demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "ビジネスアドバイザー", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(16, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User question
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 80)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "スタートアップで", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "効果的な資金調達方法", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 55), "を教えて", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 100
    
    # AI business response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 300)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_blue'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_blue'])
    draw.text((35, y_pos + 20), "💼", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "経営コンサルタント", fill=COLORS['accent_blue'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Funding options
    draw.text((30, y_pos + 50), "💰 主な資金調達方法：", fill=COLORS['accent_green'], 
              anchor="lt", font=get_font(13, bold=True))
    
    funding_methods = [
        ("エンジェル投資", "個人投資家からの初期資金", COLORS['accent_purple']),
        ("VC（ベンチャーキャピタル）", "機関投資家による大型調達", COLORS['accent_blue']),
        ("クラウドファンディング", "一般からの小口資金調達", COLORS['accent_green']),
        ("政府系補助金", "スタートアップ支援制度", COLORS['accent_orange']),
        ("銀行融資", "担保・保証付き借入", COLORS['accent_cyan'])
    ]
    
    method_y = y_pos + 80
    for method, description, color in funding_methods:
        draw.text((40, method_y), f"• {method}", fill=color, 
                  anchor="lt", font=get_font(12, bold=True))
        draw.text((50, method_y + 15), description, fill=COLORS['text_secondary'], 
                  anchor="lt", font=get_font(10))
        method_y += 40
    
    # Key advice
    draw.text((30, y_pos + 260), "📈 成功のポイント：", fill=COLORS['accent_red'], 
              anchor="lt", font=get_font(12, bold=True))
    draw.text((30, y_pos + 280), "事業計画書の完成度が重要！", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(11))
    
    bg.save("screenshots/business_advisor.png")
    print("✅ Created business_advisor.png")

# Generate all extended demos
create_creative_writing_demo()
create_language_learning_demo()
create_cooking_assistant()
create_travel_planner()
create_fitness_coach()
create_business_advisor()

print("\n🎨 All extended demo screens generated!")