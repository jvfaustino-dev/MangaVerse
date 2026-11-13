import mysql.connector
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMessageBox
import os
import recursos_rc
from PyQt6 import QtCore

'''EXECUTAR TERMINAL
& "C:/Users/Etec de Sapopemba/AppData/Local/Programs/Python/Python312/python.exe" -m pip install PySide6

& "C:/Users/Etec de Sapopemba/AppData/Local/Programs/Python/Python312/Scripts/pyside6-rcc.exe" recursos.qrc -o recursos_rc.py

(Get-Content .\recursos_rc.py -Raw).Replace('from PySide6 import QtCore', 'from PyQt6 import QtCore') | Set-Content .\recursos_rc.py -Encoding utf8'''

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def connect():
    conn = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        port='3306',
        database='db_contas'
    )
    return conn



def abrir_tela_login():
    global abrir_login
    cadastro.close()
    abrir_login = uic.loadUi("./login_contas.ui")
    abrir_login.show()


# ALTERADO: agora recebe a tela de login como parâmetro
def verificar_conta(tela_login):
    try:
        # ALTERADO: utiliza tela_login em vez de login
        usuario_email = str(tela_login.txt_usuario_email.text())
        senha = str(tela_login.txt_senha.text())

        conn = connect()
        cursor = conn.cursor()

        SQL = """ SELECT 1 FROM contas WHERE (USUARIO = %s OR EMAIL = %s) AND SENHA = %s LIMIT 1 """
        
        cursor.execute(SQL, (usuario_email, usuario_email, senha))
        resultado = cursor.fetchone()

        if resultado:
            
            mensagem = QMessageBox()
            mensagem.setIcon(QMessageBox.Icon.Information)
            mensagem.setText(str('Conta Logada'))
            mensagem.setStandardButtons(QMessageBox.StandardButton.Ok)
            mensagem.exec()

            # ALTERADO: utiliza tela_login
            tela_login.txt_usuario_email.setText("")
            tela_login.txt_senha.setText("")
            tela_login.txt_usuario_email.setFocus()

        else:

            mensagem = QMessageBox()
            mensagem.setIcon(QMessageBox.Icon.Warning)
            mensagem.setText(str('Login Incorreto'))
            mensagem.setStandardButtons(QMessageBox.StandardButton.Ok)
            mensagem.exec()

    except Exception as erro:
        mensagem_box = QMessageBox()
        mensagem_box.setIcon(QMessageBox.Icon.Critical)
        mensagem_box.setWindowTitle('ERRO NO LOGIN')
        mensagem_box.setText(f'Ocorreu um erro: {erro}')
        mensagem_box.setStandardButtons(
            QMessageBox.StandardButton.Ok
        )
        mensagem_box.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    cadastro = uic.loadUi("./cadastro_contas.ui")
    login = uic.loadUi("./login_contas.ui")

    # ALTERADO: passa a tela de login como argumento
    login.btn_entrar.clicked.connect(lambda: verificar_conta(login))

    login.show()
    app.exec()