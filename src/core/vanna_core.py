import pandas as pd
from dotenv import load_dotenv
import os
from src.database2.database_helpers import DB_CONFIG, get_distinct_values
from src.core.vanna_pre_post_process import preprocess_chain, postprocess_chain
from src.vanna_helpers.init_vanna import get_vanna
import time

load_dotenv(override=True)

def run_vanna_query(question):
    """Execute Vanna query and return results + visualization"""
    try:
        print("Start")
        # Pre-Process the question to get clear and suitable prompt
        company_and_stock_code = get_distinct_values(os.getenv("MINI_BALANCE_SHEET_EOP_WITH_YEAR_START_TABLE_NAME"), ["company_name", "stock_code"])
        company_and_stock_code_str = "\n".join(
            f"{company} — {stock}"
            for company, stock in company_and_stock_code
        )

        prompt = f"""You have access to a database containing balance sheet metrics for the following companies:
{company_and_stock_code_str}
When generating the query:
- Include the relevant numeric values (assets, liabilities, cash, ratios…)
- If the question involves comparisons (>, <, >=, <=), you MUST fetch the numbers for each company and show the values used to decide
- If the answer requires a calculation (growth %, difference, ratio), you MUST compute it and show the computed values
- DO NOT guess missing data
- Only use numbers that exist in the database
- USE language that matched with the question for naming the column
User question:
{question}"""
        print(f"Vanna prompt: {prompt}")

        vn = get_vanna()
        sql = vn.generate_sql(prompt)
        print(sql)
        df = vn.run_sql(sql)
        print(df)
        plot = vn.generate_plotly_code(df)
        print(plot)
        print(type(plot))
        plot_fig = vn.get_plotly_figure(plot, df)
        # sql, df, plot = vn.ask(prompt)

        print("Before post process")

        final_answer = postprocess_chain.invoke({
            "original_question": question
            , "data": df.to_dict()
        }).content
        print("Final answer: ", final_answer)

        return df, plot_fig, final_answer
        
    except Exception as e:
        return f"SQL Error: {str(e)}", pd.DataFrame(), None, "No Answer"