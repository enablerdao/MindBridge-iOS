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
    'accent_orange': "#FF9F0A",
    'accent_red': "#FF453A",
    'accent_pink': "#FF2D92",
    'accent_cyan': "#32D74B",
    'text_primary': "#FFFFFF",
    'text_secondary': "#8E8E93",
    'user_bubble': "#007AFF",
    'ai_bubble': "#2C2C2E",
}

def get_font(size=16, bold=False):
    try:
        if bold:
            return ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", size)
        else:
            return ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", size)
    except:
        return ImageFont.load_default()

def create_gradient(width, height, start_color, end_color):
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

def create_medical_consultation():
    """Medical consultation demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "健康相談アシスタント", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(16, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User symptom
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 80)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "最近肩こりがひどくて", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "改善方法を教えて", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 55), "ください 🏥", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 100
    
    # AI medical response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 320)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_red'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_red'])
    draw.text((35, y_pos + 20), "⚕️", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "健康アドバイザー", fill=COLORS['accent_red'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Warning
    draw.rounded_rectangle([(30, y_pos + 45), (WIDTH - 70, y_pos + 65)], 
                          radius=8, fill=COLORS['accent_orange'])
    draw.text((35, y_pos + 50), "⚠️ 医療診断ではありません", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(10, bold=True))
    
    # Remedies
    draw.text((30, y_pos + 80), "🧘 肩こり改善法：", fill=COLORS['accent_green'], 
              anchor="lt", font=get_font(13, bold=True))
    
    remedies = [
        "• 肩甲骨ストレッチ（1日3回）",
        "• 温湿布で血行促進",
        "• デスクワーク時の姿勢改善",
        "• 適度な運動（ウォーキング等）",
        "• 十分な睡眠（7-8時間）"
    ]
    
    remedy_y = y_pos + 105
    for remedy in remedies:
        draw.text((40, remedy_y), remedy, fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(11))
        remedy_y += 20
    
    # Exercise demo
    draw.text((30, y_pos + 210), "🤸 簡単ストレッチ：", fill=COLORS['accent_blue'], 
              anchor="lt", font=get_font(12, bold=True))
    
    exercises = [
        "1. 肩を上下に10回動かす",
        "2. 首を左右にゆっくり回す",
        "3. 肩甲骨を寄せて5秒キープ"
    ]
    
    exercise_y = y_pos + 235
    for exercise in exercises:
        draw.text((40, exercise_y), exercise, fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(11))
        exercise_y += 18
    
    # Disclaimer
    draw.text((30, y_pos + 295), "🏥 症状が続く場合は医師にご相談を", fill=COLORS['accent_red'], 
              anchor="lt", font=get_font(10))
    
    bg.save("screenshots/medical_consultation.png")
    print("✅ Created medical_consultation.png")

def create_legal_advisor():
    """Legal advice demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "法律相談アシスタント", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(16, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User question
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 80)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "賃貸契約の敷金について", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "退去時の返金ルールを", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 55), "教えて ⚖️", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 100
    
    # AI legal response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 300)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_purple'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_purple'])
    draw.text((35, y_pos + 20), "⚖️", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "法律アドバイザー", fill=COLORS['accent_purple'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Legal info
    draw.text((30, y_pos + 50), "📖 敷金返金の基本原則：", fill=COLORS['accent_blue'], 
              anchor="lt", font=get_font(13, bold=True))
    
    legal_points = [
        "• 自然損耗は借主負担なし",
        "• 故意・過失の損傷は借主負担", 
        "• 原状回復費用の明細提示義務",
        "• 6ヶ月以内の返金が原則",
        "• 国土交通省ガイドライン準拠"
    ]
    
    legal_y = y_pos + 75
    for point in legal_points:
        draw.text((40, legal_y), point, fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(11))
        legal_y += 20
    
    # Practical advice
    draw.text((30, y_pos + 180), "💡 実践的アドバイス：", fill=COLORS['accent_green'], 
              anchor="lt", font=get_font(12, bold=True))
    
    advice_items = [
        "入居時の写真撮影を推奨",
        "契約書の特約事項を確認",
        "退去立会いに必ず参加"
    ]
    
    advice_y = y_pos + 205
    for advice in advice_items:
        draw.text((40, advice_y), f"• {advice}", fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(11))
        advice_y += 18
    
    # Disclaimer
    draw.rounded_rectangle([(30, y_pos + 265), (WIDTH - 70, y_pos + 285)], 
                          radius=8, fill=COLORS['accent_orange'])
    draw.text((35, y_pos + 270), "⚠️ 一般的な情報です。専門家にご相談を", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(9))
    
    bg.save("screenshots/legal_advisor.png")
    print("✅ Created legal_advisor.png")

def create_financial_planner():
    """Financial planning demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "資産運用アドバイザー", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(16, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User question
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 80)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "20代からできる", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "おすすめの投資方法", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 55), "を教えて 💰", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 100
    
    # AI financial response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 320)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_green'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_green'])
    draw.text((35, y_pos + 20), "💹", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "ファイナンシャルプランナー", fill=COLORS['accent_green'], 
              anchor="lm", font=get_font(12, bold=True))
    
    # Investment options
    draw.text((30, y_pos + 50), "📈 20代におすすめの投資：", fill=COLORS['accent_blue'], 
              anchor="lt", font=get_font(13, bold=True))
    
    investments = [
        ("つみたてNISA", "月3.3万円まで非課税", COLORS['accent_green'], "低リスク"),
        ("iDeCo", "老後資金＋節税効果", COLORS['accent_blue'], "長期運用"),
        ("インデックス投資", "市場全体に分散投資", COLORS['accent_purple'], "中リスク"),
        ("米国株ETF", "成長市場への投資", COLORS['accent_orange'], "中リスク")
    ]
    
    invest_y = y_pos + 75
    for name, desc, color, risk in investments:
        draw.text((40, invest_y), f"• {name}", fill=color, 
                  anchor="lt", font=get_font(12, bold=True))
        draw.text((50, invest_y + 15), desc, fill=COLORS['text_secondary'], 
                  anchor="lt", font=get_font(10))
        draw.text((WIDTH - 80, invest_y + 15), risk, fill=color, 
                  anchor="rt", font=get_font(9))
        invest_y += 40
    
    # Key principles
    draw.text((30, y_pos + 235), "💎 投資の基本原則：", fill=COLORS['accent_pink'], 
              anchor="lt", font=get_font(12, bold=True))
    
    principles = [
        "長期投資で複利効果を活用",
        "分散投資でリスクを軽減",
        "定期積立で時間分散"
    ]
    
    principle_y = y_pos + 260
    for principle in principles:
        draw.text((40, principle_y), f"• {principle}", fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(11))
        principle_y += 18
    
    bg.save("screenshots/financial_planner.png")
    print("✅ Created financial_planner.png")

def create_study_buddy():
    """Study assistance demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "学習サポーター", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(16, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User question
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 60)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "効率的な暗記方法を", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "教えて 📚", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 80
    
    # AI study response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 300)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_blue'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_blue'])
    draw.text((35, y_pos + 20), "🎓", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "学習コーチ", fill=COLORS['accent_blue'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Memory techniques
    draw.text((30, y_pos + 50), "🧠 効率的暗記テクニック：", fill=COLORS['accent_purple'], 
              anchor="lt", font=get_font(13, bold=True))
    
    techniques = [
        ("スペース反復法", "間隔を空けて繰り返し復習", COLORS['accent_green']),
        ("連想記憶術", "既知の情報と関連付け", COLORS['accent_orange']),
        ("アクティブリコール", "思い出すことを重視", COLORS['accent_cyan']),
        ("視覚化", "イメージで記憶を強化", COLORS['accent_pink'])
    ]
    
    tech_y = y_pos + 75
    for technique, description, color in techniques:
        draw.text((40, tech_y), f"• {technique}", fill=color, 
                  anchor="lt", font=get_font(12, bold=True))
        draw.text((50, tech_y + 15), description, fill=COLORS['text_secondary'], 
                  anchor="lt", font=get_font(10))
        tech_y += 35
    
    # Study schedule
    draw.text((30, y_pos + 215), "📅 推奨学習スケジュール：", fill=COLORS['accent_red'], 
              anchor="lt", font=get_font(12, bold=True))
    
    schedule = [
        "1日目：新規学習",
        "3日目：1回目復習", 
        "1週間後：2回目復習",
        "1ヶ月後：3回目復習"
    ]
    
    schedule_y = y_pos + 240
    for item in schedule:
        draw.text((40, schedule_y), f"• {item}", fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(11))
        schedule_y += 18
    
    bg.save("screenshots/study_buddy.png")
    print("✅ Created study_buddy.png")

def create_design_consultant():
    """Design consultation demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "デザインコンサルタント", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(16, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User question
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 80)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "モバイルアプリの", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "UI/UXデザインのコツ", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 55), "を教えて 🎨", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 100
    
    # AI design response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 300)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_pink'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_pink'])
    draw.text((35, y_pos + 20), "🎨", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "UI/UXデザイナー", fill=COLORS['accent_pink'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Design principles
    draw.text((30, y_pos + 50), "✨ UI/UXデザインの原則：", fill=COLORS['accent_blue'], 
              anchor="lt", font=get_font(13, bold=True))
    
    principles = [
        ("ユーザー中心設計", "ユーザーのニーズを最優先", COLORS['accent_green']),
        ("シンプリシティ", "不要な要素を削ぎ落とす", COLORS['accent_blue']),
        ("一貫性", "統一されたデザインルール", COLORS['accent_purple']),
        ("アクセシビリティ", "誰でも使いやすいデザイン", COLORS['accent_orange'])
    ]
    
    principle_y = y_pos + 75
    for principle, description, color in principles:
        draw.text((40, principle_y), f"• {principle}", fill=color, 
                  anchor="lt", font=get_font(12, bold=True))
        draw.text((50, principle_y + 15), description, fill=COLORS['text_secondary'], 
                  anchor="lt", font=get_font(10))
        principle_y += 35
    
    # Practical tips
    draw.text((30, y_pos + 215), "🛠️ 実践的なコツ：", fill=COLORS['accent_cyan'], 
              anchor="lt", font=get_font(12, bold=True))
    
    tips = [
        "44px以上のタッチターゲット",
        "十分なコントラスト比を確保",
        "読みやすいフォントサイズ（14px+）",
        "適切な余白でスペースを活用"
    ]
    
    tip_y = y_pos + 240
    for tip in tips:
        draw.text((40, tip_y), f"• {tip}", fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(11))
        tip_y += 18
    
    bg.save("screenshots/design_consultant.png")
    print("✅ Created design_consultant.png")

def create_mental_health_support():
    """Mental health support demo"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "メンタルヘルスサポート", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(15, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User concern
    draw.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 60)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 15), "最近ストレスが多くて", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    draw.text((WIDTH - 30, y_pos + 35), "リラックス方法は？", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 80
    
    # AI support response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 320)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_cyan'], width=1)
    
    draw.circle((35, y_pos + 20), 12, fill=COLORS['accent_cyan'])
    draw.text((35, y_pos + 20), "🧘", fill=COLORS['text_primary'], anchor="mm", font=get_font(14))
    
    draw.text((55, y_pos + 20), "ウェルネスコーチ", fill=COLORS['accent_cyan'], 
              anchor="lm", font=get_font(13, bold=True))
    
    # Relaxation techniques
    draw.text((30, y_pos + 50), "🌸 リラクゼーション法：", fill=COLORS['accent_green'], 
              anchor="lt", font=get_font(13, bold=True))
    
    techniques = [
        ("深呼吸法", "4秒吸って8秒で吐く", COLORS['accent_blue']),
        ("瞑想", "1日10分の静寂タイム", COLORS['accent_purple']),
        ("プログレッシブ筋弛緩", "筋肉の緊張と弛緩を繰り返す", COLORS['accent_green']),
        ("自然散歩", "緑の中でのウォーキング", COLORS['accent_orange'])
    ]
    
    tech_y = y_pos + 75
    for technique, description, color in techniques:
        draw.text((40, tech_y), f"• {technique}", fill=color, 
                  anchor="lt", font=get_font(12, bold=True))
        draw.text((50, tech_y + 15), description, fill=COLORS['text_secondary'], 
                  anchor="lt", font=get_font(10))
        tech_y += 35
    
    # Lifestyle tips
    draw.text((30, y_pos + 215), "💡 ライフスタイルのヒント：", fill=COLORS['accent_pink'], 
              anchor="lt", font=get_font(12, bold=True))
    
    lifestyle_tips = [
        "規則正しい睡眠リズム",
        "適度な運動習慣",
        "バランスの取れた食事",
        "人との繋がりを大切に"
    ]
    
    lifestyle_y = y_pos + 240
    for tip in lifestyle_tips:
        draw.text((40, lifestyle_y), f"• {tip}", fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(11))
        lifestyle_y += 18
    
    # Support note
    draw.rounded_rectangle([(30, y_pos + 290), (WIDTH - 70, y_pos + 310)], 
                          radius=8, fill=COLORS['accent_cyan'])
    draw.text((35, y_pos + 295), "💙 つらい時は専門家に相談してくださいね", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(9))
    
    bg.save("screenshots/mental_health_support.png")
    print("✅ Created mental_health_support.png")

# Generate all professional demos
create_medical_consultation()
create_legal_advisor()
create_financial_planner()
create_study_buddy()
create_design_consultant()
create_mental_health_support()

print("\n🏥 All professional demo screens generated!")