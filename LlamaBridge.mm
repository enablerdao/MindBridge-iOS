#import "Qwen3iOS-Bridging-Header.h"
#include "llama.h"
#include <string>
#include <vector>

struct llama_context_wrapper {
    llama_model* model = nullptr;
    llama_context* ctx = nullptr;
    llama_batch batch;
    std::vector<llama_token> tokens;
};

extern "C" {

llama_context llama_init_model(const char* model_path) {
    llama_backend_init();
    
    auto wrapper = new llama_context_wrapper();
    
    // モデルパラメータの設定
    llama_model_params model_params = llama_model_default_params();
    model_params.n_gpu_layers = 99; // Metal で全レイヤーを GPU 実行
    
    // モデルの読み込み
    wrapper->model = llama_load_model_from_file(model_path, model_params);
    if (!wrapper->model) {
        delete wrapper;
        return nullptr;
    }
    
    // コンテキストパラメータの設定
    llama_context_params ctx_params = llama_context_default_params();
    ctx_params.n_ctx = 4096;
    ctx_params.n_batch = 512;
    ctx_params.n_threads = 4;
    
    // コンテキストの作成
    wrapper->ctx = llama_new_context_with_model(wrapper->model, ctx_params);
    if (!wrapper->ctx) {
        llama_free_model(wrapper->model);
        delete wrapper;
        return nullptr;
    }
    
    // バッチの初期化
    wrapper->batch = llama_batch_init(512, 0, 1);
    
    return (llama_context)wrapper;
}

const char* llama_generate(llama_context ctx, const char* prompt, float temperature, int max_tokens, float top_p) {
    auto wrapper = (llama_context_wrapper*)ctx;
    if (!wrapper || !wrapper->ctx) {
        return strdup("Error: Invalid context");
    }
    
    // プロンプトのトークン化
    std::string prompt_str(prompt);
    wrapper->tokens.clear();
    wrapper->tokens.resize(prompt_str.length() + 1);
    int n_tokens = llama_tokenize(wrapper->model, prompt_str.c_str(), prompt_str.length(), 
                                   wrapper->tokens.data(), wrapper->tokens.size(), true, false);
    wrapper->tokens.resize(n_tokens);
    
    // バッチのクリアと準備
    llama_batch_clear(wrapper->batch);
    for (int i = 0; i < n_tokens; i++) {
        llama_batch_add(wrapper->batch, wrapper->tokens[i], i, {0}, false);
    }
    wrapper->batch.logits[wrapper->batch.n_tokens - 1] = true;
    
    // 評価
    if (llama_decode(wrapper->ctx, wrapper->batch) != 0) {
        return strdup("Error: Failed to evaluate prompt");
    }
    
    // 生成
    std::string generated_text;
    int n_cur = wrapper->batch.n_tokens;
    int n_decode = 0;
    
    llama_token new_token_id = 0;
    while (n_decode < max_tokens) {
        // サンプリング
        auto logits = llama_get_logits_ith(wrapper->ctx, wrapper->batch.n_tokens - 1);
        auto n_vocab = llama_n_vocab(wrapper->model);
        
        std::vector<llama_token_data> candidates;
        candidates.reserve(n_vocab);
        for (llama_token token_id = 0; token_id < n_vocab; token_id++) {
            candidates.emplace_back(llama_token_data{token_id, logits[token_id], 0.0f});
        }
        
        llama_token_data_array candidates_p = { candidates.data(), candidates.size(), false };
        
        // サンプリング戦略
        llama_sample_top_k(wrapper->ctx, &candidates_p, 40, 1);
        llama_sample_top_p(wrapper->ctx, &candidates_p, top_p, 1);
        llama_sample_temp(wrapper->ctx, &candidates_p, temperature);
        new_token_id = llama_sample_token(wrapper->ctx, &candidates_p);
        
        // EOS チェック
        if (llama_token_is_eog(wrapper->model, new_token_id)) {
            break;
        }
        
        // トークンをテキストに変換
        char buf[256];
        int n = llama_token_to_piece(wrapper->model, new_token_id, buf, sizeof(buf), 0, false);
        if (n > 0) {
            generated_text.append(buf, n);
        }
        
        // 次のトークンの準備
        llama_batch_clear(wrapper->batch);
        llama_batch_add(wrapper->batch, new_token_id, n_cur, {0}, true);
        n_cur++;
        
        if (llama_decode(wrapper->ctx, wrapper->batch) != 0) {
            break;
        }
        
        n_decode++;
    }
    
    return strdup(generated_text.c_str());
}

void llama_free_context(llama_context ctx) {
    auto wrapper = (llama_context_wrapper*)ctx;
    if (wrapper) {
        if (wrapper->ctx) {
            llama_free(wrapper->ctx);
        }
        if (wrapper->model) {
            llama_free_model(wrapper->model);
        }
        llama_batch_free(wrapper->batch);
        delete wrapper;
    }
    llama_backend_free();
}

int llama_get_vocab_size(llama_context ctx) {
    auto wrapper = (llama_context_wrapper*)ctx;
    if (wrapper && wrapper->model) {
        return llama_n_vocab(wrapper->model);
    }
    return 0;
}

int llama_get_context_size(llama_context ctx) {
    auto wrapper = (llama_context_wrapper*)ctx;
    if (wrapper && wrapper->ctx) {
        return llama_n_ctx(wrapper->ctx);
    }
    return 0;
}

} // extern "C"