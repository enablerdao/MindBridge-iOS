import SwiftUI

struct SettingsView: View {
    @ObservedObject var viewModel: ChatViewModel
    @Environment(\.dismiss) private var dismiss
    @AppStorage("temperature") private var temperature: Double = 0.7
    @AppStorage("maxTokens") private var maxTokens: Double = 512
    @AppStorage("topP") private var topP: Double = 0.9
    
    var body: some View {
        NavigationView {
            Form {
                Section("モデル設定") {
                    VStack(alignment: .leading) {
                        Text("Temperature: \(temperature, specifier: "%.2f")")
                        Slider(value: $temperature, in: 0...2, step: 0.1)
                    }
                    
                    VStack(alignment: .leading) {
                        Text("最大トークン数: \(Int(maxTokens))")
                        Slider(value: $maxTokens, in: 128...2048, step: 128)
                    }
                    
                    VStack(alignment: .leading) {
                        Text("Top-p: \(topP, specifier: "%.2f")")
                        Slider(value: $topP, in: 0...1, step: 0.05)
                    }
                }
                
                Section("モデル情報") {
                    HStack {
                        Text("モデル")
                        Spacer()
                        Text("Qwen3-4B-Instruct")
                            .foregroundColor(.gray)
                    }
                    
                    HStack {
                        Text("量子化")
                        Spacer()
                        Text("Q4_K_M")
                            .foregroundColor(.gray)
                    }
                    
                    HStack {
                        Text("ファイルサイズ")
                        Spacer()
                        Text("約 2.7GB")
                            .foregroundColor(.gray)
                    }
                    
                    HStack {
                        Text("状態")
                        Spacer()
                        if viewModel.isModelLoaded {
                            Label("読み込み済み", systemImage: "checkmark.circle.fill")
                                .foregroundColor(.green)
                        } else {
                            Label("未読み込み", systemImage: "xmark.circle.fill")
                                .foregroundColor(.red)
                        }
                    }
                }
                
                Section("チャット") {
                    Button("チャット履歴をクリア") {
                        viewModel.clearChat()
                        dismiss()
                    }
                    .foregroundColor(.red)
                }
                
                Section("アプリ情報") {
                    HStack {
                        Text("バージョン")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.gray)
                    }
                    
                    Link("llama.cpp について", destination: URL(string: "https://github.com/ggerganov/llama.cpp")!)
                }
            }
            .navigationTitle("設定")
            .toolbar {
                ToolbarItem(placement: .automatic) {
                    Button("完了") {
                        dismiss()
                    }
                }
            }
        }
    }
}

struct SettingsView_Previews: PreviewProvider {
    static var previews: some View {
        SettingsView(viewModel: ChatViewModel())
    }
}