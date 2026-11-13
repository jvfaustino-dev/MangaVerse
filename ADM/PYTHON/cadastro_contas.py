import mysql.connector
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMessageBox
import os
import recursos_rc
from PyQt6 import QtCore

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



def cadastrar_conta():
    try:
        usuario = str(cadastro.txt_usuario.text())
        email = str(cadastro.txt_email.text())
        senha = str(cadastro.txt_senha.text())

        conn = connect()
        cursor = conn.cursor()
        
        SQL = """ SELECT * FROM contas WHERE USUARIO = %s OR EMAIL = %s LIMIT 1 """

        cursor.execute(SQL, (usuario, email))
        resultado = cursor.fetchone()

        if resultado:
            mensagem = QMessageBox()
            mensagem.setIcon(QMessageBox.Icon.Warning)
            mensagem.setText(str('Cadastro já existente'))
            mensagem.setStandardButtons(QMessageBox.StandardButton.Ok)
            mensagem.exec()
        else:
            SQL_INSERT = f"INSERT INTO contas (USUARIO, EMAIL, SENHA) VALUES ('{usuario}', '{email}', '{senha}')"
            cursor.execute(SQL_INSERT)
            conn.commit()
        
            mensagem = QMessageBox()
            mensagem.setText(f'DADOS ENVIADOS COM SUCESSO!!')
            mensagem.setWindowTitle('CADASTRO DE CONTAS')
            mensagem.setIcon(QMessageBox.Icon.Information)
            mensagem.setStandardButtons(QMessageBox.StandardButton.Ok)
            mensagem.exec()
        
            cadastro.txt_usuario.setText("")
            cadastro.txt_email.setText("")
            cadastro.txt_senha.setText("")
            cadastro.txt_usuario.setFocus()
        
        cursor.close()
        conn.close()
    except:
        mensagem_box = QMessageBox()
        mensagem_box.setIcon(QMessageBox.Icon.Critical)
        mensagem_box.setText(str('ERRO AO GRAVAR!!'))
        mensagem_box.setWindowTitle('CADASTRO DE CONTAS')
        mensagem_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        mensagem_box.exec()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    cadastro = uic.loadUi("./cadastro_contas.ui")

    login = uic.loadUi("./login_contas.ui")

    cadastro.btn_criar.clicked.connect(cadastrar_conta)

    cadastro.show()
    app.exec()
