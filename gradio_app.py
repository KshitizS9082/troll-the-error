import gradio as gr
import uuid
import os

from chains import error_to_caption_chain, select_template, load_faiss_resources
from meme_generator import create_meme

# Load FAISS/index/embedder ONCE for efficiency!
embedder, index, filenames = load_faiss_resources()

def parse_llm_caption(caption):
    # Defensively get exactly two lines
    lines = [line.strip(' "\'') for line in caption.strip().split('\n') if line.strip()]
    # Remove obvious headings
    lines = [l for l in lines if "caption" not in l.lower() and "here is" not in l.lower()]
    if len(lines) >= 2:
        return lines[0], lines[1]
    elif len(lines) == 1:
        return lines[0], lines[0]
    else:
        return "", ""

def troll_the_error_fn(error_log):
    # Generate LLM caption
    caption = error_to_caption_chain.run(error_log=error_log)
    top_text, bottom_text = parse_llm_caption(caption)
    # Select template using FAISS similarity
    template_filename = select_template(error_log, embedder, index, filenames)
    # Create meme image
    output_dir = "output_memes"
    os.makedirs(output_dir, exist_ok=True)
    meme_path = os.path.join(output_dir, f"{uuid.uuid4().hex}.jpg")
    create_meme(template_filename, top_text, bottom_text, output_path=meme_path)
    return meme_path

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# TrollTheError\nGenerate witty memes from your error logs!")
    error_input = gr.Textbox(lines=5, label="Paste your error log here")
    gen_btn = gr.Button("Generate Meme")
    output_img = gr.Image(type="filepath", label="Generated Meme")
    gen_btn.click(fn=troll_the_error_fn, inputs=error_input, outputs=output_img)

if __name__ == "__main__":
    demo.launch()
