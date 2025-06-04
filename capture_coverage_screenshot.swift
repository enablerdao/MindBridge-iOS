#!/usr/bin/env swift

import Foundation
import AppKit
import WebKit

class ScreenshotCapture: NSObject {
    let webView = WKWebView(frame: NSRect(x: 0, y: 0, width: 1200, height: 800))
    var completion: ((Bool) -> Void)?
    
    func captureScreenshot(url: URL, outputPath: String, completion: @escaping (Bool) -> Void) {
        self.completion = completion
        
        webView.navigationDelegate = self
        webView.load(URLRequest(url: url))
    }
    
    func takeSnapshot(outputPath: String) {
        let config = WKSnapshotConfiguration()
        config.rect = webView.bounds
        
        webView.takeSnapshot(with: config) { image, error in
            guard let image = image else {
                print("❌ スナップショット取得エラー: \(error?.localizedDescription ?? "不明なエラー")")
                self.completion?(false)
                return
            }
            
            if let tiffData = image.tiffRepresentation,
               let bitmap = NSBitmapImageRep(data: tiffData),
               let pngData = bitmap.representation(using: .png, properties: [:]) {
                do {
                    try pngData.write(to: URL(fileURLWithPath: outputPath))
                    print("✅ スクリーンショットを保存: \(outputPath)")
                    self.completion?(true)
                } catch {
                    print("❌ 保存エラー: \(error)")
                    self.completion?(false)
                }
            }
        }
    }
}

extension ScreenshotCapture: WKNavigationDelegate {
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        // ページ読み込み完了後、少し待ってからスクリーンショット
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
            self.takeSnapshot(outputPath: "coverage_visualization.png")
        }
    }
    
    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        print("❌ ページ読み込みエラー: \(error)")
        completion?(false)
    }
}

// メイン処理
let app = NSApplication.shared
app.setActivationPolicy(.accessory)

let capture = ScreenshotCapture()
let url = URL(string: "http://localhost:18457/coverage_report.html")!

print("📸 カバレッジレポートのスクリーンショットを撮影中...")

let semaphore = DispatchSemaphore(value: 0)
var success = false

capture.captureScreenshot(url: url, outputPath: "coverage_visualization.png") { result in
    success = result
    semaphore.signal()
}

// タイムアウト付き待機
let timeout = DispatchTime.now() + .seconds(10)
if semaphore.wait(timeout: timeout) == .timedOut {
    print("❌ タイムアウト")
    exit(1)
}

exit(success ? 0 : 1)