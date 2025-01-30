import json
from hashlib import md5
from parser import args
from typing import List

from get_documents import paper_dict
from json_repair import repair_json
from langchain_community.graphs import Neo4jGraph
from langchain_community.graphs.graph_document import GraphDocument, Node, Relationship
from pydantic import BaseModel, Field
from utils import Timeout

BASE_ENTITY_LABEL = "__Entity__"
EXCLUDED_LABELS = ["_Bloom_Perspective_", "_Bloom_Scene_"]
EXCLUDED_RELS = ["_Bloom_HAS_SCENE_"]
EXHAUSTIVE_SEARCH_LIMIT = 10000
LIST_LIMIT = 128
# Threshold for returning all available prop values in graph schema
DISTINCT_VALUE_LIMIT = 10

include_docs_query = (
    "MERGE (d:Document {id:$document.metadata.id}) "
    # "SET d.text = $document.page_content "  # we don't want the page content as text property as the relations take care of that
    "SET d += $document.metadata "
    "WITH d "
)


def escape_json(s):
    _s = ""
    for ss in s:
        _s += ss
        if ss in ["{", "}"]:
            _s += ss
    return _s


def _remove_backticks(text: str) -> str:
    return text.replace("`", "")


def _get_node_import_query(baseEntityLabel: bool, include_source: bool) -> str:
    if baseEntityLabel:
        return (
            f"{include_docs_query if include_source else ''}"
            "UNWIND $data AS row "
            f"MERGE (source:`{BASE_ENTITY_LABEL}` {{id: row.id}}) "
            "SET source += row.properties "
            f"{'MERGE (d)-[:MENTIONS]->(source) ' if include_source else ''}"
            "WITH source, row "
            "CALL apoc.create.addLabels( source, [row.type] ) YIELD node "
            "RETURN distinct 'done' AS result"
        )
    else:
        return (
            f"{include_docs_query if include_source else ''}"
            "UNWIND $data AS row "
            "CALL apoc.merge.node([row.type], {id: row.id}, "
            "row.properties, {}) YIELD node "
            f"{'MERGE (d)-[:MENTIONS]->(node) ' if include_source else ''}"
            "RETURN distinct 'done' AS result"
        )


def _get_rel_import_query(baseEntityLabel: bool) -> str:
    if baseEntityLabel:
        return (
            "UNWIND $data AS row "
            f"MERGE (source:`{BASE_ENTITY_LABEL}` {{id: row.source}}) "
            f"MERGE (target:`{BASE_ENTITY_LABEL}` {{id: row.target}}) "
            "WITH source, target, row "
            "CALL apoc.merge.relationship(source, row.type, "
            "{}, row.properties, target) YIELD rel "
            "RETURN distinct 'done'"
        )
    else:
        return (
            # "MATCH (d:Document {id:$document.metadata.id}) "
            # "WITH d "
            "UNWIND $data AS row "
            "CALL apoc.merge.node([row.source_label], {id: row.source},"
            "{}, {}) YIELD node as source "
            "CALL apoc.merge.node([row.target_label], {id: row.target},"
            "{}, {}) YIELD node as target "
            "CALL apoc.merge.relationship(source, row.type, {}, row.properties, target) YIELD rel "
            "SET rel.texts = coalesce(rel.texts, []) + row.text "  # here, we collect all the text chunks where a relation was found
            # "SET rel.texts = coalesce(rel.texts, []) + [row.text, d.id] "
            "RETURN distinct 'done' "
        )


class MyNeo4jGraph(Neo4jGraph):
    def add_graph_documents(
        self,
        graph_documents: List[GraphDocument],
        include_source: bool = False,
        baseEntityLabel: bool = False,
    ) -> None:
        """
        This method constructs nodes and relationships in the graph based on the
        provided GraphDocument objects.

        Parameters:
        - graph_documents (List[GraphDocument]): A list of GraphDocument objects
        that contain the nodes and relationships to be added to the graph. Each
        GraphDocument should encapsulate the structure of part of the graph,
        including nodes, relationships, and the source document information.
        - include_source (bool, optional): If True, stores the source document
        and links it to nodes in the graph using the MENTIONS relationship.
        This is useful for tracing back the origin of data. Merges source
        documents based on the `id` property from the source document metadata
        if available; otherwise it calculates the MD5 hash of `page_content`
        for merging process. Defaults to False.
        - baseEntityLabel (bool, optional): If True, each newly created node
        gets a secondary __Entity__ label, which is indexed and improves import
        speed and performance. Defaults to False.
        """
        if baseEntityLabel:  # Check if constraint already exists
            constraint_exists = any(
                [
                    el["labelsOrTypes"] == [BASE_ENTITY_LABEL]
                    and el["properties"] == ["id"]
                    for el in self.structured_schema.get("metadata", {}).get(
                        "constraint", []
                    )
                ]
            )

            if not constraint_exists:
                # Create constraint
                self.query(
                    f"CREATE CONSTRAINT IF NOT EXISTS FOR (b:{BASE_ENTITY_LABEL}) "
                    "REQUIRE b.id IS UNIQUE;"
                )
                self.refresh_schema()  # Refresh constraint information

        node_import_query = _get_node_import_query(baseEntityLabel, include_source)
        rel_import_query = _get_rel_import_query(baseEntityLabel)
        for document in graph_documents:
            if not document.source.metadata.get("id"):
                document.source.metadata["id"] = md5(
                    document.source.page_content.encode("utf-8")
                ).hexdigest()

            # Remove backticks from node types
            for node in document.nodes:
                node.type = _remove_backticks(node.type)
            # Import nodes
            self.query(
                node_import_query,
                {
                    "data": [el.__dict__ for el in document.nodes],
                    "document": document.source.__dict__,
                },
            )
            # Import relationships
            self.query(
                rel_import_query,
                {
                    "document": document.source.__dict__,
                    "data": [
                        {
                            "source": el.source.id,
                            "source_label": _remove_backticks(el.source.type),
                            "target": el.target.id,
                            "target_label": _remove_backticks(el.target.type),
                            "type": _remove_backticks(
                                el.type.replace(" ", "_").upper()
                            ),
                            "properties": el.properties,
                            "text": document.source.page_content,
                        }
                        for el in document.relationships
                    ],
                },
            )


