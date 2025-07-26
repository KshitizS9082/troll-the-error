from faiss_utils import load_template_tags, embed_texts, build_faiss_index, save_index

texts, filenames = load_template_tags('templates/template_meta.json')
vectors, embedder = embed_texts(texts)
index = build_faiss_index(vectors)
save_index(index, "faiss_template.index")
