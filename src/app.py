import gradio as gr
import os
from dotenv import load_dotenv
from src.core.balance_sheet import process_document
from src.core.vanna_core import run_vanna_query

# --- Gradio Interface ---
with gr.Blocks(title="Financial Data Assistant") as app:
    with gr.Tabs(selected="chat_tab") as tabs:
        with gr.Tab("Chat", id="chat_tab"):
            gr.Markdown("## 💬 Query Financial Database")
            with gr.Row():
                # Left Panel - Chat
                with gr.Column(scale=1):
                    question = gr.Textbox(label="Ask a question", placeholder="E.g.: What's the cash balance for TDS in Q1 2025?")
                    submit_btn = gr.Button("Submit")
                    final_answer_output = gr.Textbox(label="Final Answer")
                    
                # Right Panel - Results
                with gr.Column(scale=2):
                    sql_output = gr.Code(label="Generated SQL", language="sql")
                    dataframe_output = gr.Dataframe(label="Query Results", wrap=True)
                    plot_output = gr.Plot(label="Visualization", container=True)
            
            submit_btn.click(
                fn=run_vanna_query
                , inputs=question
                , outputs=[sql_output, dataframe_output, plot_output, final_answer_output]
            )
        
        with gr.Tab("Add Documents", id="docs_tab"):
            gr.Markdown("## Upload PDF Documents")
            with gr.Row():
                with gr.Column(scale=1):
                    file_upload = gr.File(
                        file_types=[".pdf"]
                        , label="Drag PDF here"
                        , type="binary"
                    )
                    upload_btn = gr.Button("Process Document")
                    upload_status = gr.Markdown()
                
                with gr.Column(scale=3):
                    # Company Information Card
                    with gr.Group():
                        gr.Markdown("### Company Information")
                        with gr.Row():
                            company_name = gr.Textbox(label="Company Name", interactive=False)
                            stock_code = gr.Textbox(label="Stock Code", interactive=False)
                            report_date = gr.Textbox(label="Period", interactive=False)
                            currency = gr.Textbox(label="Currency", interactive=False)
                    
                    # Balance Sheet Display
                    with gr.Group():
                        gr.Markdown("### Balance Sheet Items")
                        balance_sheet_table = gr.Dataframe(
                            headers=["Code", "Item", "Period End", "Year Start"]
                            , datatype=["str", "str", "number", "number"]
                            , interactive=False
                            , wrap=True
                        )
            
            # Connect the upload button
            upload_btn.click(
                fn=process_document
                , inputs=file_upload
                , outputs=[
                    upload_status
                    , company_name
                    , stock_code
                    , report_date
                    , currency
                    , balance_sheet_table
                ]
            )

app.launch()