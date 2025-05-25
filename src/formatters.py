import pandas as pd
import plotly.express as px
from typing import Union

def format_result(sql_result, sql, normalized_question, final_answer):
    """
    Formats query results into either a styled card (for single values) 
    or Plotly figure (for tables)
    
    Args:
        df: Pandas DataFrame with query results
        sql: Generated SQL string
        
    Returns:
        tuple: (sql, df, visualization)
    """
    if df.shape == (1, 1):  # Single cell result
        value = df.iloc[0, 0]
        html_card = f"""
        <div style='
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        '>
            <div style='font-size: 16px; margin-bottom: 10px;'>Result</div>
            {value}
        </div>
        """
        return sql, df, html_card
    
    # Try to return bar
    elif len(df.columns) == 2 and not df.empty:  # Two columns -> Bar Chart
        fig = px.bar(df, x=df.columns[0], y=df.columns[1])
        return sql, df, fig
    
    # Anything else -> Table
    else:
        styled_df = df.style.set_properties(**{
            'background-color': '#f9f9f9',
            'border': '1px solid #ccc',
            'text-align': 'center',
            'padding': '8px'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#f2f2f2'), ('color', 'black')]}
        ])
        return sql, df, styled_df  # or use HTML(styled_df.render()) for full HTML output