"""
Extraction utilities for combining and processing extraction results.
"""

import math
from parser import args

from baml.baml_client.sync_client import b
from baml.baml_client.types import Entities, Message, Triples
from brat_utils import parse_brat_annotations
from clients import cr
from documents import all_nes_paths, spacy_ne_paths, true_ne_paths
from prompts import rel_system_prompt


def combine_by_voting(all_path_results, threshold=None):
    """Combine ToT paths by majority voting

    Args:
        all_path_results: List of triple lists from each path
        threshold: Minimum number of paths that must agree (default: ceil(n/2) for majority)
    """
    triple_counts = {}

    for path_triples in all_path_results:
        for triple in path_triples:
            key = (
                f"{triple.head.lower()}|{triple.relation.lower()}|{triple.tail.lower()}"
            )
            if key not in triple_counts:
                triple_counts[key] = {"count": 0, "example": triple}
            triple_counts[key]["count"] += 1

    if threshold is None:
        n_paths = len(all_path_results)
        threshold = math.ceil(n_paths / 2)

    # Keep triples appearing in at least 'threshold' paths
    consensus_triples = [
        data["example"]
        for key, data in triple_counts.items()
        if data["count"] >= threshold
    ]

    return consensus_triples


def combine_by_best_path(all_path_results, all_path_evaluations):
    """Select results from the highest-scored path"""
    if not all_path_evaluations or not any(all_path_evaluations):
        return all_path_results[0] if all_path_results else []

    # Calculate average score for each path
    path_scores = []
    for path_eval in all_path_evaluations:
        if path_eval:
            avg_score = sum(item["score"] for item in path_eval) / len(path_eval)
            path_scores.append(avg_score)
        else:
            path_scores.append(0)

    # Return triples from best path
    best_path_idx = path_scores.index(max(path_scores)) if path_scores else 0
    return all_path_results[best_path_idx]


def combine_by_merging(all_path_results, all_path_evaluations):
    """Merge high-confidence triples from all paths"""
    merged_triples = {}

    for path_idx, path_eval in enumerate(all_path_evaluations):
        for item in path_eval:
            triple = item["triple"]
            score = item["score"]
            key = (
                f"{triple.head.lower()}|{triple.relation.lower()}|{triple.tail.lower()}"
            )

            # Include if: score >= 8, OR appears in multiple paths, OR score >= 6 and in 2+ paths
            if key not in merged_triples:
                merged_triples[key] = {"triple": triple, "max_score": score, "count": 1}
            else:
                merged_triples[key]["max_score"] = max(
                    merged_triples[key]["max_score"], score
                )
                merged_triples[key]["count"] += 1

    # Filter based on confidence criteria
    final_triples = [
        data["triple"]
        for key, data in merged_triples.items()
        if data["max_score"] >= 8
        or data["count"] >= 2
        or (data["max_score"] >= 6 and data["count"] >= 2)
    ]

    return final_triples


def get_nes(messages, responses, doc, prompts, collector, tb):
    """Handle entity extraction for different modes (all_nes_given, true_nes_given, spacy_nes_given)"""
    try:
        if args.all_nes_given or args.true_nes_given:
            ne_paths = true_ne_paths if args.true_nes_given else all_nes_paths
            ne_path = [
                x for x in ne_paths if doc[0].metadata["file_path"].stem == x.stem
            ][0]
            if ne_path:
                nes = open(ne_path, "r").readlines()
                nes = [x.strip() for x in nes]
            else:
                nes = []
            response = Entities(entities=nes)
            responses.append(response)
            messages.append(Message(role="assistant", content=f"{str(response)}"))
        elif args.spacy_nes_given:
            # Find the corresponding BRAT annotation file
            ann_file = None
            if spacy_ne_paths:
                matching_files = [
                    x
                    for x in spacy_ne_paths
                    if doc[0].metadata["file_path"].stem == x.stem
                ]
                if matching_files:
                    ann_file = matching_files[0]

            if ann_file and ann_file.exists():
                # Parse BRAT annotations
                text = doc[0].page_content
                entities = parse_brat_annotations(ann_file, text)

                # Extract just the entity names for the Entities response
                entity_names = [entity["text"] for entity in entities]
                response = Entities(entities=entity_names)
                # Add minimal context information with spans to help the model understand the ground truth entities
                if entities:
                    context_message = "NE LIST:\n"
                    for entity in entities:
                        context_message += f"- {entity['text']} (type: {entity['type']}, span: {entity['start']}-{entity['end']})\n"

                    # Insert this context message before the NER prompt
                    messages.append(Message(role="user", content=context_message))
            else:
                print(
                    f"No BRAT annotation file found for {doc[0].metadata['file_path'].stem}"
                )
                response = Entities(entities=[])
    except Exception as e:
        print(f"Exception at Entity extraction: {e}")
        response = Entities(entities=[])
    responses.append(response)
    return prompts


