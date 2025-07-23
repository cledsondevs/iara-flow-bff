import os
import smtplib
from email.message import EmailMessage
from typing import Dict, Any, Optional
from flask import request

class EmailSenderService:
    def __init__(self, sender_email: Optional[str] = None, app_password: Optional[str] = None):
        # Usar configurações fornecidas ou padrão do ambiente
        self.sender_email = sender_email or os.getenv("SENDER_EMAIL", "cledsonborgesalves@gmail.com")
        self.app_password = app_password or os.getenv("GMAIL_APP_PASSWORD", "eapbanqlgbrrrims")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465 # Porta para SSL

    @classmethod
    def from_request_headers(cls):
        """Criar instância usando headers da requisição HTTP"""
        sender_email = request.headers.get('X-Email-Gmail')
        app_password = request.headers.get('X-Email-App-Password')
        return cls(sender_email, app_password)

    def send_backlog_report_email(self, recipient_email: str, report_data: Dict[str, Any]):
        """Enviar e-mail com relatório de backlog gerado"""
        if not all([self.sender_email, self.app_password]):
            raise ValueError("Credenciais do Gmail incompletas. Verifique as configurações de e-mail.")

        subject = f"Relatório de Backlog Gerado - {report_data.get('package_name', 'App')}"
        body = self._generate_backlog_email_body(report_data)

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg.set_content(body, subtype='html')

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
                smtp.login(self.sender_email, self.app_password)
                smtp.send_message(msg)
            return {"status": "success", "message": "E-mail de relatório de backlog enviado com sucesso."}
        except Exception as e:
            raise Exception(f"Erro ao enviar e-mail de relatório de backlog: {str(e)}")

    def send_executive_report_email(self, recipient_email: str, report_data: Dict[str, Any]):
        """Enviar e-mail com relatório executivo"""
        if not all([self.sender_email, self.app_password]):
            raise ValueError("Credenciais do Gmail incompletas. Verifique as configurações de e-mail.")

        subject = f"Relatório Executivo - {report_data.get('package_name', 'App')}"
        body = self._generate_executive_email_body(report_data)

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg.set_content(body, subtype='html')

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
                smtp.login(self.sender_email, self.app_password)
                smtp.send_message(msg)
            return {"status": "success", "message": "E-mail de relatório executivo enviado com sucesso."}
        except Exception as e:
            raise Exception(f"Erro ao enviar e-mail de relatório executivo: {str(e)}")

    def _generate_executive_email_body(self, report_data: Dict[str, Any]) -> str:
        """Gerar corpo do e-mail para relatório executivo"""
        package_name = report_data.get("package_name", "Aplicativo Desconhecido")
        negative_reviews_count = report_data.get("negative_reviews_count", 0)
        main_themes = report_data.get("main_themes", [])
        critical_reviews = report_data.get("critical_reviews", [])
        suggestions = report_data.get("suggestions", [])

        themes_text = ", ".join(main_themes[:5]) if main_themes else "Nenhum tema específico identificado"
        suggestions_text = "<br>".join([f"• {suggestion}" for suggestion in suggestions[:5]]) if suggestions else "Nenhuma sugestão específica"

        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #f4f4f4; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .alert-box {{ background-color: #ffebee; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #f44336; }}
                .summary-box {{ background-color: #e8f4fd; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                .suggestions-box {{ background-color: #f3e5f5; padding: 15px; margin: 15px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚨 Relatório Executivo - Reviews Negativos</h1>
                <h2>{package_name}</h2>
            </div>
            
            <div class="content">
                <p>Prezado(a) Gerente,</p>
                <p>Foi detectado um número significativo de reviews negativos para o aplicativo <strong>{package_name}</strong>.</p>

                <div class="alert-box">
                    <h3>⚠️ Alerta de Reviews Negativos</h3>
                    <p><strong>{negative_reviews_count}</strong> reviews negativos foram identificados e requerem atenção imediata.</p>
                </div>

                <div class="summary-box">
                    <h3>📊 Principais Temas Identificados</h3>
                    <p>{themes_text}</p>
                </div>

                <div class="suggestions-box">
                    <h3>💡 Sugestões de Ação</h3>
                    <p>{suggestions_text}</p>
                </div>

                <p>Recomendamos que a equipe de desenvolvimento priorize a resolução destes problemas para melhorar a satisfação dos usuários.</p>
                
                <p>Este relatório foi gerado automaticamente pelo sistema de análise de reviews.</p>
                <p>Para mais informações, entre em contato com a equipe de desenvolvimento.</p>
            </div>
        </body>
        </html>
        """

        return html_body

    def _generate_backlog_email_body(self, report_data: Dict[str, Any]) -> str:
        """Gerar corpo do e-mail para relatório de backlog"""
        # Dados do relatório
        package_name = report_data.get("package_name", "Aplicativo Desconhecido")
        total_items = report_data.get("total_items", 0)
        high_priority_count = report_data.get("high_priority_count", 0)
        analysis_period = report_data.get("analysis_period_days", 7)
        main_themes = report_data.get("main_themes", [])
        high_priority_items = report_data.get("high_priority_items", [])
        items_by_category = report_data.get("items_by_category", {})
        category_summary = report_data.get("category_summary", {})

        # Criar lista de temas principais
        themes_text = ", ".join(main_themes[:5]) if main_themes else "Nenhum tema específico identificado"

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
                        <li><strong>Principais temas identificados:</strong> {themes_text}</li>
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
                priority_class = "priority-high" if item["priority"] == 5 else "priority-medium"
                description_short = item["description"][:100] + ("..." if len(item["description"]) > 100 else "")
                html_body += f"""
                        <tr>
                            <td><strong>{item["title"]}</strong></td>
                            <td>{item["category"].title()}</td>
                            <td class="{priority_class}">{item["priority"]}</td>
                            <td>{item["frequency"]}</td>
                            <td>{description_short}</td>
                        </tr>
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
                            <td>{data["count"]}</td>
                            <td>{data["avg_priority"]:.1f}</td>
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
                    priority_text = "🔴" if item["priority"] >= 4 else "🟡" if item["priority"] == 3 else "🟢"
                    description_short = item["description"][:150] + ("..." if len(item["description"]) > 150 else "")
                    html_body += f"""
                            <li>
                                <strong>{priority_text} {item["title"]}</strong><br>
                                <small>{description_short}</small>
                            </li>
                    """
                
                if len(items) > 5:
                    html_body += f"<li><em>... e mais {len(items) - 5} itens</em></li>"
                
                html_body += """
                        </ul>
                    </div>
                """

        html_body += """
                <p>Este relatório foi gerado automaticamente pelo sistema de análise de reviews.</p>
                <p>Para mais informações, entre em contato com a equipe de desenvolvimento.</p>
            </div>
        </body>
        </html>
        """

        return html_body

