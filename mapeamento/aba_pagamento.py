import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import re
import sys

from credenciais import Senhas


class TelaPagamento:
    def __init__(self, page):
        self.page = page
        self.tabela_boleto = page.locator('#table-boletos')

    def acessar_tela_pagamento(self, page):
        page.goto(f'{page.url}financeiro')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)

    def achar_boleto(self, mes_atual=''):
        total_linhas = self.tabela_boleto.locator('tr').count()
        padrao_data = re.compile(r'\d{1,2}/\d{1,2}/\d{2,4}')
        for i in range(total_linhas):
            elementos_linha = self.tabela_boleto.locator('tr').nth(i).locator('td')
            contar = elementos_linha.count()

            if 'A Vencer' in self.tabela_boleto.locator('tr').nth(i).text_content():
                for a in range(contar):
                    texto = elementos_linha.nth(a).text_content()
                    possiveis_datas = padrao_data.findall(texto)
                    if possiveis_datas:
                        for data in possiveis_datas:
                            mes_data = data.split('/')[1]
                            if mes_data == mes_atual:
                                print(f"Data encontrada no mês atual: {data}")
                                with self.page.expect_download() as download_info:
                                    with self.page.expect_popup() as page1_info:
                                        self.tabela_boleto.locator('tr').nth(i).get_by_role("link").click()
                                        download = download_info.value
                                        download.save_as(
                                            fr'C:\Users\q\Documents\BoletosFaculdade\boleto_mes{mes_atual}.pdf')
                                        return download.path()
                print(f"Envio interrompido, boleto nao encontrado do mes {mes_atual}")
                sys.exit(1)


    def enviar_boleto_email(self, arquivo_enviar, email_enviar, assunto_email):
        message = MIMEMultipart()
        message["From"] = Senhas['usuario']
        message["To"] = email_enviar
        message["Subject"] = assunto_email
        file_name = os.path.basename(arquivo_enviar)

        message.attach(MIMEText('Segue em anexo o boleto.', 'plain'))

        # Anexa o arquivo
        try:
            with open(arquivo_enviar, "rb") as attachment:
                part = MIMEBase("application", "pdf")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={file_name}")
                message.attach(part)
        except Exception as e:
            print("Erro ao anexar o arquivo:", e)
            return


        try:
            with smtplib.SMTP(Senhas['servidor_smtp'], Senhas['porta']) as server:
                server.starttls()
                server.login(Senhas['usuario'], Senhas['senha'])
                server.sendmail(Senhas['usuario'], email_enviar, message.as_string())
            print("E-mail enviado com sucesso!")
        except smtplib.SMTPException as e:
            print("Erro no envio do e-mail:", e)
        except Exception as e:
            print("Erro inesperado:", e)

