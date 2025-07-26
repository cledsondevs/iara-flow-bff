import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

email_bp = Blueprint('email', __name__)

@email_bp.route('/send-email', methods=['POST'])
@cross_origin()
def send_email():
    """
    Endpoint para envio de e-mail via Gmail
    
    Parâmetros esperados no JSON:
    - recipient: e-mail do destinatário
    - subject: assunto do e-mail
    - content: conteúdo do e-mail
    """
    try:
        # Obter dados do request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        recipient = data.get('recipient')
        subject = data.get('subject')
        content = data.get('content')
        
        # Validar campos obrigatórios
        if not recipient:
            return jsonify({'error': 'Campo recipient é obrigatório'}), 400
        
        if not subject:
            return jsonify({'error': 'Campo subject é obrigatório'}), 400
            
        if not content:
            return jsonify({'error': 'Campo content é obrigatório'}), 400
        
        # Configurações do Gmail
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "cledsonborgesalves@gmail.com"
        sender_password = "eapb anql gbrr rims"
        
        # Criar mensagem
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient
        message["Subject"] = subject
        
        # Adicionar conteúdo ao e-mail
        message.attach(MIMEText(content, "plain", "utf-8"))
        
        # Conectar ao servidor SMTP e enviar e-mail
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Habilitar criptografia
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, recipient, text)
        
        return jsonify({
            'success': True,
            'message': f'E-mail enviado com sucesso para {recipient}',
            'data': {
                'recipient': recipient,
                'subject': subject,
                'sender': sender_email
            }
        }), 200
        
    except smtplib.SMTPAuthenticationError:
        return jsonify({
            'error': 'Erro de autenticação SMTP. Verifique as credenciais.',
            'success': False
        }), 401
        
    except smtplib.SMTPRecipientsRefused:
        return jsonify({
            'error': 'Destinatário recusado. Verifique o e-mail do destinatário.',
            'success': False
        }), 400
        
    except smtplib.SMTPException as e:
        return jsonify({
            'error': f'Erro SMTP: {str(e)}',
            'success': False
        }), 500
        
    except Exception as e:
        return jsonify({
            'error': f'Erro interno do servidor: {str(e)}',
            'success': False
        }), 500

@email_bp.route('/email-config', methods=['GET'])
@cross_origin()
def get_email_config():
    """
    Endpoint para obter configurações de e-mail (sem expor senha)
    """
    return jsonify({
        'sender_email': 'cledsonborgesalves@gmail.com',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'encryption': 'TLS'
    }), 200

