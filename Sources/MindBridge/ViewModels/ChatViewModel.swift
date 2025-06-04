import Foundation
import SwiftUI

@MainActor
@available(iOS 16.0, macOS 13.0, *)
class ChatViewModel: ObservableObject {
    @Published var messages: [ChatMessage] = []
    @Published var showSettings = false
    @Published var isModelLoaded = false
    @Published var modelLoadingProgress: Double = 0
    
    private let llamaService = LlamaService()
    
    init() {
        messages.append(ChatMessage(
            content: "こんにちは！Qwen3-4Bモデルを使用したチャットアプリです。何かお手伝いできることはありますか？",
            isUser: false
        ))
    }
    
    func initializeModel() {
        Task {
            do {
                modelLoadingProgress = 0.1
                try await llamaService.loadModel()
                modelLoadingProgress = 1.0
                isModelLoaded = true
            } catch {
                messages.append(ChatMessage(
                    content: "モデルの読み込みに失敗しました: \(error.localizedDescription)",
                    isUser: false
                ))
            }
        }
    }
    
    func sendMessage(_ text: String) async {
        messages.append(ChatMessage(content: text, isUser: true))
        
        do {
            let response = try await llamaService.generateResponse(prompt: text)
            messages.append(ChatMessage(content: response, isUser: false))
        } catch {
            messages.append(ChatMessage(
                content: "エラーが発生しました: \(error.localizedDescription)",
                isUser: false
            ))
        }
    }
    
    func clearChat() {
        messages = [ChatMessage(
            content: "チャットがクリアされました。新しい会話を始めましょう！",
            isUser: false
        )]
    }
}