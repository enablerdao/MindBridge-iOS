#include "include/llama.h"
#include <stdlib.h>
#include <string.h>

// Mock implementation for testing
void llama_backend_init(void) {}
void llama_backend_free(void) {}

struct llama_model_params llama_model_default_params(void) {
    struct llama_model_params params = {0};
    params.n_gpu_layers = 99;
    return params;
}

struct llama_context_params llama_context_default_params(void) {
    struct llama_context_params params = {0};
    params.n_ctx = 4096;
    params.n_batch = 512;
    params.n_threads = 4;
    return params;
}