from ipo_evaluator import run_ui_eval
import gradio as gr

demo = gr.Interface(
    fn=run_ui_eval,
    inputs=gr.Textbox(label="Enter IPO Name"),
    outputs=gr.JSON(),
    title="IPO DRHP RAG Evaluator"
)

if __name__ == "__main__":
    demo.launch(inbrowser=True)