import SwiftUI

@available(iOS 16.0, macOS 13.0, *)
struct ModelSelectionView: View {
    @StateObject private var downloadService = ModelDownloadService()
    @Environment(\.dismiss) private var dismiss
    @Binding var selectedModel: ModelInfo?
    
    var body: some View {
        NavigationView {
            VStack {
                if downloadService.isSearching {
                    ProgressView("モデルを検索中...")
                        .padding()
                } else {
                    List {
                        Section("利用可能なモデル") {
                            ForEach(downloadService.availableModels) { model in
                                ModelRowView(
                                    model: model,
                                    isSelected: selectedModel?.id == model.id,
                                    downloadService: downloadService,
                                    onSelect: {
                                        selectedModel = model
                                        dismiss()
                                    }
                                )
                            }
                        }
                        
                        Section("モデルについて") {
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Qwen3-4B-Instructは、Alibaba Cloudが開発した高性能な言語モデルです。")
                                    .font(.caption)
                                Text("• Q4_K_M: バランス型（推奨）")
                                    .font(.caption)
                                Text("• Q5_K_M: 高品質")
                                    .font(.caption)
                                Text("• Q6_K: 最高品質")
                                    .font(.caption)
                                Text("• Q8_0: ほぼ無損失")
                                    .font(.caption)
                            }
                            .foregroundColor(.secondary)
                        }
                    }
                }
            }
            .navigationTitle("モデル選択")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("キャンセル") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .automatic) {
                    Button(action: {
                        Task {
                            await downloadService.searchModels()
                        }
                    }) {
                        Image(systemName: "arrow.clockwise")
                    }
                }
            }
        }
    }
}

@available(iOS 16.0, macOS 13.0, *)
struct ModelRowView: View {
    let model: ModelInfo
    let isSelected: Bool
    @ObservedObject var downloadService: ModelDownloadService
    let onSelect: () -> Void
    
    @State private var isDownloading = false
    @State private var showError = false
    @State private var errorMessage = ""
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text(model.name)
                        .font(.headline)
                    HStack {
                        Label(model.size, systemImage: "doc.fill")
                        Label(model.quantization, systemImage: "cpu")
                    }
                    .font(.caption)
                    .foregroundColor(.secondary)
                }
                
                Spacer()
                
                if model.isDownloaded {
                    if isSelected {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundColor(.green)
                    } else {
                        Button("選択") {
                            onSelect()
                        }
                        .buttonStyle(.borderedProminent)
                    }
                } else {
                    Button(action: downloadModel) {
                        if isDownloading {
                            ProgressView()
                                .progressViewStyle(CircularProgressViewStyle())
                                .scaleEffect(0.8)
                        } else {
                            Label("ダウンロード", systemImage: "arrow.down.circle")
                        }
                    }
                    .buttonStyle(.bordered)
                    .disabled(isDownloading)
                }
            }
            
            if isDownloading, let progress = downloadService.downloadingModel?.id == model.id ? downloadService.downloadProgress : nil {
                ProgressView(value: progress)
                    .progressViewStyle(LinearProgressViewStyle())
                Text("\(Int(progress * 100))% ダウンロード中...")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
        .alert("エラー", isPresented: $showError) {
            Button("OK") { }
        } message: {
            Text(errorMessage)
        }
    }
    
    private func downloadModel() {
        isDownloading = true
        
        Task {
            do {
                try await downloadService.downloadModel(model)
                isDownloading = false
            } catch {
                errorMessage = "ダウンロードに失敗しました: \(error.localizedDescription)"
                showError = true
                isDownloading = false
            }
        }
    }
}

@available(iOS 16.0, macOS 13.0, *)
struct ModelSelectionView_Previews: PreviewProvider {
    static var previews: some View {
        ModelSelectionView(selectedModel: .constant(nil))
    }
}