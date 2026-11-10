"""B3 generation and capture (design sections 5, 7.5, 7.6, 7.12, 10, 12.5).

Modules:
    prompts    frozen prompt loading with hash verification, chat-template rendering
    requests   seeded GenerationRequest construction (frozen and fresh sets)
    backends   VLLMBackend (pod), TransformersBackend (CPU smoke), MockBackend (integration test)
    tokens     elicitation turns from chat templates, answer-token variants, code-span mapping
    capture    TransformersCapture (single teacher-forced pass), MockCapture
    storage    parquet and safetensors shards, resumable writes, manifest entries
    stage      run_generate and run_capture stage entry points
"""
