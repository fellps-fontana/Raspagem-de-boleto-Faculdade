from datetime import datetime
from playwright.sync_api import sync_playwright
from mapeamento.aba_pagamento import TelaPagamento
from credenciais import Senhas



def test_enviar_boleto():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(f'https://estudante.sesisenai.org.br')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        page.get_by_placeholder("Usuário").click()
        page.get_by_placeholder("Usuário").fill(Senhas['user_senai'])
        page.get_by_placeholder("Senha").click()
        page.get_by_placeholder("Senha").fill(Senhas["senhas_senai"])
        page.get_by_role("button", name="Entrar").click()
        if page.get_by_role("button", name="Fechar").is_visible():
            page.get_by_role("button", name="Fechar").click()
        date = datetime.now()
        mes_atual = date.strftime('%m')
        mes_atual_formatado = str(mes_atual)
        tela_pagamento = TelaPagamento(page)
        tela_pagamento.acessar_tela_pagamento(page)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        dowload = tela_pagamento.achar_boleto(mes_atual_formatado)
        email_receptor = Senhas['email_receptor']
        tela_pagamento.enviar_boleto_email(
            email_enviar=email_receptor,
            arquivo_enviar=dowload,
            assunto_email=f"boleto pagamento faculdade mes {mes_atual_formatado}"
        )

# Chame a função aqui
if __name__ == "__main__":
    test_enviar_boleto()
