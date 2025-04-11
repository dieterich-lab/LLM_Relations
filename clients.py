from parser import args

from baml_py import ClientRegistry

ip_dict = {
    "g4": "10.250.135.153",
    "g2": "10.250.135.143",
    "g3": "10.250.135.150",
    "g5": "10.250.135.156",
    "mk22d": "10.250.135.115",
}

ollama_client_names = [
    ("llama33", "llama3.3:70b"),
    ("llama31", "llama3.1-128k:8b"),
    ("deepseek8b", "deepseek-r1-128k:8b"),
    ("deepseek70b", "deepseek-r1-128k:70b"),
    ("gemma", "gemma3:27b"),
    ("gemmaregu", "gemma3:27b-regu-Q4_K_M"),
    ("llama33regu", "llama3.3:70b-regu_Q4_K_M"),
    ("llama31regu", "llama3.1-128k-8b-regu"),
]

ollama_client_dict = {
    "llama33": "llama3.3:70b",
    "llama31": "llama3.1-128k:8b",
    "deepseek8b": "deepseek-r1-128k:8b",
    "deepseek70b": "deepseek-r1-128k:70b",
    "gemma": "gemma3:27b",
    "gemmaregu": "gemma3:27b-regu-Q4_K_M",
    "llama33regu": "llama3.3:70b-regu_Q4_K_M",
    "llama31regu": "llama3.1-128k-8b-regu",
}


hf_client_names = {
    "llama33": "unsloth/Llama-3.3-70B-Instruct",
    "llama31": "unsloth/Meta-Llama-3.1-8B",
    "deepseek8b": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    "deepseek70b": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
    "gemma": "google/gemma-3-27b-it",
}


model = ollama_client_dict[args.model]
hf_model_id = hf_client_names.get(args.model)


clients = list()
for name, client in ollama_client_names:
    clients.append(
        {
            "name": name,
            "provider": "openai-generic",  # ollama is finally openai capable (https://ollama.com/blog/openai-compatibility)
            "options": {
                "base_url": f"http://{ip_dict[args.node]}:114{args.port}/v1",
                "model": client,
                "max_tokens": 10000,
                "temperature": 0.0,
                "n_ctx": 120_000,  # should be overruled by OLLAMA_CONTEXT_LENGTH (https://github.com/ollama/ollama/blob/main/docs/faq.md)
            },
        }
    )

cr = ClientRegistry()
for client in clients:
    cr.add_llm_client(**client)
cr.set_primary(args.model)
