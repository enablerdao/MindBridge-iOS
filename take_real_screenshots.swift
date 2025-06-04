#!/usr/bin/env swift

import Foundation
import Cocoa
import AppKit

// Create a simple screenshot taking script
print("📸 実際のスクリーンショット作成ツール")
print("================================")

// Take a screenshot of the current screen
func takeScreenshot(filename: String) -> Bool {
    let task = Process()
    task.launchPath = "/usr/sbin/screencapture"
    task.arguments = ["-x", "-t", "png", "screenshots/real_\(filename).png"]
    
    print("スクリーンショットを撮影中: \(filename)")
    task.launch()
    task.waitUntilExit()
    
    return task.terminationStatus == 0
}

// Instructions for manual screenshot taking
print("\n📱 実際のスクリーンショット撮影手順:")
print("======================================")
print("1. Xcodeでプロジェクトを開く")
print("2. iOSシミュレーターで実行")
print("3. アプリの各画面を表示")
print("4. Cmd+S でスクリーンショット保存")
print("")
print("推奨撮影画面:")
print("- チャット画面（会話中）")
print("- 設定画面")
print("- モデル選択画面") 
print("- 読み込み画面")
print("- プログラミング支援画面")
print("- 数学解答画面")
print("")

// Create directories
let screenshotsDir = "screenshots/real_screenshots"
do {
    try FileManager.default.createDirectory(atPath: screenshotsDir, withIntermediateDirectories: true)
    print("✅ 実際のスクリーンショット用ディレクトリを作成しました")
} catch {
    print("❌ ディレクトリ作成に失敗: \(error)")
}

// Create a script to open the project
let openXcodeScript = """
#!/bin/bash
echo "🚀 Xcodeプロジェクトを開いています..."
open MindBridge.xcodeproj
echo "📱 シミュレーターでアプリを実行してください"
echo "🎬 準備ができたら、画面のスクリーンショットを撮影してください"
"""

do {
    try openXcodeScript.write(toFile: "open_for_screenshots.sh", atomically: true, encoding: .utf8)
    print("✅ Xcode起動スクリプトを作成しました")
} catch {
    print("❌ スクリプト作成に失敗: \(error)")
}

print("\n🎯 次のステップ:")
print("1. ./open_for_screenshots.sh を実行")
print("2. Xcodeでアプリをビルド・実行")
print("3. シミュレーターで各画面のスクリーンショットを撮影")
print("4. screenshots/real_screenshots/ に保存")

print("\n✨ 完了したらREADMEを更新します")