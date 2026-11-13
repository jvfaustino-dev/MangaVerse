from PyQt6 import uic, QtWidgets
from cadastro_contas import cadastrar_conta
from login_contas import verificar_conta

def abrir_tela_cadastro():
    login.hide()
    cadastro.show()

def abrir_tela_login():
    cadastro.hide()
    login.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Carrega os arquivos .ui
    cadastro = uic.loadUi("./cadastro_contas.ui")
    login = uic.loadUi("./login_contas.ui")

    # Conexões dos botões de navegação entre as telas
    cadastro.btn_login.clicked.connect(abrir_tela_login)
    login.btn_cadastro.clicked.connect(abrir_tela_cadastro)

    # Conexões das ações dos botões (passando a tela correspondente como parâmetro)
    cadastro.btn_criar.clicked.connect(lambda: cadastrar_conta(cadastro))
    login.btn_entrar.clicked.connect(lambda: verificar_conta(login))

    # Inicia o app mostrando a tela de login
    login.show()
    app.exec()