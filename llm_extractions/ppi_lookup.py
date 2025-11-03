"""
PPI Lookup utilities for STRING database integration.
"""

import json
import os
import re
import tempfile
from collections import defaultdict

from whoosh import index
from whoosh.analysis import StandardAnalyzer
from whoosh.fields import TEXT, Schema
from whoosh.qparser import FuzzyTermPlugin, QueryParser

from baml.baml_client.types import Message


def load_string_data(string_ppi_path="/prj/LINDA_LLM/STRING/string_ppi.tsv"):
    """Load STRING PPI data into a defaultdict."""
    protein_to_ppis = defaultdict(list)
    try:
        with open(string_ppi_path, "r") as f:
            header_skipped = False
            for line in f:
                if not header_skipped:
                    header_skipped = True
                    continue  # skip header
                parts = line.strip().split("\t")
                if len(parts) >= 10:
                    protein1, protein2 = parts[0], parts[1]
                    try:
                        combined_score = float(parts[9])
                        if combined_score > 400:  # only high confidence
                            protein_to_ppis[protein1.lower()].append(
                                (protein2, combined_score)
                            )
                            protein_to_ppis[protein2.lower()].append(
                                (protein1, combined_score)
                            )
                    except ValueError:
                        continue  # skip invalid lines
        print(f"Loaded STRING PPIs for {len(protein_to_ppis)} proteins.")
    except FileNotFoundError:
        print(f"STRING PPI file not found at {string_ppi_path}.")
        protein_to_ppis = {}
    return protein_to_ppis


def load_synonyms(synonyms_path="/prj/LINDA_LLM/outputs/regu_test_names.json"):
    """Load synonyms dictionary."""
    synonyms = {}
    try:
        with open(synonyms_path, "r") as f:
            synonyms = json.load(f)
        print(f"Loaded synonyms for {len(synonyms)} terms.")
    except FileNotFoundError:
        print(f"Synonyms file not found at {synonyms_path}.")
        synonyms = {}
    return synonyms


def create_whoosh_index(protein_to_ppis):
    """Create Whoosh index for fuzzy protein name search."""
    schema = Schema(name=TEXT(stored=True, analyzer=StandardAnalyzer()))
    index_dir = tempfile.mkdtemp()
    ix = index.create_in(index_dir, schema)
    writer = ix.writer()
    for protein in protein_to_ppis:
        writer.add_document(name=protein)
    writer.commit()
    print(f"Created Whoosh index with {len(protein_to_ppis)} proteins.")
    return ix


def fuzzy_match(ne, ix, protein_to_ppis):
    """Fuzzy match entity against STRING proteins using Whoosh."""
    clean_ne = re.sub(r"[^\w]", "", ne.lower())
    if not clean_ne:
        return None

    with ix.searcher() as searcher:
        parser = QueryParser("name", ix.schema)
        parser.add_plugin(FuzzyTermPlugin())
        query = parser.parse(clean_ne + "~2")
        results = searcher.search(query, limit=1)

        if results:
            matched_protein = results[0]["name"]
            return protein_to_ppis[matched_protein]

    return None


def lookup_infos(messages, responses, protein_to_ppis, synonyms, ix):
    """Look up background knowledge for named entities from STRING database."""
    infos = {}
    nes = responses[-1]  # Get the last response (Entities)

    for ne in nes.entities:
        # Check direct match in STRING db
        if ne.lower() in protein_to_ppis:
            ppis = protein_to_ppis[ne.lower()]
        # Check synonyms
        elif ne in synonyms and any(
            syn.lower() in protein_to_ppis for syn in synonyms[ne]
        ):
            syn_match = next(
                syn for syn in synonyms[ne] if syn.lower() in protein_to_ppis
            )
            ppis = protein_to_ppis[syn_match.lower()]
        # Fuzzy match
        else:
            ppis = fuzzy_match(ne, ix, protein_to_ppis)

        if ppis:
            # Sort by score desc, take top 5
            ppis_sorted = sorted(ppis, key=lambda x: x[1], reverse=True)[:5]
            ppi_str = ", ".join(f"{p} ({s:.0f})" for p, s in ppis_sorted)
            infos[ne] = f"Known PPIs: {ppi_str}"

    messages.append(Message(role="user", content=f"BACKGROUND KNOWLEDGE: {infos}\n"))
