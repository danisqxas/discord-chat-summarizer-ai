# Discord Chat Summarizer AI

> Un resumidor de conversaciones de Discord robusto y autocontenido.

Este proyecto ofrece una solución completa para procesar historiales de chat y
obtener un resumen conciso sin depender de servicios externos.  Está diseñado
para ser transparente, extensible y fácil de desplegar en distintos entornos,
desde aplicaciones locales y bots hasta funciones sin servidor.

## Visión general

El objetivo del **Discord Chat Summarizer AI** es convertir grandes volúmenes
de mensajes en resúmenes manejables.  Utiliza un algoritmo extractivo
basado en frecuencia que selecciona las frases más relevantes de la
conversación, ignorando palabras vacías comunes en inglés y español.  El
sistema almacena de forma opcional el historial de conversaciones en disco y
ofrece varias capas de abstracción para integrarse con interfaces de usuario,
bots de Discord o API HTTP.

### Arquitectura

La aplicación está organizada en los siguientes módulos principales:

| Módulo                        | Propósito |
|------------------------------|-----------|
| `src/helpers/utils.py`       | Implementa el algoritmo de **resumen extractivo** y funciones de utilidad como limpieza de tokens y separación en frases. |
| `src/core/history_manager.py`| Gestiona la persistencia de mensajes en un archivo JSON con límites configurables de memoria. |
| `src/services/api_service.py`| Expone funciones asincrónicas para resumir mensajes y comprobar la salud del servicio. |
| `src/controllers/summarizer_controller.py` | Orquesta la interacción entre el gestor de historial y el servicio de API para generar resúmenes y devolverlos a las capas superiores. |
| `src/commands/bot_commands.py`| Define comandos para un bot de Discord que permiten resumir el historial, consultar su estado o restablecerlo. |
| `src/ui.py`                  | Proporciona una interfaz gráfica sencilla usando **Tkinter** para introducir texto y visualizar el resumen. |
| `api/index.py`               | Punto de entrada compatible con plataformas _serverless_ que ofrece un endpoint HTTP para resumir mensajes y un *health check*. |

Además, el repositorio incluye scripts de configuración (`src/config/config_manager.py`), modelos de datos (`src/models`) y pruebas automatizadas en el directorio `tests`.

## Instalación

Para ejecutar el proyecto localmente se recomienda utilizar Python 3.9 o superior.

1. **Clonar el repositorio** y entrar en su directorio:

   ```bash
   git clone https://github.com/danisqxas/discord-chat-summarizer-ai.git
   cd discord-chat-summarizer-ai
   ```

2. **Crear y activar un entorno virtual** (opcional pero recomendado):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Como biblioteca

Puedes importar la función `summarize_messages` desde `src.helpers.utils` en
tu propio código para generar resúmenes a partir de una lista de cadenas:

```python
from src.helpers.utils import summarize_messages

mensajes = [
    "Hoy hemos discutido la arquitectura del proyecto.",
    "Se ha diseñado un algoritmo de resumen extractivo.",
    "Es importante evitar dependencias externas y mantener el código limpio."
]

resumen = summarize_messages(mensajes)
print(resumen)
```

### Ejecutar la interfaz gráfica

El archivo `src/ui.py` lanza una ventana GUI donde se puede pegar el texto a
resumir y obtener el resultado.  Ejecuta lo siguiente desde la raíz del
proyecto:

```bash
python -m src.ui
```

### Punto de entrada *serverless*

Si deseas desplegar el servicio como una función sin servidor, el archivo
`api/index.py` expone una función `handler` compatible con Vercel, AWS
Lambda y otros proveedores.  La función acepta peticiones **POST** con
cuerpo JSON que contenga un arreglo `messages` y responde con un objeto
`summary`.

Ejemplo de solicitud con `curl`:

```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"messages": ["Este es el primer mensaje.", "Aquí va el segundo."]}' \
     http://localhost:8000
```

El handler también responde a **GET** con un mensaje de estado para verificar
que el servicio está activo.

### Integración con bots de Discord

El módulo `src/commands/bot_commands.py` contiene comandos asincrónicos
listos para ser conectados a un bot de Discord.  Los comandos disponibles son

- `summarize` – Genera un resumen del historial y lo envía al canal.
- `summarize reset` – Limpia el historial guardado.
- `summarize status` – Informa cuántas entradas hay en el historial.
- `summarize logs` – Devuelve tanto el resumen como el registro completo.

Ejemplos de uso se encuentran dentro del módulo como comentarios.

## Configuración y ajustes

El archivo `src/config/config_manager.py` gestiona los parámetros de
configuración persistentes en un archivo `config.json`.  Puedes ajustar,
por ejemplo, el modelo predeterminado (aunque no se usa un modelo externo
por defecto) o el límite de memoria del historial.  Para modificar
cualquier parámetro, utiliza las funciones `update_config_data` y
`get_config_data`.

## Pruebas automatizadas

Se incluyen pruebas sencillas bajo el directorio `tests` para comprobar
funcionalidades clave como la generación de resúmenes, la salud del API y
utilidades auxiliares.  Ejecuta las pruebas con:

```bash
pytest -q
```

## Contribuciones

Se agradecen aportaciones de la comunidad.  Si deseas proponer mejoras o
corregir errores, abre una *issue* o envía un *pull request*.  Asegúrate de
que las nuevas funciones incluyan pruebas y documentación adecuadas.

## Licencia

Este proyecto se publica bajo una licencia permisiva y se proporciona
**tal cual** para fines educativos.  Consulta el archivo `LICENSE` para más
detalles.