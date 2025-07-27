from faiss_utils import load_index, load_embedder, load_template_tags, query_template

def test_template_query_returns_filename():
    embedder = load_embedder()
    index = load_index('faiss_template.index')
    _, filenames = load_template_tags('templates/template_meta.json')
    sample_error = "FileNotFoundError: config"
    filename = query_template(sample_error, embedder, index, filenames)
    assert filename in filenames
