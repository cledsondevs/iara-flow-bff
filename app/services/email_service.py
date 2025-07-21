
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



