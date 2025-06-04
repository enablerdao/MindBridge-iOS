#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import platform

# Create screenshots directory
os.makedirs("screenshots", exist_ok=True)

# iPhone 14 Pro dimensions
WIDTH = 393
HEIGHT = 852
SAFE_AREA_TOP = 59
SAFE_AREA_BOTTOM = 34

# Colors
BACKGROUND = "#F2F2F7"
CARD_WHITE = "#FFFFFF"
USER_BUBBLE = "#007AFF"
AI_BUBBLE = "#E9E9EB"
TEXT_PRIMARY = "#000000"
TEXT_SECONDARY = "#8E8E93"
ACCENT_COLOR = "#007AFF"

# Font setup
def get_font(size=16, bold=False):
    """Get appropriate font for the system"""
    try:
        if platform.system() == "Darwin":  # macOS
            if bold:
                return ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", size)
            else:
                return ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", size)
        else:
            # Fallback to default
            return ImageFont.load_default()
    except:
        return ImageFont.load_default()

def create_chat_screen():
    """Create main chat screen"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(img)
    
    # Status bar
    draw.rectangle([(0, 0), (WIDTH, SAFE_AREA_TOP)], fill=CARD_WHITE)
    draw.text((WIDTH//2, 15), "9:41", fill=TEXT_PRIMARY, anchor="mt", font=get_font(14))
    
    # Navigation bar
    draw.rectangle([(0, SAFE_AREA_TOP), (WIDTH, SAFE_AREA_TOP + 44)], fill=CARD_WHITE)
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "Qwen3-4B Chat", fill=TEXT_PRIMARY, anchor="mm", font=get_font(17, bold=True))
    draw.text((WIDTH - 20, SAFE_AREA_TOP + 22), "⚙️", fill=ACCENT_COLOR, anchor="rm", font=get_font(20))
    
    # Chat messages
    y_pos = SAFE_AREA_TOP + 60
    
    # AI message
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 80, y_pos + 100)], 
                          radius=16, fill=AI_BUBBLE)
    draw.text((30, y_pos + 10), "Qwen3", fill=TEXT_SECONDARY, anchor="lt", font=get_font(12))
    draw.text((30, y_pos + 30), "こんにちは！Qwen3-4Bモデル", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    draw.text((30, y_pos + 50), "を使用したチャットアプリです。", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    draw.text((30, y_pos + 70), "何かお手伝いできることは", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    draw.text((30, y_pos + 90), "ありますか？", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    
    y_pos += 120
    
    # User message
    draw.rounded_rectangle([(80, y_pos), (WIDTH - 20, y_pos + 40)], 
                          radius=16, fill=USER_BUBBLE)
    draw.text((WIDTH - 30, y_pos + 20), "こんにちは！", fill=CARD_WHITE, anchor="rm", font=get_font(15))
    
    y_pos += 60
    
    # AI response
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 80, y_pos + 60)], 
                          radius=16, fill=AI_BUBBLE)
    draw.text((30, y_pos + 10), "Qwen3", fill=TEXT_SECONDARY, anchor="lt", font=get_font(12))
    draw.text((30, y_pos + 30), "こんにちは！今日は", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    draw.text((30, y_pos + 50), "どのようなお手伝いが", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    
    # Input bar
    input_y = HEIGHT - SAFE_AREA_BOTTOM - 60
    draw.rectangle([(0, input_y), (WIDTH, HEIGHT - SAFE_AREA_BOTTOM)], fill=CARD_WHITE)
    draw.rounded_rectangle([(20, input_y + 10), (WIDTH - 60, input_y + 40)], 
                          radius=20, fill="#F2F2F7", outline="#E5E5EA")
    draw.text((30, input_y + 25), "メッセージを入力...", fill=TEXT_SECONDARY, anchor="lm", font=get_font(14))
    draw.circle((WIDTH - 35, input_y + 25), 16, fill=ACCENT_COLOR)
    draw.text((WIDTH - 35, input_y + 25), "➤", fill=CARD_WHITE, anchor="mm", font=get_font(16))
    
    img.save("screenshots/chat_screen.png")
    print("✅ Created chat_screen.png")

def create_settings_screen():
    """Create settings screen"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(img)
    
    # Status bar
    draw.rectangle([(0, 0), (WIDTH, SAFE_AREA_TOP)], fill=CARD_WHITE)
    draw.text((WIDTH//2, 15), "9:41", fill=TEXT_PRIMARY, anchor="mt", font=get_font(14))
    
    # Navigation bar
    draw.rectangle([(0, SAFE_AREA_TOP), (WIDTH, SAFE_AREA_TOP + 44)], fill=CARD_WHITE)
    draw.text((20, SAFE_AREA_TOP + 22), "⬅️", fill=ACCENT_COLOR, anchor="lm", font=get_font(20))
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "設定", fill=TEXT_PRIMARY, anchor="mm", font=get_font(17, bold=True))
    draw.text((WIDTH - 20, SAFE_AREA_TOP + 22), "完了", fill=ACCENT_COLOR, anchor="rm", font=get_font(16))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # Model settings section
    draw.text((20, y_pos), "モデル設定", fill=TEXT_SECONDARY, anchor="lt", font=get_font(13))
    y_pos += 30
    
    # Settings card
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 20, y_pos + 180)], 
                          radius=12, fill=CARD_WHITE)
    
    # Temperature
    draw.text((30, y_pos + 20), "Temperature: 0.70", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    draw.rectangle([(30, y_pos + 45), (WIDTH - 30, y_pos + 47)], fill="#E5E5EA")
    draw.circle((30 + (WIDTH - 60) * 0.7, y_pos + 46), 8, fill=ACCENT_COLOR)
    
    # Max tokens
    draw.text((30, y_pos + 70), "最大トークン数: 512", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    draw.rectangle([(30, y_pos + 95), (WIDTH - 30, y_pos + 97)], fill="#E5E5EA")
    draw.circle((30 + (WIDTH - 60) * 0.5, y_pos + 96), 8, fill=ACCENT_COLOR)
    
    # Top-p
    draw.text((30, y_pos + 120), "Top-p: 0.90", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    draw.rectangle([(30, y_pos + 145), (WIDTH - 30, y_pos + 147)], fill="#E5E5EA")
    draw.circle((30 + (WIDTH - 60) * 0.9, y_pos + 146), 8, fill=ACCENT_COLOR)
    
    y_pos += 200
    
    # Model info section
    draw.text((20, y_pos), "モデル情報", fill=TEXT_SECONDARY, anchor="lt", font=get_font(13))
    y_pos += 30
    
    draw.rounded_rectangle([(20, y_pos), (WIDTH - 20, y_pos + 100)], 
                          radius=12, fill=CARD_WHITE)
    draw.text((30, y_pos + 20), "モデル: Qwen3-4B-Instruct", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    draw.text((30, y_pos + 40), "量子化: Q4_K_M", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    draw.text((30, y_pos + 60), "サイズ: 約 2.7GB", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    draw.text((30, y_pos + 80), "状態: ✅ 読み込み済み", fill=TEXT_PRIMARY, anchor="lt", font=get_font(15))
    
    img.save("screenshots/settings_screen.png")
    print("✅ Created settings_screen.png")

def create_loading_screen():
    """Create loading screen"""
    img = Image.new('RGB', (WIDTH, HEIGHT), CARD_WHITE)
    draw = ImageDraw.Draw(img)
    
    # Center content
    center_y = HEIGHT // 2
    
    # App logo/title
    draw.text((WIDTH//2, center_y - 80), "Qwen3-4B Chat", fill=TEXT_PRIMARY, anchor="mm", font=get_font(24, bold=True))
    
    # Loading spinner placeholder
    draw.text((WIDTH//2, center_y), "⏳", fill=ACCENT_COLOR, anchor="mm", font=get_font(40))
    
    # Loading text
    draw.text((WIDTH//2, center_y + 40), "モデルを読み込み中...", fill=TEXT_SECONDARY, anchor="mm", font=get_font(16))
    
    # Progress bar
    bar_width = WIDTH - 80
    bar_x = 40
    bar_y = center_y + 80
    draw.rounded_rectangle([(bar_x, bar_y), (bar_x + bar_width, bar_y + 8)], 
                          radius=4, fill="#E5E5EA")
    draw.rounded_rectangle([(bar_x, bar_y), (bar_x + bar_width * 0.7, bar_y + 8)], 
                          radius=4, fill=ACCENT_COLOR)
    draw.text((WIDTH//2, bar_y + 20), "70%", fill=TEXT_SECONDARY, anchor="mt", font=get_font(14))
    
    img.save("screenshots/loading_screen.png")
    print("✅ Created loading_screen.png")

def create_model_selection_screen():
    """Create model selection screen"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(img)
    
    # Status bar
    draw.rectangle([(0, 0), (WIDTH, SAFE_AREA_TOP)], fill=CARD_WHITE)
    draw.text((WIDTH//2, 15), "9:41", fill=TEXT_PRIMARY, anchor="mt", font=get_font(14))
    
    # Navigation bar
    draw.rectangle([(0, SAFE_AREA_TOP), (WIDTH, SAFE_AREA_TOP + 44)], fill=CARD_WHITE)
    draw.text((WIDTH//2, SAFE_AREA_TOP + 22), "モデル選択", fill=TEXT_PRIMARY, anchor="mm", font=get_font(17, bold=True))
    
    y_pos = SAFE_AREA_TOP + 60
    
    # Description
    draw.text((20, y_pos), "利用可能なモデル", fill=TEXT_SECONDARY, anchor="lt", font=get_font(13))
    y_pos += 30
    
    # Model options
    models = [
        ("Qwen3-4B Q4_K_M", "2.7GB - バランス型（推奨）", True),
        ("Qwen3-4B Q5_K_M", "3.2GB - 高品質", False),
        ("Qwen3-4B Q6_K", "3.8GB - 最高品質", False),
        ("Qwen3-4B Q8_0", "4.5GB - ほぼ無損失", False)
    ]
    
    for model_name, desc, selected in models:
        draw.rounded_rectangle([(20, y_pos), (WIDTH - 20, y_pos + 70)], 
                              radius=12, fill=CARD_WHITE)
        draw.text((30, y_pos + 20), model_name, fill=TEXT_PRIMARY, anchor="lt", font=get_font(16, bold=True))
        draw.text((30, y_pos + 45), desc, fill=TEXT_SECONDARY, anchor="lt", font=get_font(14))
        if selected:
            draw.text((WIDTH - 30, y_pos + 35), "✓", fill=ACCENT_COLOR, anchor="rm", font=get_font(24))
        y_pos += 80
    
    # Download button
    y_pos += 20
    draw.rounded_rectangle([(40, y_pos), (WIDTH - 40, y_pos + 50)], 
                          radius=25, fill=ACCENT_COLOR)
    draw.text((WIDTH//2, y_pos + 25), "ダウンロード開始", fill=CARD_WHITE, anchor="mm", font=get_font(17, bold=True))
    
    img.save("screenshots/model_selection.png")
    print("✅ Created model_selection.png")

# Generate all screenshots
create_chat_screen()
create_settings_screen()
create_loading_screen()
create_model_selection_screen()

print("\n✅ All screenshots generated in screenshots/ directory")