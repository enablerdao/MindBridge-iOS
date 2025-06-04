import XCTest
@testable import MindBridge

@available(iOS 16.0, macOS 13.0, *)
final class ModelDownloadServiceTests: XCTestCase {
    
    var service: ModelDownloadService!
    var mockFileManager: MockFileManager!
    
    @MainActor
    override func setUp() {
        super.setUp()
        service = ModelDownloadService()
        mockFileManager = MockFileManager()
    }
    
    @MainActor
    override func tearDown() {
        service = nil
        mockFileManager = nil
        super.tearDown()
    }
    
    // MARK: - Initialization Tests
    
    @MainActor
    func testServiceInitialization() {
        // Then
        XCTAssertFalse(service.isSearching)
        XCTAssertNil(service.downloadingModel)
        XCTAssertEqual(service.downloadProgress, 0.0)
        XCTAssertGreaterThan(service.availableModels.count, 0)
    }
    
    @MainActor
    func testAvailableModelsSetup() {
        // Then
        XCTAssertEqual(service.availableModels.count, 4)
        
        // Check first model (Q4_K_M)
        let firstModel = service.availableModels[0]
        XCTAssertEqual(firstModel.name, "Qwen3-4B-Instruct Q4_K_M")
        XCTAssertEqual(firstModel.fileName, "qwen3-4b-instruct-q4_k_m.gguf")
        XCTAssertEqual(firstModel.size, "2.7GB")
        XCTAssertEqual(firstModel.quantization, "Q4_K_M")
        XCTAssertTrue(firstModel.url.contains("huggingface.co"))
    }
    
    // MARK: - Model Info Tests
    
    @MainActor
    func testModelInfoProperties() {
        // Given
        let modelInfo = ModelInfo(
            name: "Test Model",
            fileName: "test.gguf",
            url: "https://example.com/test.gguf",
            size: "1.0GB",
            quantization: "Q4_K_M"
        )
        
        // Then
        XCTAssertNotNil(modelInfo.id)
        XCTAssertEqual(modelInfo.name, "Test Model")
        XCTAssertEqual(modelInfo.fileName, "test.gguf")
        XCTAssertEqual(modelInfo.url, "https://example.com/test.gguf")
        XCTAssertEqual(modelInfo.size, "1.0GB")
        XCTAssertEqual(modelInfo.quantization, "Q4_K_M")
        XCTAssertFalse(modelInfo.isDownloaded)
        XCTAssertEqual(modelInfo.downloadProgress, 0.0)
    }
    
    // MARK: - Search Tests
    
    @MainActor
    func testSearchModels() async {
        // Given
        XCTAssertFalse(service.isSearching)
        
        // When
        let searchTask = Task {
            await service.searchModels()
        }
        
        // Give it a moment to start
        try? await Task.sleep(nanoseconds: 100_000_000) // 0.1秒
        
        // Then - should be searching
        XCTAssertTrue(service.isSearching)
        
        // Wait for completion
        await searchTask.value
        
        // Then - should finish searching
        XCTAssertFalse(service.isSearching)
    }
    
    // MARK: - Model Path Tests
    
    @MainActor
    func testGetModelPath() {
        // Given
        let model = service.availableModels[0]
        
        // When
        let path = service.getModelPath(for: model)
        
        // Then
        // Path should be nil if file doesn't exist
        if let path = path {
            XCTAssertTrue(path.absoluteString.contains(model.fileName))
        }
    }
    
    // MARK: - Download Progress Tests
    
    @MainActor
    func testDownloadProgressTracking() async throws {
        // Given
        let _ = service.availableModels[0]
        XCTAssertEqual(service.downloadProgress, 0.0)
        XCTAssertNil(service.downloadingModel)
        
        // When starting download
        // Note: In real tests, we'd mock URLSession to avoid actual network calls
        // This is just testing the structure
        
        // Then
        // Would verify:
        // - downloadingModel is set
        // - downloadProgress updates
        // - model.isDownloaded becomes true after completion
    }
    
    // MARK: - Delete Model Tests
    
    @MainActor
    func testDeleteModel() throws {
        // Given
        var model = service.availableModels[0]
        model.isDownloaded = true
        
        // When & Then
        // In real implementation, would test:
        // - File is removed from disk
        // - model.isDownloaded becomes false
        // - No errors thrown for valid deletion
    }
}

// MARK: - Mock Classes

class MockFileManager {
    var filesExist: [String: Bool] = [:]
    var shouldThrowError = false
    
    func fileExists(atPath path: String) -> Bool {
        return filesExist[path] ?? false
    }
    
    func removeItem(at URL: URL) throws {
        if shouldThrowError {
            throw NSError(domain: "MockError", code: 1, userInfo: nil)
        }
        filesExist[URL.path] = false
    }
    
    func moveItem(at srcURL: URL, to dstURL: URL) throws {
        if shouldThrowError {
            throw NSError(domain: "MockError", code: 2, userInfo: nil)
        }
        filesExist[dstURL.path] = true
    }
}

class MockURLSession {
    var mockData: Data?
    var mockResponse: URLResponse?
    var mockError: Error?
    var progressUpdates: [Double] = [0.25, 0.5, 0.75, 1.0]
    
    func download(from url: URL, progress: @escaping (Double) -> Void) async throws -> (URL, URLResponse) {
        if let error = mockError {
            throw error
        }
        
        // Simulate progress updates
        for progressValue in progressUpdates {
            progress(progressValue)
            try await Task.sleep(nanoseconds: 100_000_000) // 0.1秒
        }
        
        let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent("mock.tmp")
        if let data = mockData {
            try data.write(to: tempURL)
        }
        
        let response = mockResponse ?? URLResponse(
            url: url,
            mimeType: "application/octet-stream",
            expectedContentLength: Int(mockData?.count ?? 0),
            textEncodingName: nil
        )
        
        return (tempURL, response)
    }
}