import os
from parser import args

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

if not args.nebius:
    model_dict = {
        "8b": "llama3.1:8b",
        "70b": "llama3.1:70b",
        "405b": "llama3.1:405b-cpu",
    }
    model = model_dict[args.model]
else:
    model_dict = {
        "8b": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "70b": "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "405b": "meta-llama/Meta-Llama-3.1-405B-Instruct",
    }
    model = model_dict[args.model]


ip_dict = {
    "g4": "10.250.135.153",
    "g2": "10.250.135.143",
    "g3": "10.250.135.150",
    "g5": "10.250.135.156",
    "mk22d": "10.250.135.115",
}

if not args.nebius:
    llm = ChatOllama(
        model=model,
        temperature=0,
        keep_alive="240h",
        base_url=f"http://{ip_dict[args.node]}:114{args.port}",
        num_ctx=50_000 if args.doclevel else 4_000,
        num_predict=-1,
        seed=0,
    )
else:
    llm = ChatOpenAI(
        base_url="https://api.studio.nebius.ai/v1/",
        api_key=os.getenv(args.apikey),
        model=model,
        temperature=0,
        max_tokens=512,
        seed=0,
    )

print(f"Using llm {llm}.")
