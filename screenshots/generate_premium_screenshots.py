#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import platform
import math

# Create screenshots directory
os.makedirs("screenshots", exist_ok=True)

# iPhone 14 Pro dimensions
WIDTH = 393
HEIGHT = 852
SAFE_AREA_TOP = 59
SAFE_AREA_BOTTOM = 34

# Premium Colors & Gradients
COLORS = {
    'bg_primary': "#0A0A0A",
    'bg_secondary': "#1C1C1E", 
    'card_dark': "#2C2C2E",
    'card_light': "#3A3A3C",
    'accent_blue': "#007AFF",
    'accent_purple': "#AF52DE",
    'accent_green': "#30D158",
    'text_primary': "#FFFFFF",
    'text_secondary': "#8E8E93",
    'text_tertiary': "#48484A",
    'user_bubble': "#007AFF",
    'ai_bubble': "#2C2C2E",
    'success': "#30D158",
    'warning': "#FF9F0A",
    'error': "#FF453A"
}

# Font setup
def get_font(size=16, bold=False):
    """Get appropriate font for the system"""
    try:
        if platform.system() == "Darwin":  # macOS
            if bold:
                return ImageFont.truetype("/System/Library/Fonts/SF-Pro-Display-Bold.otf", size)
            else:
                return ImageFont.truetype("/System/Library/Fonts/SF-Pro-Display-Regular.otf", size)
        else:
            return ImageFont.load_default()
    except:
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

def add_glow_effect(img, color, radius=10):
    """Add glow effect to elements"""
    return img.filter(ImageFilter.GaussianBlur(radius=radius))

