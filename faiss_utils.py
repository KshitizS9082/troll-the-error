import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import json

def load_template_tags(meta_path):
    """Load template tags and filenames from provided metadata path."""
    with open(meta_path) as f:
        templates = json.load(f)
    texts = [" ".join(t["tags"]) for t in templates]
    filenames = [t["filename"] for t in templates]
    return texts, filenames

def embed_texts(text_list, model="all-MiniLM-L6-v2"):
    """Embed a list of tag texts using a SentenceTransformer model."""
    embedder = SentenceTransformer(model)
    vectors = embedder.encode(text_list, show_progress_bar=True)
    return vectors, embedder

def build_faiss_index(vectors):
    """Build a FAISS flat L2 index from provided vectors."""
    idx = faiss.IndexFlatL2(vectors.shape[1])
    idx.add(np.array(vectors))
    return idx

def save_index(index, path):
    """Save the FAISS index to disk."""
    faiss.write_index(index, path)

def load_index(path):
    """Load a saved FAISS index from disk."""
    return faiss.read_index(path)

def load_embedder(model_name="all-MiniLM-L6-v2"):
    """Load a SentenceTransformer embedder."""
    return SentenceTransformer(model_name)

def query_template(error_log, embedder, index, filenames):
    """Given an error log, return the best-matching template filename."""
    vector = embedder.encode([error_log])[0]
    D, I = index.search(np.array([vector]), 1)
    return filenames[I[0][0]]
