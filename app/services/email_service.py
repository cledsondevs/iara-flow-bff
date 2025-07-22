
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any

class EmailSenderService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.sender_email = os.getenv("SENDER_EMAIL")

    def send_backlog_report_email(self, recipient_email: str, report_data: Dict[str, Any]):
        """Enviar e-mail com relatório de backlog gerado"""
        if not all([self.smtp_server, self.smtp_username, self.smtp_password, self.sender_email]):
            raise ValueError("Configurações de SMTP incompletas. Verifique as variáveis de ambiente.")

        subject = f"Relatório de Backlog Gerado - {report_data.get('package_name', 'App')}"
        body = self._generate_backlog_email_body(report_data)

        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            return {"status": "success", "message": "E-mail de relatório de backlog enviado com sucesso."}
        except Exception as e:
            raise Exception(f"Erro ao enviar e-mail de relatório de backlog: {str(e)}")

    def _generate_backlog_email_body(self, report_data: Dict[str, Any]) -> str:
        """Gerar corpo do e-mail para relatório de backlog"""
        # Dados do relatório
        package_name = report_data.get('package_name', 'Aplicativo Desconhecido')
        total_items = report_data.get('total_items', 0)
        high_priority_count = report_data.get('high_priority_count', 0)
        analysis_period = report_data.get('analysis_period_days', 7)
        main_themes = report_data.get('main_themes', [])
        high_priority_items = report_data.get('high_priority_items', [])
        items_by_category = report_data.get('items_by_category', {})
        category_summary = report_data.get('category_summary', {})

        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #f4f4f4; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .summary-box {{ background-color: #e8f4fd; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                .priority-high {{ color: #d32f2f; font-weight: bold; }}
                .priority-medium {{ color: #f57c00; font-weight: bold; }}
                .priority-low {{ color: #388e3c; font-weight: bold; }}
                .category {{ margin: 15px 0; padding: 10px; border-left: 4px solid #2196f3; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Relatório de Backlog Gerado</h1>
                <h2>{package_name}</h2>
            </div>
            
            <div class="content">
                <p>Prezado(a) Gerente,</p>
                <p>Foi gerado um novo backlog baseado na análise de reviews dos últimos <strong>{analysis_period} dias</strong> para o aplicativo <strong>{package_name}</strong>.</p>

                <div class="summary-box">
                    <h3>📊 Resumo Executivo</h3>
                    <ul>
                        <li><strong>Total de itens gerados:</strong> {total_items}</li>
                        <li><strong>Itens de alta prioridade:</strong> {high_priority_count}</li>
                        <li><strong>Período de análise:</strong> {analysis_period} dias</li>
                        <li><strong>Principais temas identificados:</strong> {', '.join(main_themes[:5]) if main_themes else 'Nenhum tema específico identificado'}</li>
                    </ul>
                </div>

                <h3>🔥 Itens de Alta Prioridade (Prioridade ≥ 4)</h3>
        """

        if high_priority_items:
            html_body += """
                <table>
                    <thead>
                        <tr>
                            <th>Título</th>
                            <th>Categoria</th>
                            <th>Prioridade</th>
                            <th>Frequência</th>
                            <th>Descrição</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for item in high_priority_items:
                priority_class = "priority-high" if item['priority'] == 5 else "priority-medium"
                html_body += f"""
                        <tr>
                            <td><strong>{item['title']}</strong></td>
                            <td>{item['category'].title()}</td>
                            <td class="{priority_class}">{item['priority']}</td>
                            <td>{item['frequency']}</td>
                            <td>{item['description'][:100]}{'...' if len(item['description']) > 100 else ''}</td>                     </tr>
                """
            
            html_body += """
                    </tbody>
                </table>
            """
        else:
            html_body += "<p>Nenhum item de alta prioridade identificado neste período.</p>"

        # Resumo por categoria
        html_body += "<h3>📋 Resumo por Categoria</h3>"
        
        if category_summary:
            html_body += """
                <table>
                    <thead>
                        <tr>
                            <th>Categoria</th>
                            <th>Quantidade</th>
                            <th>Prioridade Média</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for category, data in category_summary.items():
                html_body += f"""
                        <tr>
                            <td>{category.title()}</td>
                            <td>{data['count']}</td>
                            <td>{data['avg_priority']:.1f}</td>
                        </tr>
                """
            
            html_body += """
                    </tbody>
                </table>
            """

        # Detalhes por categoria
        if items_by_category:
            html_body += "<h3>📝 Detalhes por Categoria</h3>"
            
            for category, items in items_by_category.items():
                html_body += f"""
                    <div class="category">
                        <h4>{category.title()} ({len(items)} itens)</h4>
                        <ul>
                """
                
                for item in items[:5]:  # Mostrar apenas os 5 primeiros de cada categoria
                    priority_text = "🔴" if item['priority'] >= 4 else "🟡" if item['priority'] == 3 else "🟢"
                    html_body += f"""
                            <li>
                                <strong>{priority_text} {item["title"]}</strong><br>
                                <small>{item["description"][:150]}{"...".format() if len(item["description"]) > 150 else ""}</small>
                            </li>
                    """
                
                if len(items) > 5:
                    html_body += f"<li><em>... e mais {len(items) - 5} itens</em></li>"