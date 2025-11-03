import csv

# Utility functions
import os
import pickle
from parser import args
from pathlib import Path

from langchain_core.documents.base import Document
from langchain_text_splitters import MarkdownTextSplitter

from paths import regulatome_ppi_eval_path, regulatome_tf_eval_path

text_splitter = MarkdownTextSplitter(
    chunk_size=args.chunksize,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)


def load_pickle_objects(path, as_set=False):
    """Load all objects from a pickle file. If as_set, return set of file paths."""
    result = set() if as_set else []
    try:
        with open(path, "rb") as f:
            while True:
                try:
                    obj = pickle.load(f)
                    if as_set:
                        result.add(str(obj[0].metadata["file_path"]))
                    else:
                        result.append(obj)
                except EOFError:
                    break
    except FileNotFoundError:
        pass
    return result


def load_eval_data(eval_path):
    """Load evaluation data from a tab-separated file."""
    with open(eval_path, "r") as f:
        eval_data = [
            (x.split("\t")[0], x.split("\t")[1], x.split("\t")[2].strip())
            for x in f.readlines()[1:]
        ]
    eval_data = [
        {"file_stem": x[0], "relations": x[1], "split": x[2]} for x in eval_data
    ]
    return eval_data


def load_align_dict(csv_path):
    """Load alignment dictionary from a CSV file."""
    align_dict = dict()
    with open(csv_path, mode="r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for id, pmc in reader:
            if pmc:
                align_dict[pmc] = id
    return align_dict


def write_documents(
    chunk_pkl_path, paper_pkl_path, test_paper_paths, chunk_file_paths, paper_file_paths
):
    """Write chunked and full documents to pickle files if not already present."""
    if args.force_new:
        with (
            open(chunk_pkl_path, "wb") as chunk_file,
            open(paper_pkl_path, "wb") as doc_file,
        ):
            pass
    with (
        open(chunk_pkl_path, "ab+") as chunk_file,
        open(paper_pkl_path, "ab+") as doc_file,
    ):
        for i, test_paper_path in enumerate(test_paper_paths):
            if not args.force_new and (
                str(test_paper_path) in paper_file_paths
                and str(test_paper_path) in chunk_file_paths
            ):
                continue
            text = open(test_paper_path, "r").read().strip()
            if text:
                texts = text_splitter.create_documents([text])
                doc = Document(
                    page_content=text, metadata={"file_path": test_paper_path}
                )
                for chunk in texts:
                    chunk.metadata = {"file_path": test_paper_path}
                    pickle.dump((chunk, i), chunk_file)
                pickle.dump((doc, i), doc_file)


def get_config():
    """Return all configuration variables for paths and ner files."""
    all_ne_paths = None
    true_ne_paths = None
    spacy_ne_paths = None
    if args.data == "biored":
        _paper_paths = Path(
            "/beegfs/prj/LINDA_LLM/RegulaTome/BIORED/BIORED/src/corpus/test"
        )
    elif args.data == "regulatome":
        _paper_paths = Path(
            "/beegfs/prj/LINDA_LLM/RegulaTome/test_ppi_annotations/regulatome_extraction_13_12_2024/src/corpus"
        )
        if args.target == "ppi":
            _all_ne_paths = Path(
                "/beegfs/prj/LINDA_LLM/RegulaTome/test_ppi_annotations/regulatome_extraction_13_12_2024/src/entities"
            )
            all_ne_paths = list(_all_ne_paths.glob(f"*"))
            _true_ne_paths = Path(
                "/beegfs/prj/LINDA_LLM/RegulaTome/test_ppi_annotations/regulatome_extraction_13_12_2024/src/entities_relations_ppi"
            )
            true_ne_paths = list(_true_ne_paths.glob(f"*"))
            _spacy_ne_paths = Path(
                "/home/pwiesenbach/RegulaTome_extraction-1/LargeScaleRelationExtractionPipeline/spacy/ppi/test"
            )
            spacy_ne_paths = list(_spacy_ne_paths.glob(f"*.ann"))
        elif args.target == "tf":
            _all_ne_paths = Path(
                "/beegfs/prj/LINDA_LLM/RegulaTome/test_ppi_annotations/regulatome_extraction_13_12_2024/src/entities"
            )
            all_ne_paths = list(_all_ne_paths.glob(f"*"))
            _true_ne_paths = Path(
                "/beegfs/prj/LINDA_LLM/RegulaTome/test_ppi_annotations/regulatome_extraction_13_12_2024/src/entities_relations_tf"
            )
            true_ne_paths = list(_true_ne_paths.glob(f"*"))
            _spacy_ne_paths = Path(
                "/home/pwiesenbach/RegulaTome_extraction-1/LargeScaleRelationExtractionPipeline/spacy/grn/test"
            )
            spacy_ne_paths = list(_spacy_ne_paths.glob(f"*.ann"))
    elif args.data == "regulatomepapers":
        _paper_paths = Path("/prj/LINDA_LLM/outputs/parsed_papers/regu_test")
    elif args.data == "cardio":
        if args.target == "ppi":
            _paper_paths = Path("/prj/LINDA_LLM/outputs/parsed_papers/CardioPrior/ppi")
        elif args.target == "tf":
            _paper_paths = Path("/prj/LINDA_LLM/outputs/parsed_papers/CardioPrior/tf")
    elif args.data == "5curated":
        _paper_paths = Path(
            f"/beegfs/prj/LINDA_LLM/outputs/parsed_papers/ppi/{args.parser}/5curated/"
        )
    # ending_dict = {"marker": "md", "llama_parse": "txt", "pymupdf4llm": "md"}
    # ending = ending_dict[args.parser] if args.data != "regulatomepapers" else "md"
    # paper_paths = list(_paper_paths.glob(f"*.{ending}"))
    paper_paths = list(_paper_paths.glob("*.txt"))
    return all_ne_paths, true_ne_paths, spacy_ne_paths, paper_paths


def get_texts():
    _, _, _, paper_paths = get_config()

    if args.data in ["regulatome", "regulatomepapers"]:
        if args.target == "ppi":
            regulatome_eval_path = regulatome_ppi_eval_path
        elif args.target == "tf":
            regulatome_eval_path = regulatome_tf_eval_path
        eval_data = load_eval_data(regulatome_eval_path)
        test_data = [x["file_stem"] for x in eval_data if x["split"] == "Test"]
        if args.data == "regulatomepapers":
            csv_path = "/prj/LINDA_LLM/resources/pmid_to_pmcid_mapped_test.csv"
            align_dict = load_align_dict(csv_path)
            test_paper_paths = [
                x for x in paper_paths if align_dict.get(x.stem) in test_data
            ]
        elif args.data == "regulatome":
            test_paper_paths = [x for x in paper_paths if x.stem in test_data]
    else:
        test_paper_paths = paper_paths

    chunk_pkl_path = Path(
        f"/beegfs/prj/LINDA_LLM/outputs/docs/{args.data}/{args.target}/{args.parser}/paper_chunks_{args.chunksize}.pkl"
    )
    os.makedirs(chunk_pkl_path.parent, exist_ok=True)
    paper_pkl_path = chunk_pkl_path.parent / "papers.pkl"
    os.makedirs(paper_pkl_path.parent, exist_ok=True)

    chunk_file_paths = load_pickle_objects(chunk_pkl_path, as_set=True)
    paper_file_paths = load_pickle_objects(paper_pkl_path, as_set=True)

    write_documents(
        chunk_pkl_path,
        paper_pkl_path,
        test_paper_paths,
        chunk_file_paths,
        paper_file_paths,
    )

    test_chunks = load_pickle_objects(chunk_pkl_path)
    test_docs = load_pickle_objects(paper_pkl_path)

    texts = test_docs if args.doclevel == "docs" else test_chunks
    return texts


# Make variables importable
all_nes_paths, true_ne_paths, spacy_ne_paths, paper_paths = get_config()
texts = get_texts()
