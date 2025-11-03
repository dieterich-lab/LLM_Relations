from parser import args

import hnswlib
import numpy as np
from ollama import Client
from tqdm import tqdm

from dataset import get_dataset

ip_dict = {
    "g4": "10.250.135.153",
    "g2": "10.250.135.143",
    "g3": "10.250.135.150",
    "g5": "10.250.135.156",
    "mk22d": "10.250.135.115",
}

dim = 1024  # ?
# dim = 384
index_path = f"/prj/LINDA_LLM/outputs/vectorstore/regulatome_{args.target}_idx.bin"
embeddings_path = index_path.replace("_idx.bin", "_embeds.npy")

embed_model = "mxbai-embed-large"
port_dict = {"g2": 32, "g3": 33, "g4": 34, "g5": 35}
port = port_dict[args.node]

client = Client(
    host=f"http://{ip_dict[args.node]}:114{port}",
)


def save_index():
    train_dataset, dev_dataset, _ = get_dataset(args.target, args.data)

    embeds = list()
    for sample in tqdm(train_dataset):
        embed = client.embed(
            model=embed_model,
            input=sample["doc"],
        ).embeddings
        embeds.append(embed[0])

    for sample in tqdm(dev_dataset):
        embed = client.embed(
            model=embed_model,
            input=sample["doc"],
        ).embeddings
        embeds.append(embed[0])

    embeds = np.array(embeds)

    # Improved index parameters for better quality and efficiency
    p = hnswlib.Index(space="cosine", dim=dim)  # Use cosine for normalized embeddings
    p.init_index(
        max_elements=len(embeds), ef_construction=200, M=32
    )  # M=32 is more typical
    p.set_ef(50)  # Higher ef for better search quality
    p.set_num_threads(4)
    p.add_items(embeds)

    print("Saving index to '%s'" % index_path)
    p.save_index(index_path)

    print("Saving embeddings to '%s'" % embeddings_path)
    np.save(embeddings_path, embeds)


def load_index():
    p = hnswlib.Index(space="cosine", dim=dim)  # Match save_index space
    p.load_index(index_path)
    return p


if __name__ == "__main__":
    save_index()