def extract_nes(messages, responses, collector, tb):
    """Extract named entities using BAML"""
    try:
        response = b.ExtractNEs(
            messages,
            baml_options={"client_registry": cr, "tb": tb, "collector": collector},
        )
    except Exception as e:
        print(f"Exception at Entity extraction: {e}")
        response = Entities(entities=[])
    responses.append(response)
    messages.append(Message(role="assistant", content=f"{str(response)}"))


def extract_rels(
    messages, responses, prompts, examples_content="", collector=None, tb=None
):
    """Standard single-pass extraction"""
    if examples_content:
        messages[-1].content += f"\n{examples_content}"
    response = b.GeneralChatExtractRelationships(
        messages,
        baml_options={"client_registry": cr, "tb": tb, "collector": collector},
    )
    responses.append(response)
    messages.append(Message(role="assistant", content=str(response)))
    for i, prompt in enumerate(prompts):
        message = Message(role="user", content=prompt)
        messages.append(message)
        try:
            response = b.GeneralChatExtractRelationships(
                messages,
                baml_options={"client_registry": cr, "tb": tb, "collector": collector},
            )
        except Exception as e:
            print(f"Exception at step {i}: {e}")
            response = Triples(triples=[])
        responses.append(response)
        messages.append(Message(role="assistant", content=str(response)))


def extract_rels_ensemble(
    messages,
    responses,
    text,
    prompts,
    n_samples=5,
    temperature=0.7,
    examples_content="",
    collector=None,
    tb=None,
):
    """Self-consistency ensemble extraction with voting"""
    print(f"  Running ensemble extraction with n={n_samples}, temp={temperature}")

    # Collect all triples from all model versions
    all_model_version_triples = []

    for sample_idx in range(n_samples):
        print(f"    Model version {sample_idx + 1}/{n_samples}")
        model_messages = messages.copy()
        model_responses = []

        # First extraction step for this model version
        if examples_content:
            model_messages[-1].content += f"\n{examples_content}"
        response = b.GeneralChatExtractRelationships(
            model_messages,
            baml_options={
                "client_registry": cr,
                "tb": tb,
                "collector": collector,
                "temperature": temperature,
            },
        )
        model_responses.append(response)
        model_messages.append(Message(role="assistant", content=str(response)))

        # Additional extractions for each prompt
        for i, prompt in enumerate(prompts):
            message = Message(role="user", content=prompt)
            model_messages.append(message)
            try:
                response = b.GeneralChatExtractRelationships(
                    model_messages,
                    baml_options={
                        "client_registry": cr,
                        "tb": tb,
                        "collector": collector,
                        "temperature": temperature,
                    },
                )
            except Exception as e:
                print(f"      Exception at step {i}: {e}")
                response = Triples(triples=[])
            model_responses.append(response)
            model_messages.append(Message(role="assistant", content=str(response)))

        # Collect all triples from this model version
        for response in model_responses:
            all_model_version_triples.extend(response.triples)
        print(f"      Collected {sum(len(r.triples) for r in model_responses)} triples")

    # Vote: keep triples appearing in ≥50% of model versions
    triple_counts = {}
    for triple in all_model_version_triples:
        # Create a unique key for each triple (case-insensitive to handle variations)
        key = f"{triple.head.lower()}|{triple.relation.lower()}|{triple.tail.lower()}"
        if key not in triple_counts:
            triple_counts[key] = {"count": 0, "example": triple}
        triple_counts[key]["count"] += 1

    # Select triples that appear in at least half of the model versions
    threshold = n_samples // 2
    consensus_triples = [
        data["example"]
        for key, data in triple_counts.items()
        if data["count"] >= threshold
    ]

    print(
        f"    Consensus: {len(consensus_triples)} triples (threshold: {threshold}/{n_samples})"
    )

    # Create final response with consensus triples
    consensus_response = Triples(triples=consensus_triples)
    responses.append(consensus_response)
    messages.append(Message(role="assistant", content=str(consensus_response)))


