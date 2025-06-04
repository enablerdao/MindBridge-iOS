import Foundation
import SwiftUI

// モデル情報の構造体
struct ModelInfo: Identifiable {
    let id = UUID()
    let name: String
    let fileName: String
    let url: String
    let size: String
    let quantization: String
    var isDownloaded: Bool = false
    var downloadProgress: Double = 0.0
}

@MainActor
@available(iOS 16.0, macOS 13.0, *)
class ModelDownloadService: ObservableObject {
    @Published var availableModels: [ModelInfo] = []
    @Published var isSearching = false
    @Published var downloadingModel: ModelInfo?
    @Published var downloadProgress: Double = 0.0
    
    private let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
    
    init() {
        setupAvailableModels()
    }
    
    private func setupAvailableModels() {
        // Qwen3-4B-Instruct の利用可能なモデル
        availableModels = [
            ModelInfo(
                name: "Qwen3-4B-Instruct Q4_K_M",
                fileName: "qwen3-4b-instruct-q4_k_m.gguf",
                url: "https://huggingface.co/Qwen/Qwen3-4B-Instruct-GGUF/resolve/main/qwen3-4b-instruct-q4_k_m.gguf",
                size: "2.7GB",
                quantization: "Q4_K_M"
            ),
            ModelInfo(
                name: "Qwen3-4B-Instruct Q5_K_M",
                fileName: "qwen3-4b-instruct-q5_k_m.gguf",
                url: "https://huggingface.co/Qwen/Qwen3-4B-Instruct-GGUF/resolve/main/qwen3-4b-instruct-q5_k_m.gguf",
                size: "3.2GB",
                quantization: "Q5_K_M"
            ),
            ModelInfo(
                name: "Qwen3-4B-Instruct Q6_K",
                fileName: "qwen3-4b-instruct-q6_k.gguf",
                url: "https://huggingface.co/Qwen/Qwen3-4B-Instruct-GGUF/resolve/main/qwen3-4b-instruct-q6_k.gguf",
                size: "3.8GB",
                quantization: "Q6_K"
            ),
            ModelInfo(
                name: "Qwen3-4B-Instruct Q8_0",
                fileName: "qwen3-4b-instruct-q8_0.gguf",
                url: "https://huggingface.co/Qwen/Qwen3-4B-Instruct-GGUF/resolve/main/qwen3-4b-instruct-q8_0.gguf",
                size: "4.5GB",
                quantization: "Q8_0"
            )
        ]
        
        // 既にダウンロード済みのモデルをチェック
        checkDownloadedModels()
    }
    
    func searchModels() async {
        isSearching = true
        
        // Hugging Face API を使ったモデル検索（シミュレーション）
        try? await Task.sleep(nanoseconds: 1_000_000_000) // 1秒待機
        
        // 実際のAPIでは:
        // let url = URL(string: "https://huggingface.co/api/models?search=qwen3+gguf")!
        // URLSession で検索
        
        isSearching = false
    }
    
    func downloadModel(_ model: ModelInfo) async throws {
        downloadingModel = model
        downloadProgress = 0.0
        
        guard let url = URL(string: model.url) else {
            throw URLError(.badURL)
        }
        
        let destinationURL = documentsPath.appendingPathComponent(model.fileName)
        
        // URLSession でダウンロード
        let (tempURL, response) = try await URLSession.shared.download(from: url) { progress in
            Task { @MainActor in
                self.downloadProgress = progress
            }
        }
        
        // ファイルを移動
        try FileManager.default.moveItem(at: tempURL, to: destinationURL)
        
        // モデルの状態を更新
        if let index = availableModels.firstIndex(where: { $0.id == model.id }) {
            availableModels[index].isDownloaded = true
        }
        
        downloadingModel = nil
        downloadProgress = 0.0
    }
    
    func deleteModel(_ model: ModelInfo) throws {
        let fileURL = documentsPath.appendingPathComponent(model.fileName)
        try FileManager.default.removeItem(at: fileURL)
        
        if let index = availableModels.firstIndex(where: { $0.id == model.id }) {
            availableModels[index].isDownloaded = false
        }
    }
    
    func getModelPath(for model: ModelInfo) -> URL? {
        let fileURL = documentsPath.appendingPathComponent(model.fileName)
        return FileManager.default.fileExists(atPath: fileURL.path) ? fileURL : nil
    }
    
    private func checkDownloadedModels() {
        for (index, model) in availableModels.enumerated() {
            let fileURL = documentsPath.appendingPathComponent(model.fileName)
            availableModels[index].isDownloaded = FileManager.default.fileExists(atPath: fileURL.path)
        }
    }
}

// カスタムURLSessionダウンロードデリゲート
@available(iOS 16.0, macOS 13.0, *)
extension URLSession {
    func download(from url: URL, progress: @escaping (Double) -> Void) async throws -> (URL, URLResponse) {
        let (asyncBytes, response) = try await URLSession.shared.bytes(from: url)
        
        let totalBytes = response.expectedContentLength
        var downloadedBytes: Int64 = 0
        
        let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        let fileHandle = try FileHandle(forWritingTo: tempURL)
        
        for try await byte in asyncBytes {
            try fileHandle.write(contentsOf: Data([byte]))
            downloadedBytes += 1
            
            if totalBytes > 0 {
                let currentProgress = Double(downloadedBytes) / Double(totalBytes)
                await MainActor.run {
                    progress(currentProgress)
                }
            }
        }
        
        try fileHandle.close()
        return (tempURL, response)
    }
}