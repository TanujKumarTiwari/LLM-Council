import gradio as gr
from council import run_council

def run(question):
    decision = run_council(question)
    return decision.__dict__



gr.Interface(
    fn=run,
    inputs="text",
    outputs="json",
    title="LLM Council"
).launch(share=True)
