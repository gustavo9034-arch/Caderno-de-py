import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from database import get_connection

def generate_charts():
    conn = get_connection()
    df = pd.read_sql_query("SELECT subject, date FROM activities", conn)
    conn.close()
    
    if df.empty:
        return False
        
    plt.figure(figsize=(6, 5))
    subject_counts = df['subject'].value_counts()
    subject_counts.plot(kind='bar', color=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'])
    plt.title("Atividades por Matéria")
    plt.xlabel("Matéria")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=15, ha='right', fontsize=9)
    plt.tight_layout()
    plt.savefig("charts_bar.png")
    plt.close()

    plt.figure(figsize=(6, 5))
    subject_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'])
    plt.title("Distribuição Percentual")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("charts_pie.png")
    plt.close()
    
    return True