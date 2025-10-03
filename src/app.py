import gradio as gr
from src.core.balance_sheet import process_document, get_balance_sheets_general_info
from src.core.vanna_core import run_vanna_query


def reload_general_info():
    return get_balance_sheets_general_info()

# --- Gradio Interface ---
with gr.Blocks(title="Financial Data Assistant") as app:
    with gr.Tabs(selected="chat_tab") as tabs:
        with gr.Tab("Chat", id="chat_tab"):
            gr.Markdown("## 💬 Truy Vấn")
            with gr.Row():
                # Left Panel - Chat
                with gr.Column(scale=1):
                    question = gr.Textbox(label="Đặt câu hỏi", placeholder="E.g.: Tổng tiền mặt của công ty TDS vào quý I 2025 là bao nhiêu?")
                    submit_btn = gr.Button("Submit")
                    final_answer_output = gr.Markdown(label="Trả lời")
                    
                # Right Panel - Results
                with gr.Column(scale=2):
                    # sql_output = gr.Code(label="Ngôn ngữ truy vấn", language="sql")
                    dataframe_output = gr.Dataframe(label="Dữ liệu thô", wrap=True)
                    plot_output = gr.Plot(label="Biểu đồ", container=True)
            
            # Even handler for the submit button
            submit_btn.click(
                fn=run_vanna_query
                , inputs=question
                , outputs=[dataframe_output, plot_output, final_answer_output]
            )
        
        with gr.Tab("Thêm tài liệu", id="docs_tab"):
            gr.Markdown("## Tải tài liệu lên")
            with gr.Row():
                with gr.Column(scale=1):
                    file_upload = gr.File(
                        file_types=[".pdf"]
                        , label="Kéo và thả file tài liệu vào đây"
                        , type="binary"
                    )
                    upload_btn = gr.Button("Bắt đầu xử lý")
                    upload_status = gr.Markdown()
                
                with gr.Column(scale=3):
                    # Company Information Card
                    with gr.Group():
                        gr.Markdown("### Thông tin công ty")
                        with gr.Row():
                            company_name = gr.Textbox(label="Tên", interactive=False)
                            stock_code = gr.Textbox(label="Mã chứng khoán", interactive=False)
                            report_date = gr.Textbox(label="Kỳ báo cáo", interactive=False)
                            currency = gr.Textbox(label="Đơn vị tiền tệ", interactive=False)
                    
                    # Balance Sheet Display
                    with gr.Group():
                        gr.Markdown("### Bảng cân đối tài chính")
                        balance_sheet_table = gr.Dataframe(
                            # headers=["Code", "Item", "Period End", "Year Start"]
                            # , datatype=["str", "str", "number", "number"]
                            headers=["Mã số", "Mục", "Số liệu cuối kỳ", "Số liệu đầu năm"]
                            , datatype=["str", "str", "str", "str"]
                            , interactive=False
                            , wrap=True
                        )
            
            # Even handler for the upload button
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


        # === General Info Tab ===
        with gr.Tab("📑 Báo cáo gần nhất", id="sql_tab"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 🏢 Thông tin báo cáo cân đối kế toán")
                    gr.Markdown(
                        "Bảng dưới đây hiển thị **công ty, mã chứng khoán, kỳ báo cáo, đơn vị tiền tệ** "
                        "và thời điểm cập nhật gần nhất."
                    )
                    refresh_btn = gr.Button("🔄 Làm mới dữ liệu")

                    df_output = gr.Dataframe(
                        headers=["Công ty", "Mã", "Kỳ báo cáo", "Đơn vị tiền tệ", "Cập nhật lúc"],
                        interactive=False,
                        wrap=True,
                        type="pandas"
                    )

            # auto-load on startup
            app.load(fn=reload_general_info, inputs=None, outputs=df_output)

            # allow manual refresh
            refresh_btn.click(fn=reload_general_info, inputs=None, outputs=df_output)

app.launch(server_name="0.0.0.0")