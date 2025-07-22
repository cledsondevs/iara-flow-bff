
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
                            <td>{item['description'][:100]{'...' if len(item['description']) > 100 else ''}}</td>
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
                                <strong>{priority_text} {item['title']}</strong><br>
                                <small>{item['description'][:150]{'...' if len(item['description']) > 150 else ''}}</small>
                            </li>
                    """
                
                if len(items) > 5:
                    html_body += f"<li><em>... e mais {len(items) - 5} itens</em></li>"
                
                html_body += """
                        </ul>
                    </div>
                """

        html_body += f"""
                <div class="summary-box">
                    <h3>💡 Próximos Passos Recomendados</h3>
                    <ol>
                        <li>Revisar e priorizar os itens de alta prioridade listados acima</li>
                        <li>Alocar recursos para resolver os problemas mais críticos (prioridade 5)</li>
                        <li>Considerar implementar as melhorias sugeridas pelos usuários</li>
                        <li>Monitorar continuamente os reviews para identificar novos padrões</li>
                        <li>Acompanhar o progresso dos itens implementados</li>
                    </ol>
                </div>

                <p>Este relatório foi gerado automaticamente baseado na análise de reviews negativos e sugestões dos usuários.</p>
                <p>Para mais detalhes, acesse o sistema de gestão de backlog.</p>

                <p>Atenciosamente,</p>
                <p><strong>Sistema Iara Flow - Análise Inteligente de Reviews</strong></p>
            </div>
        </body>
        </html>
        """
        return html_body

    def send_executive_report_email(self, recipient_email: str, report_data: Dict[str, Any]):
        if not all([self.smtp_server, self.smtp_username, self.smtp_password, self.sender_email]):
            raise ValueError("Configurações de SMTP incompletas. Verifique as variáveis de ambiente.")

        subject = f"Relatório Executivo de Reviews Negativos - {report_data.get('package_name', 'App')}"
        body = self._generate_email_body(report_data)

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            return {"status": "success", "message": "E-mail de relatório enviado com sucesso."}
        except Exception as e:
            raise Exception(f"Erro ao enviar e-mail de relatório: {str(e)}")

    def _generate_email_body(self, report_data: Dict[str, Any]) -> str:
        # Dados do relatório
        package_name = report_data.get('package_name', 'Aplicativo Desconhecido')
        negative_reviews_count = report_data.get('negative_reviews_count', 0)
        main_themes = report_data.get('main_themes', [])
        critical_reviews = report_data.get('critical_reviews', [])
        suggestions = report_data.get('suggestions', [])

        html_body = f"""
        <html>
        <head></head>
        <body>
            <h1>Relatório Executivo de Reviews Negativos - {package_name}</h1>
            <p>Prezado(a) Gerente,</p>
            <p>Este relatório apresenta um resumo dos reviews negativos processados para o aplicativo <strong>{package_name}</strong>.</p>

            <h2>Resumo Geral</h2>
            <p>Total de reviews negativos processados: <strong>{negative_reviews_count}</strong></p>
            <p>Principais temas/palavras-chave identificados nos reviews negativos: <strong>{', '.join(main_themes) if main_themes else 'Nenhum tema principal identificado.'}</strong></p>

            <h2>Detalhes dos Reviews Mais Críticos</h2>
        """

        if critical_reviews:
            for review in critical_reviews:
                html_body += f"""
                <h3>Review ID: {review.get('review_id', 'N/A')}</h3>
                <p><strong>Usuário:</strong> {review.get('user_name', 'Anônimo')}</p>
                <p><strong>Conteúdo:</strong> {review.get('content', 'N/A')}</p>
                <p><strong>Rating:</strong> {review.get('rating', 'N/A')}</p>
                <p><strong>Tópicos:</strong> {', '.join(review.get('topics', [])) if review.get('topics') else 'N/A'}</p>
                <p><strong>Sentimento:</strong> {review.get('sentiment', 'N/A')}</p>
                <hr>
                """
        else:
            html_body += "<p>Nenhum review crítico detalhado neste relatório.</p>"

        html_body += f"""
            <h2>Sugestões de Ações</h2>
        """
        if suggestions:
            html_body += "<ul>"
            for suggestion in suggestions:
                html_body += f"<li>{suggestion}</li>"
            html_body += "</ul>"
        else:
            html_body += "<p>Nenhuma sugestão de ação específica gerada neste relatório.</p>"

        html_body += f"""
            <p>Atenciosamente,</p>
            <p>Sua Equipe de Análise de Reviews</p>
        </body>
        </html>
        """
        return html_body

    def get_email_config_requirements(self) -> Dict[str, str]:
        return {
            "SMTP_SERVER": "Endereço do servidor SMTP (ex: smtp.sendgrid.net, smtp.mailgun.org)",
            "SMTP_PORT": "Porta do servidor SMTP (ex: 587 para TLS, 465 para SSL)",
            "SMTP_USERNAME": "Nome de usuário para autenticação SMTP (geralmente a API Key ou usuário do serviço)",
            "SMTP_PASSWORD": "Senha para autenticação SMTP (geralmente a API Key ou senha do serviço)",
            "SENDER_EMAIL": "Endereço de e-mail do remetente (deve ser verificado no serviço de e-mail)"
        }



