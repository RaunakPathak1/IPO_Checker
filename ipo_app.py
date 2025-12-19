from ipo_evaluator import ipo_evaluator
import gradio as gr

def main():
    chat = gr.ChatInterface(fn=ipo_evaluator)
    chat.launch(inbrowser = True)

if __name__ == "__main__":
    main()