#!/usr/bin/env python3

import subprocess
import time
import os
import sys

def capture_screenshot(url, output_name):
    """指定されたURLのスクリーンショットを撮影"""
    print(f"📸 {url} のスクリーンショットを撮影中...")
    
    # screencaptureコマンドでウィンドウをキャプチャ
    # -o : マウスカーソルを含めない
    # -l : ウィンドウIDを指定してキャプチャ
    # -x : 音を鳴らさない
    
    # Safariでページを開く
    subprocess.run(['open', '-a', 'Safari', url])
    time.sleep(3)  # ページ読み込み待機
    
    # スクリーンショット撮影
    output_path = f"{output_name}.png"
    subprocess.run(['screencapture', '-x', '-o', output_path])
    
    if os.path.exists(output_path):
        print(f"✅ スクリーンショットを保存: {output_path}")
        return True
    else:
        print(f"❌ スクリーンショットの保存に失敗")
        return False

def main():
    # HTTPサーバーが起動しているか確認
    try:
        import urllib.request
        urllib.request.urlopen('http://localhost:18457/', timeout=2)
    except:
        print("⚠️  HTTPサーバーが起動していません")
        print("🔄 HTTPサーバーを起動します...")
        subprocess.Popen(['python3', '-m', 'http.server', '18457'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        time.sleep(2)
    
    # 各レポートのスクリーンショットを撮影
    reports = [
        ('http://localhost:18457/coverage_report.html', 'coverage_visualization'),
        ('http://localhost:18457/test_dashboard.html', 'test_dashboard_screenshot')
    ]
    
    success_count = 0
    for url, output in reports:
        if capture_screenshot(url, output):
            success_count += 1
    
    print(f"\n📊 結果: {success_count}/{len(reports)} のスクリーンショットを撮影しました")
    
    # 撮影したスクリーンショットを一覧表示
    print("\n📷 撮影したスクリーンショット:")
    for _, output in reports:
        if os.path.exists(f"{output}.png"):
            size = os.path.getsize(f"{output}.png") / 1024
            print(f"  - {output}.png ({size:.1f} KB)")

if __name__ == "__main__":
    main()