def create_modern_chat_screen():
    """Create modern chat screen"""
    # Gradient background
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Status bar with blur effect
    status_bg = Image.new('RGBA', (WIDTH, SAFE_AREA_TOP), (28, 28, 30, 200))
    bg.paste(status_bg, (0, 0), status_bg)
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH-20, 15), "100% 🔋", fill=COLORS['success'], anchor="rt", font=get_font(12))
    
    # Modern navigation bar
    nav_bg = Image.new('RGBA', (WIDTH, 44), (44, 44, 46, 220))
    bg.paste(nav_bg, (0, SAFE_AREA_TOP), nav_bg)
    
    # Navigation title with gradient text effect
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "Qwen3-4B Chat", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(18, bold=True))
    
    # Settings icon with subtle glow
    draw.text((WIDTH - 25, SAFE_AREA_TOP + 22), "⚙️", fill=COLORS['accent_blue'], 
              anchor="rm", font=get_font(22))
    
    y_pos = SAFE_AREA_TOP + 70
    
    # AI message with premium styling
    ai_bubble_bg = Image.new('RGBA', (WIDTH - 100, 120), (44, 44, 46, 240))
    bg.paste(ai_bubble_bg, (20, y_pos), ai_bubble_bg)
    
    # Add subtle border
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 80, y_pos + 120)], 
                          radius=20, outline=COLORS['accent_purple'], width=1)
    
    # AI avatar
    draw.circle((35, y_pos + 15), 10, fill=COLORS['accent_purple'])
    draw.text((35, y_pos + 15), "🤖", fill=COLORS['text_primary'], anchor="mm", font=get_font(12))
    
    # AI name with typing indicator
    draw.text((55, y_pos + 15), "Qwen3 AI Assistant", fill=COLORS['accent_purple'], 
              anchor="lm", font=get_font(12, bold=True))
    draw.text((30, y_pos + 35), "こんにちは！Qwen3-4Bモデルを搭載した", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(14))
    draw.text((30, y_pos + 55), "最新のAIチャットアシスタントです。", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(14))
    draw.text((30, y_pos + 75), "何でもお気軽にお聞きください！", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(14))
    draw.text((30, y_pos + 95), "💡 日本語での高度な対話が可能です", fill=COLORS['accent_green'], 
              anchor="lt", font=get_font(12))
    
    y_pos += 140
    
    # User message with modern styling
    user_bubble_bg = Image.new('RGBA', (WIDTH - 100, 50), (0, 122, 255, 255))
    bg.paste(user_bubble_bg, (80, y_pos), user_bubble_bg)
    
    draw.rounded_rectangle([(80, y_pos), (WIDTH - 20, y_pos + 50)], 
                          radius=20, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 25), "プログラミングについて教えて！", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14, bold=True))
    
    y_pos += 70
    
    # AI response with code syntax highlighting
    ai_response_bg = Image.new('RGBA', (WIDTH - 80, 140), (44, 44, 46, 240))
    bg.paste(ai_response_bg, (20, y_pos), ai_response_bg)
    
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 140)], 
                          radius=20, outline=COLORS['accent_blue'], width=1)
    
    draw.circle((35, y_pos + 15), 10, fill=COLORS['accent_blue'])
    draw.text((35, y_pos + 15), "🧠", fill=COLORS['text_primary'], anchor="mm", font=get_font(12))
    
    draw.text((55, y_pos + 15), "Qwen3", fill=COLORS['accent_blue'], 
              anchor="lm", font=get_font(12, bold=True))
    
    # Response with syntax highlighting
    draw.text((30, y_pos + 35), "プログラミングは創造性と論理性を", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(14))
    draw.text((30, y_pos + 55), "組み合わせた素晴らしい分野です！", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(14))
    
    # Code example with syntax highlighting
    code_bg = Image.new('RGBA', (WIDTH - 120, 40), (20, 20, 20, 255))
    bg.paste(code_bg, (40, y_pos + 75), code_bg)
    draw.text((50, y_pos + 85), "def hello_world():", fill=COLORS['accent_purple'], 
              anchor="lt", font=get_font(12))
    draw.text((60, y_pos + 100), "print(\"Hello, World!\")", fill=COLORS['accent_green'], 
              anchor="lt", font=get_font(12))
    
    # Modern input bar
    input_y = HEIGHT - SAFE_AREA_BOTTOM - 80
    input_bg = Image.new('RGBA', (WIDTH, 80), (28, 28, 30, 240))
    bg.paste(input_bg, (0, input_y), input_bg)
    
    # Input field with glass morphism effect
    draw.rounded_rectangle([(20, input_y + 15), (WIDTH - 70, input_y + 50)], 
                          radius=25, fill=COLORS['card_dark'], outline=COLORS['text_tertiary'], width=1)
    draw.text((35, input_y + 32), "メッセージを入力...", fill=COLORS['text_secondary'], 
              anchor="lm", font=get_font(14))
    
    # Send button with gradient
    send_btn_bg = create_gradient(45, 35, COLORS['accent_blue'], COLORS['accent_purple'])
    bg.paste(send_btn_bg, (WIDTH - 60, input_y + 22))
    draw.rounded_rectangle([(WIDTH - 60, input_y + 22), (WIDTH - 15, input_y + 57)], 
                          radius=17, outline=COLORS['accent_blue'], width=2)
    draw.text((WIDTH - 37, input_y + 40), "→", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(20, bold=True))
    
    bg.save("screenshots/modern_chat_screen.png")
    print("✅ Created modern_chat_screen.png")

