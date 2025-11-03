"""
RAG (Retrieval-Augmented Generation) utilities.
"""

import numpy as np

from baml.baml_client.types import Message


def get_dynex(
    messages, text, args, index, embeddings, lookup_dataset, client, embed_model
):
    """Enhanced RAG: Retrieve top-k diverse examples from training data."""
    k = args.dynex_k  # Number of examples to retrieve; configurable via args
    embed = client.embed(
        model=embed_model,
        input=text,
    ).embeddings

    # Retrieve 2x candidates for diversity filtering
    labels, distances = index.knn_query(embed, k=k * 2)

    # Diversity filtering: Select k diverse examples using embedding distance
    selected_examples = []
    selected_embeds = []

    for idx, dist in zip(labels[0], distances[0]):
        example = lookup_dataset[int(idx)]
        example_embed = embeddings[int(idx)]

        # Skip if too similar to already selected (cosine similarity > 0.8, i.e., distance < 0.2)
        if any(np.dot(example_embed, sel_embed) > 0.8 for sel_embed in selected_embeds):
            continue

        selected_examples.append(example)
        selected_embeds.append(example_embed)

        if len(selected_examples) == k:
            break

    examples_text = ""
    for i, example in enumerate(selected_examples, start=1):
        example_doc = example["doc"]
        example_triples = example["triples"]

        example_line = (
            f"EXAMPLE {i}:\nText: {example_doc}\nRelations: {example_triples}"
        )
        example_line += "\n\n"
        examples_text += example_line

    messages.append(Message(role="user", content=f"SIMILAR EXAMPLES:\n{examples_text}"))