def extract_rels_tot(
    messages,
    responses,
    text,
    prompts,
    n_paths=3,
    strategy="vote",
    examples_content="",
    collector=None,
    tb=None,
):
    """
    Tree-of-Thoughts extraction with multiple reasoning paths.

    Args:
        messages: Message history
        responses: Response list to append to
        text: Document text
        prompts: Extraction prompts
        n_paths: Number of reasoning paths to explore (default=3)
        strategy: How to combine results - 'vote', 'best', or 'merge'
    """
    print(f"  Running ToT extraction with n={n_paths} paths, strategy={strategy}")

    # First extraction step
    if examples_content:
        messages[-1].content += f"\n{examples_content}"
    response = b.GeneralChatExtractRelationships(
        messages,
        baml_options={"client_registry": cr, "tb": tb, "collector": collector},
    )
    responses.append(response)
    messages.append(Message(role="assistant", content=str(response)))

    for prompt_idx, prompt in enumerate(prompts):
        print(f"  ToT Step {prompt_idx + 1}/{len(prompts)}: {prompt[:60]}...")

        # Step 1: Generate reasoning strategies using BAML
        print(f"    Generating {n_paths} reasoning strategies via LLM...")

        from prompts import interactions_type

        task_description = (
            f"Extract {interactions_type} interactions from biomedical text"
        )

        strategies_response = b.GenerateToTStrategies(
            task_description=task_description,
            n_paths=n_paths,
            text=text[:1000],  # Use first 1000 chars for strategy generation
            baml_options={"client_registry": cr, "tb": tb, "collector": collector},
        )
        strategies = [
            {"name": s.name, "focus": s.focus, "avoid": s.avoid}
            for s in strategies_response.strategies
        ]
        print(f"    Generated {len(strategies)} strategies successfully")

        # Step 2: Extract relations using each strategy
        all_path_results = []
        all_path_evaluations = []

        for path_idx, strategy_dict in enumerate(strategies):
            print(f"    Path {path_idx + 1}/{n_paths}: {strategy_dict['name']}")

            # Extract using this strategy
            # Use messages.copy() to prevent each path from polluting other paths' message history
            path_messages = messages.copy()
            from prompts import confidence_prompt, tot_path_extraction_prompt

            extraction_prompt = tot_path_extraction_prompt.format(
                interactions_type=interactions_type,
                strategy_name=strategy_dict["name"],
                strategy_focus=strategy_dict["focus"],
                strategy_avoid=strategy_dict["avoid"],
                confidence_prompt=confidence_prompt,
            )
            content = f"\n{prompt}\n\n{extraction_prompt}"
            if examples_content:
                content += f"\n{examples_content}"
            path_messages.append(Message(role="user", content=content))

            try:
                path_response = b.GeneralChatExtractRelationships(
                    rel_system_prompt,
                    text,
                    path_messages,
                    baml_options={
                        "client_registry": cr,
                        "tb": tb,
                        "collector": collector,
                    },
                )
                print(f"      Extracted: {len(path_response.triples)} triples")
                all_path_results.append(path_response.triples)

                # Step 3: Evaluate this path using BAML
                try:
                    path_eval_response = b.EvaluateToTPath(
                        text=text,
                        extracted_triples=path_response,
                        strategy_name=strategy_dict["name"],
                        task_description=task_description,
                        baml_options={
                            "client_registry": cr,
                            "tb": tb,
                            "collector": collector,
                        },
                    )

                    # Convert BAML evaluation to our internal format
                    path_eval = []
                    for eval_triple in path_eval_response.evaluated_triples:
                        # Find matching triple from extraction
                        matching_triple = None
                        for triple in path_response.triples:
                            if (
                                triple.head.lower() == eval_triple.head.lower()
                                and triple.tail.lower() == eval_triple.tail.lower()
                            ):
                                matching_triple = triple
                                break

                        if matching_triple:
                            path_eval.append(
                                {
                                    "triple": matching_triple,
                                    "score": eval_triple.score,
                                    "evidence": eval_triple.evidence,
                                    "path": path_idx,
                                }
                            )

                    print(
                        f"      Evaluated: avg score = {sum(e['score'] for e in path_eval) / len(path_eval):.1f}"
                        if path_eval
                        else "      Evaluated: no matches"
                    )
                    all_path_evaluations.append(path_eval)

                except Exception as e:
                    print(f"      Evaluation failed: {e}, using default scores")
                    # Fallback to simple scoring based on confidence attribute
                    path_eval = []
                    for triple in path_response.triples:
                        score = (
                            8
                            if not hasattr(triple, "confidence")
                            or triple.confidence == "high"
                            else 5
                        )
                        path_eval.append(
                            {"triple": triple, "score": score, "path": path_idx}
                        )
                    all_path_evaluations.append(path_eval)

            except Exception as e:
                print(f"      Exception in path {path_idx + 1}: {e}")
                all_path_results.append([])
                all_path_evaluations.append([])

        # Step 4: Combine results based on strategy
        if strategy == "vote":
            # Use default threshold (majority = ceil(n/2))
            final_triples = combine_by_voting(all_path_results)
        elif strategy == "best":
            final_triples = combine_by_best_path(all_path_results, all_path_evaluations)
        elif strategy == "merge":
            final_triples = combine_by_merging(all_path_results, all_path_evaluations)
        else:
            # Default to voting
            final_triples = combine_by_voting(all_path_results)

        print(f"    Final result: {len(final_triples)} triples")

        # Create final response
        final_response = Triples(triples=final_triples)
        responses.append(final_response)
        messages.append(Message(role="user", content=f"\nUSER QUESTION: {prompt}"))
        messages.append(Message(role="assistant", content=str(final_response)))
