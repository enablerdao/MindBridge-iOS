import XCTest

// This file aggregates all test suites for easy execution

final class AllTests: XCTestCase {
    
    // List of all test classes for documentation
    static let testSuites: [XCTestCase.Type] = [
        ChatMessageTests.self,
        ChatViewModelTests.self,
        ModelDownloadServiceTests.self
    ]
    
    func testRunAllTestSuites() {
        print("🧪 MindBridge Test Suite")
        print("=====================")
        print("Running all unit tests...")
        
        // This method serves as a documentation of all available test suites
        // Actual test execution is handled by XCTest framework
    }
}

// MARK: - Test Configuration

struct TestConfiguration {
    static let isRunningTests = ProcessInfo.processInfo.environment["XCTestConfigurationFilePath"] != nil
    static let testTimeout: TimeInterval = 10.0
    static let mockNetworkDelay: TimeInterval = 0.1
    
    // Test data paths
    static var testDataDirectory: URL {
        FileManager.default.temporaryDirectory.appendingPathComponent("MindBridgeTests")
    }
    
    static func setupTestEnvironment() {
        // Create test data directory if needed
        try? FileManager.default.createDirectory(
            at: testDataDirectory,
            withIntermediateDirectories: true,
            attributes: nil
        )
    }
    
    static func cleanupTestEnvironment() {
        // Remove test data directory
        try? FileManager.default.removeItem(at: testDataDirectory)
    }
}

// MARK: - Test Report Generator

class TestReportGenerator {
    
    struct TestResult {
        let suiteName: String
        let testName: String
        let passed: Bool
        let duration: TimeInterval
        let failureMessage: String?
    }
    
    private var results: [TestResult] = []
    
    func addResult(_ result: TestResult) {
        results.append(result)
    }
    
    func generateReport() -> String {
        let totalTests = results.count
        let passedTests = results.filter { $0.passed }.count
        let failedTests = totalTests - passedTests
        let totalDuration = results.reduce(0) { $0 + $1.duration }
        
        var report = """
        =====================================
        📊 MindBridge Test Results
        =====================================
        
        Total Tests: \(totalTests)
        ✅ Passed: \(passedTests)
        ❌ Failed: \(failedTests)
        ⏱️  Total Duration: \(String(format: "%.2f", totalDuration))s
        
        """
        
        if failedTests > 0 {
            report += "\n❌ Failed Tests:\n"
            report += "-------------------\n"
            for result in results.filter({ !$0.passed }) {
                report += "• \(result.suiteName).\(result.testName)\n"
                if let message = result.failureMessage {
                    report += "  Reason: \(message)\n"
                }
            }
        }
        
        report += "\n📈 Test Coverage:\n"
        report += "-------------------\n"
        report += "• Models: \(calculateCoverage(for: "Model"))%\n"
        report += "• ViewModels: \(calculateCoverage(for: "ViewModel"))%\n"
        report += "• Services: \(calculateCoverage(for: "Service"))%\n"
        
        return report
    }
    
    private func calculateCoverage(for component: String) -> Int {
        // This is a simplified coverage calculation
        // In real implementation, would use code coverage tools
        let relevantTests = results.filter { $0.suiteName.contains(component) }
        guard !relevantTests.isEmpty else { return 0 }
        
        let passedRelevantTests = relevantTests.filter { $0.passed }.count
        return Int((Double(passedRelevantTests) / Double(relevantTests.count)) * 100)
    }
}

// MARK: - Integration Test Base Class

class IntegrationTestCase: XCTestCase {
    
    override func setUp() {
        super.setUp()
        TestConfiguration.setupTestEnvironment()
    }
    
    override func tearDown() {
        TestConfiguration.cleanupTestEnvironment()
        super.tearDown()
    }
    
    /// Helper method for integration tests that require the full app context
    func withAppContext<T>(timeout: TimeInterval = 5.0, operation: @escaping () async throws -> T) async rethrows -> T {
        return try await withTaskCancellationHandler(
            operation: {
                try await operation()
            },
            onCancel: {
                print("⚠️ Integration test cancelled after \(timeout)s")
            }
        )
    }
}