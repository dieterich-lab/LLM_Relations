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
    ("llama31", "llama3.1:8b"),
    ("deepseek8b", "deepseek-r1-128k:8b"),
    ("deepseek70b", "deepseek-r1-128k:70b"),
    ("gemma", "gemma3:27b"),
    ("llama33regu", "llama3.3:70b-regu_Q4_K_M"),
    ("llama31regu", "llama3.1:8b-regu_Q4_K_M"),
    ("llama33regutf", "llama3.3-70b-regu_tf"),
    ("llama31regutf", "llama3.1-8b-regu_tf"),
    ("qwen3", "qwen3:8b"),
    ("qwen34", "qwen3:14b"),
    ("qwen330", "qwen3:30b"),
    ("qwen332", "qwen3:32b"),
]

ollama_client_dict = {
    "llama33": "llama3.3:70b",
    "llama31": "llama3.1-128k:8b",
    "deepseek8b": "deepseek-r1-128k:8b",
    "deepseek70b": "deepseek-r1-128k:70b",
    "gemma": "gemma3:27b",
    "llama33regu": "llama3.3:70b-regu_Q4_K_M",
    "llama31regu": "llama3.1-128k-8b-regu",
    "llama33regutf": "llama3.3-70b-regu_tf",
    "llama31regutf": "llama3.1-8b-regu_tf",
    "qwen3": "qwen3:8b",
    "qwen314": "qwen3:14b",
    "qwen330": "qwen3:30b",
    "qwen332": "qwen3:32b",
}


hf_client_names = {
    "llama33": "unsloth/Llama-3.3-70B-Instruct-bnb-4bit",
    "llama31": "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    "deepseek8b": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    "deepseek70b": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
    "gemma": "unsloth/gemma-3-27b-it-unsloth-bnb-4bit",
}


model = ollama_client_dict[args.model]
hf_model_id = hf_client_names.get(args.model)

port_dict = {"g2": 32, "g3": 33, "g4": 34, "g5": 35}
if not args.port:
    port = port_dict[args.node]
else:
    port = args.port

clients = list()
for name, client in ollama_client_names:
    clients.append(
        {
            "name": name,
            "provider": "openai-generic",  # ollama is finally openai capable (https://ollama.com/blog/openai-compatibility)
            "options": {
                "base_url": f"http://{ip_dict[args.node]}:114{port}/v1",
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