def create_advanced_settings_screen():
    """Create advanced settings screen"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Status bar
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH-20, 15), "100% 🔋", fill=COLORS['success'], anchor="rt", font=get_font(12))
    
    # Navigation
    draw.text((25, SAFE_AREA_TOP + 22), "←", fill=COLORS['accent_blue'], anchor="lm", font=get_font(24, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "設定", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(18, bold=True))
    draw.text((WIDTH - 25, SAFE_AREA_TOP + 22), "保存", fill=COLORS['accent_blue'], 
              anchor="rm", font=get_font(16, bold=True))
    
    y_pos = SAFE_AREA_TOP + 80
    
    # AI Model Section
    draw.text((25, y_pos), "🤖 AIモデル設定", fill=COLORS['accent_purple'], 
              anchor="lt", font=get_font(16, bold=True))
    y_pos += 35
    
    # Model info card
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 20, y_pos + 100)], 
                          radius=15, fill=COLORS['card_dark'], outline=COLORS['accent_blue'], width=1)
    
    # Model status indicator
    draw.circle((35, y_pos + 20), 8, fill=COLORS['success'])
    draw.text((55, y_pos + 20), "Qwen3-4B-Instruct", fill=COLORS['text_primary'], 
              anchor="lm", font=get_font(16, bold=True))
    draw.text((WIDTH - 35, y_pos + 20), "オンライン", fill=COLORS['success'], 
              anchor="rm", font=get_font(12))
    
    draw.text((35, y_pos + 45), "量子化: Q4_K_M • サイズ: 2.7GB", fill=COLORS['text_secondary'], 
              anchor="lt", font=get_font(13))
    draw.text((35, y_pos + 65), "メモリ使用量: 2.1GB / 8.0GB", fill=COLORS['text_secondary'], 
              anchor="lt", font=get_font(13))
    
    # Memory usage bar
    draw.rounded_rectangle([(35, y_pos + 80), (WIDTH - 35, y_pos + 85)], 
                          radius=3, fill=COLORS['text_tertiary'])
    draw.rounded_rectangle([(35, y_pos + 80), (35 + (WIDTH - 70) * 0.26, y_pos + 85)], 
                          radius=3, fill=COLORS['accent_blue'])
    
    y_pos += 120
    
    # Performance Settings
    draw.text((25, y_pos), "⚡ パフォーマンス設定", fill=COLORS['accent_blue'], 
              anchor="lt", font=get_font(16, bold=True))
    y_pos += 35
    
    # Temperature setting
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 20, y_pos + 70)], 
                          radius=15, fill=COLORS['card_dark'])
    
    draw.text((35, y_pos + 15), "Temperature", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(15, bold=True))
    draw.text((WIDTH - 35, y_pos + 15), "0.70", fill=COLORS['accent_purple'], 
              anchor="rm", font=get_font(15, bold=True))
    draw.text((35, y_pos + 35), "創造性と一貫性のバランス", fill=COLORS['text_secondary'], 
              anchor="lt", font=get_font(12))
    
    # Slider
    draw.rounded_rectangle([(35, y_pos + 50), (WIDTH - 35, y_pos + 55)], 
                          radius=3, fill=COLORS['text_tertiary'])
    slider_pos = 35 + (WIDTH - 70) * 0.7
    draw.rounded_rectangle([(35, y_pos + 50), (slider_pos, y_pos + 55)], 
                          radius=3, fill=COLORS['accent_purple'])
    draw.circle((slider_pos, y_pos + 52), 8, fill=COLORS['accent_purple'], outline=COLORS['text_primary'], width=2)
    
    y_pos += 90
    
    # Max tokens setting
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 20, y_pos + 70)], 
                          radius=15, fill=COLORS['card_dark'])
    
    draw.text((35, y_pos + 15), "最大トークン数", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(15, bold=True))
    draw.text((WIDTH - 35, y_pos + 15), "512", fill=COLORS['accent_blue'], 
              anchor="rm", font=get_font(15, bold=True))
    draw.text((35, y_pos + 35), "レスポンスの最大長", fill=COLORS['text_secondary'], 
              anchor="lt", font=get_font(12))
    
    # Slider
    draw.rounded_rectangle([(35, y_pos + 50), (WIDTH - 35, y_pos + 55)], 
                          radius=3, fill=COLORS['text_tertiary'])
    slider_pos = 35 + (WIDTH - 70) * 0.5
    draw.rounded_rectangle([(35, y_pos + 50), (slider_pos, y_pos + 55)], 
                          radius=3, fill=COLORS['accent_blue'])
    draw.circle((slider_pos, y_pos + 52), 8, fill=COLORS['accent_blue'], outline=COLORS['text_primary'], width=2)
    
    y_pos += 90
    
    # Advanced options
    draw.text((25, y_pos), "🔧 高度な設定", fill=COLORS['accent_green'], 
              anchor="lt", font=get_font(16, bold=True))
    y_pos += 35
    
    # GPU acceleration toggle
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 20, y_pos + 50)], 
                          radius=15, fill=COLORS['card_dark'])
    
    draw.text((35, y_pos + 15), "Metal GPU加速", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(15, bold=True))
    draw.text((35, y_pos + 30), "ハードウェア加速で高速化", fill=COLORS['text_secondary'], 
              anchor="lt", font=get_font(12))
    
    # Toggle switch
    toggle_bg = COLORS['success']
    draw.rounded_rectangle([(WIDTH - 70, y_pos + 20), (WIDTH - 35, y_pos + 35)], 
                          radius=8, fill=toggle_bg)
    draw.circle((WIDTH - 45, y_pos + 27), 6, fill=COLORS['text_primary'])
    
    bg.save("screenshots/advanced_settings.png")
    print("✅ Created advanced_settings.png")

def create_loading_animation_screen():
    """Create animated loading screen"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    center_y = HEIGHT // 2
    
    # App logo with glow effect
    logo_size = 80
    logo_bg = create_gradient(logo_size, logo_size, COLORS['accent_blue'], COLORS['accent_purple'])
    bg.paste(logo_bg, (WIDTH//2 - logo_size//2, center_y - 120))
    
    draw.rounded_rectangle([(WIDTH//2 - logo_size//2, center_y - 120), 
                           (WIDTH//2 + logo_size//2, center_y - 40)], 
                          radius=20, outline=COLORS['text_primary'], width=2)
    draw.text((WIDTH//2, center_y - 80), "Q", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(40, bold=True))
    
    # App title
    draw.text((WIDTH//2, center_y - 10), "Qwen3-4B Chat", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(28, bold=True))
    draw.text((WIDTH//2, center_y + 20), "Powered by llama.cpp", fill=COLORS['text_secondary'], 
              anchor="mm", font=get_font(14))
    
    # Loading text with animation dots
    draw.text((WIDTH//2, center_y + 60), "AIモデルを初期化中", fill=COLORS['accent_blue'], 
              anchor="mm", font=get_font(16, bold=True))
    
    # Animated progress indicator
    progress_width = WIDTH - 80
    progress_x = 40
    progress_y = center_y + 100
    
    # Background track
    draw.rounded_rectangle([(progress_x, progress_y), (progress_x + progress_width, progress_y + 8)], 
                          radius=4, fill=COLORS['text_tertiary'])
    
    # Progress fill with gradient
    progress_fill = create_gradient(int(progress_width * 0.75), 8, COLORS['accent_blue'], COLORS['accent_purple'], 'horizontal')
    bg.paste(progress_fill, (progress_x, progress_y))
    
    draw.text((WIDTH//2, progress_y + 25), "75%", fill=COLORS['text_secondary'], 
              anchor="mt", font=get_font(14))
    
    # Status messages
    draw.text((progress_x, progress_y + 50), "✓ モデルファイルを検証", fill=COLORS['success'], 
              anchor="lt", font=get_font(13))
    draw.text((progress_x, progress_y + 70), "✓ Metal GPUを初期化", fill=COLORS['success'], 
              anchor="lt", font=get_font(13))
    draw.text((progress_x, progress_y + 90), "⏳ メモリに展開中...", fill=COLORS['warning'], 
              anchor="lt", font=get_font(13))
    
    bg.save("screenshots/loading_animation.png")
    print("✅ Created loading_animation.png")

def create_conversation_examples():
    """Create multiple conversation examples"""
    
    # Programming conversation
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "Qwen3-4B Chat", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(18, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User question
    draw.rounded_rectangle([(80, y_pos), (WIDTH - 20, y_pos + 40)], 
                          radius=18, fill=COLORS['user_bubble'])
    draw.text((WIDTH - 30, y_pos + 20), "Swiftで配列をソートする方法は？", fill=COLORS['text_primary'], 
              anchor="rm", font=get_font(14))
    y_pos += 60
    
    # AI response with code
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 200)], 
                          radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_blue'], width=1)
    
    draw.circle((35, y_pos + 15), 10, fill=COLORS['accent_blue'])
    draw.text((35, y_pos + 15), "🧠", fill=COLORS['text_primary'], anchor="mm", font=get_font(12))
    
    draw.text((30, y_pos + 35), "Swiftでの配列ソート方法をご紹介します：", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(14))
    
    # Code block
    code_y = y_pos + 60
    draw.rounded_rectangle([(30, code_y), (WIDTH - 70, code_y + 100)], 
                          radius=8, fill=COLORS['bg_primary'])
    
    draw.text((40, code_y + 10), "// 昇順ソート", fill=COLORS['text_secondary'], 
              anchor="lt", font=get_font(12))
    draw.text((40, code_y + 25), "let numbers = [3, 1, 4, 1, 5]", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(12))
    draw.text((40, code_y + 40), "let sorted = numbers.sorted()", fill=COLORS['accent_green'], 
              anchor="lt", font=get_font(12))
    draw.text((40, code_y + 55), "// [1, 1, 3, 4, 5]", fill=COLORS['text_secondary'], 
              anchor="lt", font=get_font(12))
    draw.text((40, code_y + 75), "numbers.sort() // in-place", fill=COLORS['accent_purple'], 
              anchor="lt", font=get_font(12))
    
    draw.text((30, y_pos + 170), "より詳しい説明が必要でしたら", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(13))
    draw.text((30, y_pos + 185), "お気軽にお聞きください！", fill=COLORS['text_primary'], 
              anchor="lt", font=get_font(13))
    
    bg.save("screenshots/programming_conversation.png")
    print("✅ Created programming_conversation.png")
    
    # Japanese conversation
    bg2 = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw2 = ImageDraw.Draw(bg2)
    
    # Header
    draw2.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw2.text((WIDTH//2, SAFE_AREA_TOP + 22), "Qwen3-4B Chat", fill=COLORS['text_primary'], 
               anchor="mm", font=get_font(18, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # User message
    draw2.rounded_rectangle([(60, y_pos), (WIDTH - 20, y_pos + 60)], 
                           radius=18, fill=COLORS['user_bubble'])
    draw2.text((WIDTH - 30, y_pos + 15), "日本の伝統文化について", fill=COLORS['text_primary'], 
               anchor="rm", font=get_font(14))
    draw2.text((WIDTH - 30, y_pos + 35), "教えてもらえますか？🇯🇵", fill=COLORS['text_primary'], 
               anchor="rm", font=get_font(14))
    y_pos += 80
    
    # AI response
    draw2.rounded_rectangle([(20, y_pos), (WIDTH - 60, y_pos + 160)], 
                           radius=18, fill=COLORS['ai_bubble'], outline=COLORS['accent_purple'], width=1)
    
    draw2.circle((35, y_pos + 15), 10, fill=COLORS['accent_purple'])
    draw2.text((35, y_pos + 15), "🗾", fill=COLORS['text_primary'], anchor="mm", font=get_font(12))
    
    draw2.text((30, y_pos + 35), "日本の伝統文化は非常に豊かで", fill=COLORS['text_primary'], 
               anchor="lt", font=get_font(14))
    draw2.text((30, y_pos + 55), "多様性に富んでいます：", fill=COLORS['text_primary'], 
               anchor="lt", font=get_font(14))
    
    draw2.text((30, y_pos + 80), "🎭 歌舞伎・能楽", fill=COLORS['accent_green'], 
               anchor="lt", font=get_font(13))
    draw2.text((30, y_pos + 100), "🍃 茶道・華道", fill=COLORS['accent_blue'], 
               anchor="lt", font=get_font(13))
    draw2.text((30, y_pos + 120), "🗾 着物・書道", fill=COLORS['accent_purple'], 
               anchor="lt", font=get_font(13))
    draw2.text((30, y_pos + 140), "どの分野に興味がありますか？", fill=COLORS['text_primary'], 
               anchor="lt", font=get_font(13))
    
    bg2.save("screenshots/japanese_conversation.png")
    print("✅ Created japanese_conversation.png")

def create_model_comparison_screen():
    """Create model comparison screen"""
    bg = create_gradient(WIDTH, HEIGHT, COLORS['bg_primary'], COLORS['bg_secondary'])
    draw = ImageDraw.Draw(bg)
    
    # Header
    draw.text((20, 15), "9:41", fill=COLORS['text_primary'], anchor="lt", font=get_font(14, bold=True))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "モデル選択", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(18, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # Description
    draw.text((25, y_pos), "💡 最適なモデルを選択してください", fill=COLORS['accent_blue'], 
              anchor="lt", font=get_font(14, bold=True))
    y_pos += 40
    
    # Model cards
    models = [
        {
            'name': 'Qwen3-4B Q4_K_M',
            'size': '2.7GB',
            'desc': 'バランス型（推奨）',
            'speed': '⚡ 40-50 トークン/秒',
            'quality': '🎯 高品質',
            'color': COLORS['success'],
            'selected': True
        },
        {
            'name': 'Qwen3-4B Q5_K_M',
            'size': '3.2GB', 
            'desc': '高品質モード',
            'speed': '⚡ 35-45 トークン/秒',
            'quality': '🏆 最高品質',
            'color': COLORS['accent_blue'],
            'selected': False
        },
        {
            'name': 'Qwen3-4B Q6_K',
            'size': '3.8GB',
            'desc': 'プレミアム品質',
            'speed': '⚡ 30-40 トークン/秒', 
            'quality': '💎 完璧',
            'color': COLORS['accent_purple'],
            'selected': False
        }
    ]
    
    for model in models:
        card_height = 100
        outline_color = model['color'] if model['selected'] else COLORS['text_tertiary']
        outline_width = 2 if model['selected'] else 1
        
        draw.rounded_rectangle([(20, y_pos), (WIDTH - 20, y_pos + card_height)], 
                              radius=15, fill=COLORS['card_dark'], outline=outline_color, width=outline_width)
        
        # Selection indicator
        if model['selected']:
            draw.circle((WIDTH - 35, y_pos + 20), 8, fill=model['color'])
            draw.text((WIDTH - 35, y_pos + 20), "✓", fill=COLORS['text_primary'], 
                      anchor="mm", font=get_font(12, bold=True))
        
        # Model info
        draw.text((30, y_pos + 15), model['name'], fill=COLORS['text_primary'], 
                  anchor="lt", font=get_font(16, bold=True))
        draw.text((30, y_pos + 35), f"{model['size']} • {model['desc']}", fill=model['color'], 
                  anchor="lt", font=get_font(13))
        draw.text((30, y_pos + 55), model['speed'], fill=COLORS['text_secondary'], 
                  anchor="lt", font=get_font(12))
        draw.text((30, y_pos + 75), model['quality'], fill=COLORS['text_secondary'], 
                  anchor="lt", font=get_font(12))
        
        y_pos += card_height + 15
    
    # Download button
    y_pos += 20
    download_bg = create_gradient(WIDTH - 80, 50, COLORS['accent_blue'], COLORS['accent_purple'])
    bg.paste(download_bg, (40, y_pos))
    draw.rounded_rectangle([(40, y_pos), (WIDTH - 40, y_pos + 50)], 
                          radius=25, outline=COLORS['text_primary'], width=2)
    draw.text((WIDTH//2, y_pos + 25), "💾 ダウンロード開始", fill=COLORS['text_primary'], 
              anchor="mm", font=get_font(16, bold=True))
    
    bg.save("screenshots/model_comparison.png")
    print("✅ Created model_comparison.png")

# Generate all premium screenshots
create_modern_chat_screen()
create_advanced_settings_screen()
create_loading_animation_screen()
create_conversation_examples()
create_model_comparison_screen()

print("\n🎨 All premium screenshots generated!")