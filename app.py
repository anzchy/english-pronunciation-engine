import gradio as gr
import re
from core.pronunciation_assessment import run_pronunciation_assessment
import os
import datetime
import io
from flask import send_file

def split_text(text):
    # Split text by comma or space
    words = re.split(r'[,\s]+', text.strip())
    # Ensure exactly 5 words, pad with empty strings if needed
    words = (words + [''] * 5)[:5]
    return words[0], words[1], words[2], words[3], words[4]

def evaluate_pronunciation(audio1, audio2, audio3, audio4, audio5, word1, word2, word3, word4, word5):
    try:
        evaluation_results = []
        for audio, word in zip([audio1, audio2, audio3, audio4, audio5], 
                              [word1, word2, word3, word4, word5]):
            if audio is not None:
                scores = run_pronunciation_assessment(audio, word)
                evaluation_results.append(f"Pronunciation score for '{word}': {scores['pronunciation_score']}, Accuracy: {scores['accuracy']}, Fluency: {scores['fluency']}, Prosody: {scores['prosody']}, Completeness: {scores['completeness']}")
            else:
                evaluation_results.append("No audio recorded")
        return evaluation_results
    except Exception as e:
        return f"Error: {e}"

def export_results(result1, result2, result3, result4, result5):
    now = datetime.datetime.now()
    filename = f"{now.strftime('%Y%m%d%M%S')}-evaluation_results.md"
    markdown_content = f"""# Pronunciation Evaluation Results

1. {result1}
2. {result2}
3. {result3}
4. {result4}
5. {result5}
"""
    return send_file(
        io.BytesIO(markdown_content.encode()),
        mimetype="text/markdown",
        as_attachment=True,
        download_name=filename
    )

with gr.Blocks(css="#app { font-size: 2.0rem; }") as app:
    # Input text area and control buttons
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(label="Enter five words (separated by commas or spaces)", 
                                  container=True)
        with gr.Column():
            split_btn = gr.Button("Split text", variant="primary")
            evaluate_btn = gr.Button("evaluate", variant="primary")
            download_btn = gr.Button("Download Markdown", variant="primary")

    # Words and recording sections
    with gr.Row():
        with gr.Column():
            word_1 = gr.Textbox(label="Word_1")
            audio_1 = gr.Audio(type="filepath", label="Record_1")
            download_1 = gr.Button("Download Audio 1", variant="primary")
        with gr.Column():
            result_1 = gr.Textbox(label="Evaluation_result_1")
            download_audio_1 = gr.File(label="Download Audio 1")
    
    with gr.Row():
        with gr.Column():
            word_2 = gr.Textbox(label="Word_2")
            audio_2 = gr.Audio(type="filepath", label="Record_2")
            download_2 = gr.Button("Download Audio 2", variant="primary")
        with gr.Column():
            result_2 = gr.Textbox(label="Evaluation_result_2")
            download_audio_2 = gr.File(label="Download Audio 2")
    
    with gr.Row():
        with gr.Column():
            word_3 = gr.Textbox(label="Word_3")
            audio_3 = gr.Audio(type="filepath", label="Record_3")
            download_3 = gr.Button("Download Audio 3", variant="primary")
        with gr.Column():
            result_3 = gr.Textbox(label="Evaluation_result_3")
            download_audio_3 = gr.File(label="Download Audio 3")
    
    with gr.Row():
        with gr.Column():
            word_4 = gr.Textbox(label="Word_4")
            audio_4 = gr.Audio(type="filepath", label="Record_4")
            download_4 = gr.Button("Download Audio 4", variant="primary")
        with gr.Column():
            result_4 = gr.Textbox(label="Evaluation_result_4")
            download_audio_4 = gr.File(label="Download Audio 4")
    
    with gr.Row():
        with gr.Column():
            word_5 = gr.Textbox(label="Word_5")
            audio_5 = gr.Audio(type="filepath", label="Record_5")
            download_5 = gr.Button("Download Audio 5", variant="primary")
        with gr.Column():
            result_5 = gr.Textbox(label="Evaluation_result_5")
            download_audio_5 = gr.File(label="Download Audio 5")

    # Event handlers
    split_btn.click(
        fn=split_text,
        inputs=[input_text],
        outputs=[word_1, word_2, word_3, word_4, word_5]
    )

    evaluate_btn.click(
        fn=evaluate_pronunciation,
        inputs=[audio_1, audio_2, audio_3, audio_4, audio_5,
                word_1, word_2, word_3, word_4, word_5],
        outputs=[result_1, result_2, result_3, result_4, result_5]
    )

    download_btn.click(
        fn=export_results,
        inputs=[result_1, result_2, result_3, result_4, result_5],
        outputs=gr.Textbox(label="Download Status")
    )

# Launch the app with specified host and port
app.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))