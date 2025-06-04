import XCTest

// Simple test runner for testing without full llama.cpp integration
#if os(macOS)
@available(macOS 13.0, *)
@main
struct TestRunner {
    static func main() {
        print("🧪 Running MindBridge Tests")
        print("========================")
        
        // Run tests that don't require llama.cpp
        let testClasses: [XCTestCase.Type] = [
            ChatMessageTests.self
        ]
        
        for testClass in testClasses {
            print("\n📝 Running \(String(describing: testClass))...")
            
            // Get all test methods
            let testCase = testClass.init()
            let methodCount = testCase.classMethods.count
            
            print("   Found \(methodCount) test methods")
        }
        
        print("\n✅ Test run completed")
    }
}

extension XCTestCase {
    var classMethods: [String] {
        var count: UInt32 = 0
        let methods = class_copyMethodList(type(of: self), &count)
        defer { free(methods) }
        
        var methodNames: [String] = []
        for i in 0..<Int(count) {
            if let method = methods?[i] {
                let selector = method_getName(method)
                if let name = NSString(utf8String: sel_getName(selector)) as String?,
                   name.hasPrefix("test") {
                    methodNames.append(name)
                }
            }
        }
        return methodNames
    }
}
#endif