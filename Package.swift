// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "MindBridge",
    platforms: [
        .iOS(.v16),
        .macOS(.v13)
    ],
    products: [
        .library(
            name: "MindBridge",
            targets: ["MindBridge"]),
    ],
    dependencies: [],
    targets: [
        .target(
            name: "MindBridge",
            dependencies: ["LlamaCpp"],
            path: "Sources/MindBridge",
            resources: [.process("Resources")]),
        .target(
            name: "LlamaCpp",
            path: "Sources/LlamaCpp",
            sources: [
                "llama.cpp",
                "ggml.c",
                "ggml-alloc.c",
                "ggml-backend.c",
                "ggml-quants.c",
                "ggml-metal.m"
            ],
            publicHeadersPath: "include",
            cSettings: [
                .define("GGML_USE_METAL"),
                .define("GGML_USE_ACCELERATE"),
                .define("ACCELERATE_NEW_LAPACK"),
                .define("ACCELERATE_LAPACK_ILP64")
            ],
            linkerSettings: [
                .linkedFramework("Accelerate"),
                .linkedFramework("Metal"),
                .linkedFramework("MetalKit"),
                .linkedFramework("MetalPerformanceShaders")
            ]
        ),
        .testTarget(
            name: "MindBridgeTests",
            dependencies: ["MindBridge"],
            path: "MindBridgeTests"
        )
    ]
)