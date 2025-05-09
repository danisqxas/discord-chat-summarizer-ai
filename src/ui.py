"""
Este módulo maneja la configuración de la interfaz de usuario del bot.
Incluye funciones relacionadas con la configuración visual y la interacción del bot.
"""

import tkinter as tk
from tkinter import messagebox


class ChatSummarizerUI:
    """
    Clase que representa la interfaz de usuario del bot de resumen de chats.
    """

    def __init__(self):
        """
        Inicializa la ventana principal de la interfaz de usuario.
        """
        self.root = tk.Tk()
        self.root.title("Discord Chat Summarizer AI")
        self.root.geometry("500x400")

        self._setup_widgets()

    def _setup_widgets(self):
        """
        Configura los widgets de la interfaz de usuario.
        """
        # Etiqueta de título
        title_label = tk.Label(
            self.root, text="Discord Chat Summarizer AI", font=("Arial", 16)
        )
        title_label.pack(pady=10)

        # Campo de entrada para el texto del chat
        self.chat_input = tk.Text(self.root, height=10, width=50)
        self.chat_input.pack(pady=10)

        # Botón para resumir el chat
        summarize_button = tk.Button(
            self.root, text="Resumir Chat", command=self.summarize_chat
        )
        summarize_button.pack(pady=5)

        # Área de texto para mostrar el resumen
        self.summary_output = tk.Text(self.root, height=10, width=50, state="disabled")
        self.summary_output.pack(pady=10)

    def summarize_chat(self):
        """
        Llama a la función de resumen de chat y muestra el resultado en la interfaz.
        """
        chat_text = self.chat_input.get("1.0", tk.END).strip()
        if not chat_text:
            messagebox.showwarning(
                "Advertencia", "Por favor, ingrese texto para resumir."
            )
            return

        # Aquí se llamaría a la lógica de resumen (por ejemplo, una función en otro módulo)
        summary = self._mock_summarize(chat_text)

        # Muestra el resumen en el área de salida
        self.summary_output.config(state="normal")
        self.summary_output.delete("1.0", tk.END)
        self.summary_output.insert(tk.END, summary)
        self.summary_output.config(state="disabled")

    def _mock_summarize(self, text):
        """
        Función de ejemplo para simular el resumen de texto.
        En una implementación real, esta función llamaría a la lógica de resumen.
        """
        return f"Resumen simulado: {text[:100]}..."  # Devuelve los primeros 100 caracteres como ejemplo

    def run(self):
        """
        Inicia el bucle principal de la interfaz de usuario.
        """
        self.root.mainloop()


# Ejemplo de uso
if __name__ == "__main__":
    ui = ChatSummarizerUI()
    ui.run()
