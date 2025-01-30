import json
from parser import args

from get_documents import paper_dict
from json_repair import repair_json
from langchain_community.graphs.graph_document import GraphDocument, Node, Relationship
from utils import Timeout


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


def parse_ners(ner_answer, kw):
    if "parsed" in ner_answer and ner_answer["parsed"]:
        ners = ner_answer["parsed"].model_dump()
    elif "tool_calls" in ner_answer.additional_kwargs and kw in repair_json(
        ner_answer.additional_kwargs["tool_calls"][0]["function"]["arguments"],
        return_objects=True,
    ):
        ners = repair_json(
            ner_answer.additional_kwargs["tool_calls"][0]["function"]["arguments"],
            return_objects=True,
        )
    elif "raw" in ner_answer and "tool_calls" in ner_answer["raw"].additional_kwargs:
        ners = ner_answer["raw"].additional_kwargs["tool_calls"][0]["function"][
            "arguments"
        ]
    elif "raw" in ner_answer and (
        "tool_calls" in ner_answer["raw"].response_metadata["message"]
    ):
        ners = ner_answer["raw"].response_metadata["message"]["tool_calls"][0][
            "function"
        ]["arguments"]
    elif (
        "tool_calls" in ner_answer.response_metadata["message"]
        and ner_answer.response_metadata["message"]["tool_calls"][0]["function"][
            "arguments"
        ]
    ):
        ners = ner_answer.response_metadata["message"]["tool_calls"][0]["function"][
            "arguments"
        ]
    return str(ners)
