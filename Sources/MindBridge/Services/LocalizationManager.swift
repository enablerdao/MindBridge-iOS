import Foundation
import SwiftUI

/// Manages localization for the MindBridge app
final class LocalizationManager: ObservableObject {
    static let shared = LocalizationManager()
    
    @Published var currentLanguage: String = Locale.current.language.languageCode?.identifier ?? "en"
    
    private init() {
        setupInitialLanguage()
    }
    
    private func setupInitialLanguage() {
        // Check for saved language preference
        if let savedLanguage = UserDefaults.standard.string(forKey: "selected_language") {
            currentLanguage = savedLanguage
        } else {
            // Use system language if supported, otherwise default to English
            let systemLanguage = Locale.current.language.languageCode?.identifier ?? "en"
            currentLanguage = supportedLanguages.contains(systemLanguage) ? systemLanguage : "en"
        }
    }
    
    /// List of supported languages
    var supportedLanguages: [String] {
        ["en", "ja", "zh-Hans", "ko"]
    }
    
    /// Language display names
    var languageDisplayNames: [String: String] {
        [
            "en": "English",
            "ja": "日本語",
            "zh-Hans": "简体中文",
            "ko": "한국어"
        ]
    }
    
    /// Set the current language
    func setLanguage(_ languageCode: String) {
        guard supportedLanguages.contains(languageCode) else { return }
        
        currentLanguage = languageCode
        UserDefaults.standard.set(languageCode, forKey: "selected_language")
        objectWillChange.send()
    }
    
    /// Get localized string for the current language
    func localizedString(for key: String, comment: String = "") -> String {
        guard let path = Bundle.main.path(forResource: currentLanguage, ofType: "lproj"),
              let bundle = Bundle(path: path) else {
            // Fallback to main bundle (usually English)
            return NSLocalizedString(key, comment: comment)
        }
        
        return NSLocalizedString(key, bundle: bundle, comment: comment)
    }
}

/// SwiftUI extension for easy localization
extension String {
    /// Returns localized string using LocalizationManager
    var localized: String {
        LocalizationManager.shared.localizedString(for: self)
    }
    
    /// Returns localized string with arguments
    func localized(with arguments: CVarArg...) -> String {
        let localizedString = LocalizationManager.shared.localizedString(for: self)
        return String(format: localizedString, arguments: arguments)
    }
}

/// View modifier for dynamic localization
struct LocalizedView: ViewModifier {
    @ObservedObject private var localizationManager = LocalizationManager.shared
    
    func body(content: Content) -> some View {
        content
            .environment(\.locale, Locale(identifier: localizationManager.currentLanguage))
            .onReceive(localizationManager.$currentLanguage) { _ in
                // Trigger view update when language changes
            }
    }
}

extension View {
    /// Apply localization support to any view
    func localized() -> some View {
        modifier(LocalizedView())
    }
}