def parse_msg2triples(message):
    if "parsed" in message.additional_kwargs and message.additional_kwargs["parsed"]:
        output = message.additional_kwargs["parsed"].model_dump()["triples"]
    elif (
        "raw" in message.additional_kwargs
        and "message" in message.additional_kwargs["raw"].response_metadata
    ):
        output = message.additional_kwargs["raw"].response_metadata["message"][
            "tool_calls"
        ][0]["function"]["arguments"]["triples"]
        if isinstance(output, str):
            output = repair_json(output, return_objects=True)
    if (
        "message" in message.response_metadata
        and "tool_calls" in message.response_metadata["message"]
    ):
        if isinstance(
            message.response_metadata["message"]["tool_calls"][0]["function"][
                "arguments"
            ],
            dict,
        ):
            obj = message.response_metadata["message"]["tool_calls"][0]["function"][
                "arguments"
            ]["triples"]
        else:
            obj = message.response_metadata["message"]["tool_calls"][0]["function"][
                "arguments"
            ]
        output = repair_json(obj, return_objects=True)
    elif (
        "message" in message.response_metadata
        and "content" in message.response_metadata["message"]
    ):
        obj = repair_json(
            message.response_metadata["message"]["content"], return_objects=True
        )
        if (
            isinstance(obj, dict)
            and "parameters" in obj
            and "triples" in obj["parameters"]
        ):
            output = obj["parameters"]["triples"]
        else:
            output = list()
    elif "tool_calls" in message.additional_kwargs:
        output = repair_json(
            message.additional_kwargs["tool_calls"][0]["function"]["arguments"],
            return_objects=True,
        )["triples"]
    else:
        output = []
    if not output:
        return output
    if isinstance(output, list) and isinstance(output[0], str):
        output = [output]
    triples = list()
    for triple in output:
        if isinstance(triple, dict):
            triple = repair_json(json.dumps(triple), return_objects=True)
            if not all([x in triple for x in ["head", "tail", "relation"]]):
                continue
            triples.append(triple)
        elif isinstance(triple, str):
            triple = json.loads(repair_json(triple))
            if not all([x in triple for x in ["head", "tail", "relation"]]):
                continue
            triples.append(triple)
        elif isinstance(triple, list):
            if len(triple) % 3 if args.simple else 5:
                continue
            for i in range(0, len(triple), 3 if args.simple else 5):
                _triple = {
                    "head": triple[i],
                    "relation": triple[i + 1],
                    "tail": triple[i + 2],
                }
                triples.append(_triple)
    return triples


def build_graphdoc(triples, doc, id):
    nodes_set = set()
    rels = list()
    for triple in triples:
        n1 = triple["head"]
        n2 = triple["tail"]
        nodes_set.add(n1)
        nodes_set.add(n2)
        rels.append(
            Relationship(
                source=Node(id=n1), target=Node(id=n2), type=triple["relation"]
            )
        )
    nodes = [Node(id=el) for el in list(nodes_set)]
    graph_doc = GraphDocument(nodes=nodes, relationships=rels, source=doc)
    graph_doc.source.metadata["source"] = paper_dict[id]
    graph_doc.source.metadata["id"] = str(id)
    return graph_doc


def attempt(tries, seconds, func, args=[], kwargs={}):
    c = 0
    res = None
    while c < tries:
        try:
            with Timeout(seconds):
                res = func(*args, **kwargs)
                break
        except Timeout.Timeout:
            print("Timeout")
            c += 1
    return res


def filter_ners(ners, list):
    return [x for x in ners if x.replace(" ", "").lower() in list]
