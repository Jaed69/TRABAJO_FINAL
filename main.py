import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

# Crear una clase para la ventana principal
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle('Mi Primera Aplicación en PyQt5')
        self.setGeometry(100, 100, 400, 300)

        # Crear un layout y un label
        layout = QVBoxLayout()
        label = QLabel('¡Hola, mundo!', self)

        # Agregar el label al layout
        layout.addWidget(label)

        # Configurar el layout en la ventana principal
        self.setLayout(layout)

# Configuración principal del aplicativo
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
