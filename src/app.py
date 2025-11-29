import gradio as gr
import os
from src.core.balance_sheet import process_document, get_balance_sheets_general_info, validate_spreadsheet
from src.core.vanna_core import run_vanna_query
from src.core.translate import stream_translate_live, stream_translate_pdf

uploads_folder = "uploads"

if not os.path.exists(uploads_folder):
    os.makedirs(uploads_folder)

def reload_general_info():
    return get_balance_sheets_general_info()

# --- Gradio Interface ---
with gr.Blocks(title="Báo cáo tài chính") as app:

    with gr.Tabs(selected="docs_tab") as tabs:

        with gr.Tab("✅ Bảng cân đối", id="docs_tab"):
            gr.Markdown("## Tải tài liệu lên")
            with gr.Row():
                with gr.Column(scale=1):
                    file_upload = gr.File(
                        file_types=[".pdf"]
                        , label="Kéo và thả file tài liệu vào đây"
                        , type="filepath"
                    )
                    upload_btn = gr.Button("Bắt đầu xử lý")
                    upload_status = gr.Markdown()

                    # --- NEW: Validate spreadsheet section ---
                    with gr.Accordion("Validate spreadsheet", open=False):
                        spreadsheet_file = gr.File(
                            file_types=[".xlsx", ".xls", ".csv"],
                            label="Chọn file Excel để đối chiếu",
                            type="binary",
                        )
                        validate_btn = gr.Button("Đối chiếu bảng biểu")
                        validation_status = gr.Markdown()
                
                with gr.Column(scale=8):
                    # Company Information Card
                    with gr.Group():
                        gr.Markdown("### Thông tin công ty")
                        with gr.Row():
                            company_name = gr.Textbox(label="Tên", interactive=False)
                            stock_code = gr.Textbox(label="Mã chứng khoán", interactive=False)
                            report_date = gr.Textbox(label="Kỳ báo cáo", interactive=False)
                            currency = gr.Textbox(label="Đơn vị tiền tệ", interactive=False)

                    # Balance Sheet + PDF viewer side by side
                    with gr.Group():
                        gr.Markdown("### Bảng cân đối tài chính")

                        with gr.Row():
                            # LEFT: table
                            with gr.Column(scale=2):
                                balance_sheet_table = gr.Dataframe(
                                    headers=["Mã số", "Mục", "Số liệu cuối kỳ", "Số liệu đầu năm"],
                                    datatype=["str", "str", "str", "str"],
                                    interactive=False,
                                    wrap=True,
                                    elem_id="bst",
                                )
                                gr.HTML("""
                                <style>
                                    #bst table {
                                        width: 100% !important;
                                        table-layout: auto !important;
                                    }
                                    #bst table th,
                                    #bst table td {
                                        white-space: nowrap;
                                    }
                                </style>
                                """)

                            # RIGHT: PDF pages viewer
                            with gr.Column(scale=1):
                                # gr.Markdown("#### Trang PDF chứa bảng cân đối")
                                balance_sheet_pages = gr.Gallery(
                                    label="Bảng cân đối",
                                    columns=1,
                                )

            # Event handler for the upload button
            upload_btn.click(
                fn=process_document,
                inputs=file_upload,
                outputs=[
                    upload_status,
                    company_name,
                    stock_code,
                    report_date,
                    currency,
                    balance_sheet_table,
                    balance_sheet_pages,
                ],
            )

                # Validate spreadsheet click
            validate_btn.click(
                fn=validate_spreadsheet,
                inputs=[balance_sheet_table, spreadsheet_file],
                outputs=[validation_status, balance_sheet_table],
            )

        with gr.Tab("Tra cứu bảng cân đối", id="chat_tab"):
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


        # # === General Info Tab ===
        # with gr.Tab("📑 Báo cáo gần nhất", id="sql_tab"):
        #     with gr.Row():
        #         with gr.Column():
        #             gr.Markdown("### 🏢 Thông tin báo cáo cân đối kế toán")
        #             gr.Markdown(
        #                 "Bảng dưới đây hiển thị **công ty, mã chứng khoán, kỳ báo cáo, đơn vị tiền tệ** "
        #                 "và thời điểm cập nhật gần nhất."
        #             )
        #             refresh_btn = gr.Button("🔄 Làm mới dữ liệu")

        #             df_output = gr.Dataframe(
        #                 headers=["Công ty", "Mã", "Kỳ báo cáo", "Đơn vị tiền tệ", "Cập nhật lúc"],
        #                 interactive=False,
        #                 wrap=True,
        #                 type="pandas"
        #             )

        #     # auto-load on startup
        #     app.load(fn=reload_general_info, inputs=None, outputs=df_output)

        #     # allow manual refresh
        #     refresh_btn.click(fn=reload_general_info, inputs=None, outputs=df_output)
        
        with gr.Tab("✅ Dịch báo cáo"):
            gr.Markdown("### ⌨️ Dịch trực tiếp")

            direction = gr.Radio(
                ["VI → EN", "EN → VI"],
                value="VI → EN",
                label="Direction",
                show_label=False,
                container=False,
            )

            with gr.Row():
                src = gr.Textbox(
                    label="Input",
                    lines=8,
                    placeholder="Type…"
                )
                tgt = gr.Textbox(
                    label="Output",
                    lines=8
                )

            src.input(
                fn=stream_translate_live,
                inputs=[src, direction],
                outputs=tgt,
                show_progress="hidden"
            )

            # --- PDF image-based translation ---
            gr.Markdown("### 📄 Dịch từ PDF")

            with gr.Row():
                with gr.Column(scale=1):
                    pdf_file = gr.File(
                        file_types=[".pdf"],
                        label="Upload PDF",
                        type="binary",
                    )
                    pdf_translate_btn = gr.Button("Translate PDF")

                with gr.Column(scale=2):
                    pdf_output = gr.Textbox(
                        label="PDF Translation",
                        lines=20
                    )

            pdf_translate_btn.click(
                fn=stream_translate_pdf,
                inputs=[pdf_file, direction],
                outputs=pdf_output,
                show_progress="minimal",
            )

        with gr.Tab("✅ Trả lời doanh nghiệp"):
            gr.Markdown("## 💬 Hỏi đáp với tài liệu (RAG)")

            # === Query Section (same layout as Translate tab) ===
            gr.Markdown("### 🔍 Truy vấn")

            with gr.Row():
                # Left: Input question
                with gr.Column(scale=1):
                    question_rag = gr.Textbox(
                        label="Câu hỏi",
                        placeholder="Ví dụ: Trách nhiệm và quyền hạn của người làm công tác kiểm toán nội bộ là gì?",
                        lines=6
                    )
                    ask_btn = gr.Button("Query")

                # Right: Output (streaming)
                with gr.Column(scale=2):
                    rag_answer = gr.Textbox(
                        label="Kết quả truy vấn",
                        lines=8
                    )
                    rag_sources = gr.Textbox(
                        label="Nguồn tài liệu",
                        # lines = 2
                    )

            # --- Event: Streaming Query ---
            def rag_query_stream_gradio(question: str):
                # get generator from rag_query
                from src.core.rag_store import rag_query
                # chunk_iter = rag_query(question, stream=True)

                # full_text = ""
                for answer, sources in rag_query(question, stream=True):
                    # full_text += answer
                    yield answer, sources

            ask_btn.click(
                fn=rag_query_stream_gradio,
                inputs=[question_rag],
                outputs=[rag_answer, rag_sources],
                show_progress="minimal"
            )

            # gr.Markdown("### 📄 Nạp tài liệu vào")

            # === Upload Section ===
            with gr.Row():
                # with gr.Column(scale=1):
                #     with gr.Accordion("Tải tài liệu", open=False):
                #         upload_file = gr.File(
                #             label="Tải file PDF",
                #             type="filepath"
                #         )
                #         doc_title = gr.Textbox(
                #             label="Tiêu đề tài liệu",
                #             placeholder="VD: Remote Work Policy 2024"
                #         )
                #         doc_desc = gr.Textbox(
                #             label="Mô tả ngắn",
                #             placeholder="Mô tả nhanh nội dung chính của tài liệu",
                #             lines=3
                #         )

                #         load_btn = gr.Button("Load to RAG")
                #         load_status = gr.Markdown()

                with gr.Column(scale=1):
                    rag_docs_list = gr.Markdown(
                        value="_Chưa có tài liệu nào_",
                        label="Tài liệu đã nạp"
                    )

            # # --- Event: Load document ---
            # def load_doc(file_path, title, description):
            #     from src.core.rag_store import (
            #         extract_text_from_pdf_image_based,
            #         add_doc_to_rag_store,
            #         add_catalog_entry
            #     )
            #     if not file_path:
            #         return "No file."

            #     with open(file_path, "rb") as f:
            #         file_bytes = f.read()

            #     file_name = os.path.basename(file_path)
            #     title = (title or "").strip()
            #     description = (description or "").strip()

            #     payload = {
            #         "doc_name": file_name,
            #         "title": title or file_name,
            #         "description": description,
            #     }

            #     text = extract_text_from_pdf_image_based(file_bytes)

            #     add_doc_to_rag_store(text, payload)
            #     add_catalog_entry(payload)

            #     return f"✅ Đã nạp tài liệu vào RAG: **{file_name}**"

            # def show_rag_loading():
            #     return "⏳ Đang nạp tài liệu vào RAG... Vui lòng chờ..."

            def list_docs_markdown():
                from src.core.rag_store import list_rag_docs
                names = list_rag_docs()
                if not names:
                    return "_Chưa có tài liệu trong RAG KB_"
                lines = [f"- {n}" for n in names]
                return "### 📚 Tài liệu đã nạp\n" + "\n".join(lines)

            # load_btn.click(
            #     fn=show_rag_loading,
            #     inputs=None,
            #     outputs=load_status
            # ).then(
            #     fn=load_doc,
            #     inputs=[upload_file, doc_title, doc_desc],
            #     outputs=load_status,
            #     show_progress="minimal"
            # ).then(
            #     fn=list_docs_markdown,
            #     inputs=None,
            #     outputs=rag_docs_list,
            # )
    
    # ---- Pre-load list of docs ----
    app.load(fn=list_docs_markdown, inputs=None, outputs=rag_docs_list)

app.launch(server_name="0.0.0.0")