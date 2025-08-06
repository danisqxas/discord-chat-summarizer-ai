"""Sencilla interfaz gráfica para resumir conversaciones.

La interfaz usa :func:`~chat_summarizer.summarizer.summarize_text` para producir
un resumen extractivo de los mensajes escritos por el usuario.  Está
pensada como una utilidad de demostración; en un entorno de producción
se integraría con un bot de Discord u otras plataformas.
"""

import tkinter as tk
from tkinter import messagebox

from .summarizer import summarize_text


class ChatSummarizerUI:
    """Clase que representa la interfaz de usuario del bot de resumen de chats."""

    def __init__(self) -> None:
        """Inicializa la ventana principal de la interfaz de usuario."""
        self.root = tk.Tk()
        self.root.title("Discord Chat Summarizer AI")
        self.root.geometry("500x400")

        self._setup_widgets()

    def _setup_widgets(self) -> None:
        """Configura los widgets de la interfaz de usuario."""
        title_label = tk.Label(
            self.root, text="Discord Chat Summarizer AI", font=("Arial", 16)
        )
        title_label.pack(pady=10)

        self.chat_input = tk.Text(self.root, height=10, width=50)
        self.chat_input.pack(pady=10)

        summarize_button = tk.Button(
            self.root, text="Resumir Chat", command=self.summarize_chat
        )
        summarize_button.pack(pady=5)

        self.summary_output = tk.Text(self.root, height=10, width=50, state="disabled")
        self.summary_output.pack(pady=10)

    def summarize_chat(self) -> None:
        """Llama a la función de resumen de chat y muestra el resultado."""
        chat_text = self.chat_input.get("1.0", tk.END).strip()
        if not chat_text:
            messagebox.showwarning(
                "Advertencia", "Por favor, ingrese texto para resumir."
            )
            return

        summary = summarize_text(chat_text)
        self.summary_output.config(state="normal")
        self.summary_output.delete("1.0", tk.END)
        self.summary_output.insert(tk.END, summary)
        self.summary_output.config(state="disabled")

    def run(self) -> None:
        """Inicia el bucle principal de la interfaz de usuario."""
        self.root.mainloop()


if __name__ == "__main__":
    ChatSummarizerUI().run()
