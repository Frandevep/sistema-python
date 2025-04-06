import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt

# ====================== BASE DE DATOS (SQLite) ======================
def crear_db():
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            completada BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conexion.commit()
    conexion.close()

def agregar_tarea(titulo, descripcion):
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)",
        (titulo, descripcion)
    )
    conexion.commit()
    conexion.close()

def obtener_tareas():
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM tareas")
    tareas = cursor.fetchall()
    conexion.close()
    return tareas

def eliminar_tarea(id):
    conexion = sqlite3.connect("tareas.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()

# ====================== INTERFAZ (PyQt6) ======================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Tareas Avanzado")
        self.resize(800, 600)
        
        # Widgets
        self.titulo_input = QLineEdit(placeholderText="Título de la tarea")
        self.descripcion_input = QLineEdit(placeholderText="Descripción (opcional)")
        self.boton_agregar = QPushButton("➕ Agregar Tarea")
        self.boton_eliminar = QPushButton("❌ Eliminar Selección")
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Título", "Descripción"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.titulo_input)
        layout.addWidget(self.descripcion_input)
        layout.addWidget(self.boton_agregar)
        layout.addWidget(self.boton_eliminar)
        layout.addWidget(self.tabla)
        
        # Contenedor central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Conexiones
        self.boton_agregar.clicked.connect(self.agregar_tarea)
        self.boton_eliminar.clicked.connect(self.eliminar_tarea)
        
        # Estilos CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
                font-family: 'Arial';
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-bottom: 10px;
            }
            QPushButton {
                padding: 8px;
                border-radius: 4px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            #boton_agregar {
                background-color: #4CAF50;
                color: white;
            }
            #boton_eliminar {
                background-color: #f44336;
                color: white;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
            }
        """)
        self.boton_agregar.setObjectName("boton_agregar")
        self.boton_eliminar.setObjectName("boton_eliminar")
        
        # Cargar datos
        self.actualizar_tabla()
    
    def agregar_tarea(self):
        titulo = self.titulo_input.text().strip()
        descripcion = self.descripcion_input.text().strip()
        
        if titulo:
            agregar_tarea(titulo, descripcion)
            self.titulo_input.clear()
            self.descripcion_input.clear()
            self.actualizar_tabla()
        else:
            QMessageBox.warning(self, "Error", "¡El título es obligatorio!")
    
    def eliminar_tarea(self):
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada >= 0:
            id = int(self.tabla.item(fila_seleccionada, 0).text())
            eliminar_tarea(id)
            self.actualizar_tabla()
        else:
            QMessageBox.warning(self, "Error", "Selecciona una tarea para eliminar")
    
    def actualizar_tabla(self):
        tareas = obtener_tareas()
        self.tabla.setRowCount(len(tareas))
        
        for i, tarea in enumerate(tareas):
            id_item = QTableWidgetItem(str(tarea[0]))
            id_item.setFlags(Qt.ItemFlag.NoItemFlags)  # Hacer celda no editable
            
            self.tabla.setItem(i, 0, id_item)
            self.tabla.setItem(i, 1, QTableWidgetItem(tarea[1]))
            self.tabla.setItem(i, 2, QTableWidgetItem(tarea[2]))

# ====================== EJECUCIÓN ======================
if __name__ == "__main__":
    crear_db()  # Crear la base de datos si no existe
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())