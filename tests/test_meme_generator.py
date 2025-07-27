import os
from meme_generator import create_meme

def test_meme_image_created():
    img_path = "tests/tmp_image.jpg"
    template = "success_kid.jpg"  # update to one you have in templates/
    create_meme(template, "HELLO", "WORLD", output_path=img_path)
    assert os.path.exists(img_path) and os.path.getsize(img_path) > 1000
    os.remove(img_path)
