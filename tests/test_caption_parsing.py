from gradio_app import parse_llm_caption

def test_parse_two_lines():
    top, bottom = parse_llm_caption("Foo\nBar")
    assert top == "Foo" and bottom == "Bar"

def test_parse_extra_output():
    messy = 'Here is a meme:\n"First Line"\n"Second Line"'
    top, bottom = parse_llm_caption(messy)
    assert top and bottom and len([top, bottom]) == 2

def test_parse_single_line():
    top, bottom = parse_llm_caption("Only line")
    assert top == bottom == "Only line"
