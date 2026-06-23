import sqlite3
import pandas as pd
from database import get_connection

def get_report_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM activities")
    total_activities = cursor.fetchone()[0]
    
    cursor.execute("SELECT subject, COUNT(subject) FROM activities GROUP BY subject ORDER BY COUNT(subject) DESC LIMIT 1")
    row = cursor.fetchone()
    most_popular_subject = row[0] if row else "Nenhuma"
    
    cursor.execute("SELECT accesses, records FROM statistics WHERE id = 1")
    stats = cursor.fetchone()
    system_logins = stats[0] if stats else 0
    
    conn.close()
    
    report_text = f"""
========================================
       RELATÓRIO DO CADERNO DIGITAL     
========================================
Total de Usuários:        {total_users}
Total de Atividades:      {total_activities}
Matéria Mais Estudada:    {most_popular_subject}
Total de Logins no App:   {system_logins}
========================================
Relatório gerado com sucesso.
"""
    return report_text