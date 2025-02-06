@echo off
call C:\Users\q\PycharmProjects\enviar_boleto_faculdade\.venv\Scripts\activate.bat

if errorlevel 1 (
    echo Erro ao ativar o ambiente virtual. Certifique-se de que o caminho está correto.
    pause
    exit /b 1
)

set PYTHONPATH=C:\Users\q\PycharmProjects\enviar_boleto_faculdade


python C:\Users\q\PycharmProjects\enviar_boleto_faculdade\mapeamento\aba_pagamento.py
if errorlevel 1 (
    echo Erro no aba_pagamento.py.
    pause
    exit /b 1
)

python C:\Users\q\PycharmProjects\enviar_boleto_faculdade\teste\enviar_boleto.py
if errorlevel 1 (
    echo O script encontrou um erro durante a execução.
    pause
    exit /b 1
)

echo Script executado com sucesso!
pause
