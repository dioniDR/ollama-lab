# Ollama Lab 🤖

Una interfaz web moderna y completa para interactuar con modelos de Ollama, con gestión avanzada de prompts y controles de chat mejorados.

## 🌟 Características

### 💬 Chat Interactivo
- **Interfaz web moderna** con diseño oscuro
- **Streaming en tiempo real** de respuestas
- **Detener respuesta** en cualquier momento
- **Limpiar chat** para reiniciar el contexto
- **Múltiples modelos** disponibles

### 🎯 Gestión de Prompts
- **Guardar prompts** del sistema con nombres y descripciones
- **IDs únicos** para cada prompt
- **Navegación fácil** entre prompts guardados
- **Aplicar prompts** con un solo clic
- **Eliminar prompts** no deseados
- **Metadatos** con fechas de creación y último uso

### ⚙️ Configuración Avanzada
- **Temperatura** (0.0 - 2.0)
- **Top P** (0.0 - 1.0)
- **Contexto** personalizable
- **Penalización de repetición**
- **Cambio de modelo** en tiempo real

### 🎛️ Controles de Chat
- **Botón de parar** para detener respuestas
- **Botón de limpiar** para reiniciar conversaciones
- **Prevención de múltiples requests** simultáneos
- **Indicadores visuales** del estado actual

## 🚀 Instalación

### Prerrequisitos
- Python 3.8+
- [Ollama](https://ollama.ai/) instalado y ejecutándose

### Configuración

1. **Clona el repositorio:**
```bash
git clone https://github.com/dioniDR/ollama-lab.git
cd ollama-lab
```

2. **Crea un entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

4. **Asegúrate de que Ollama esté ejecutándose:**
```bash
# En otra terminal
ollama serve
```

5. **Ejecuta la aplicación:**
```bash
python run.py
```

6. **Abre tu navegador** en `http://localhost:8000`

## 📋 Uso

### Configuración Inicial
1. Haz clic en **"Configuración"** para ajustar parámetros del modelo
2. Selecciona tu modelo preferido desde el selector
3. Configura el prompt del sistema según tus necesidades

### Gestión de Prompts
1. Haz clic en **"Prompts"** para abrir el gestor
2. **Crear nuevo prompt:**
   - Ingresa nombre y descripción
   - Escribe el prompt del sistema
   - Haz clic en "Guardar Prompt"
3. **Usar prompt guardado:**
   - Selecciona de la lista de prompts guardados
   - Haz clic en "Usar"
4. **Eliminar prompt:**
   - Haz clic en "Eliminar" junto al prompt deseado

### Controles de Chat
- **Enviar mensaje:** Escribe y presiona Enter o haz clic en "Enviar"
- **Detener respuesta:** Haz clic en "Detener" (botón rojo) mientras se genera
- **Limpiar chat:** Haz clic en "Limpiar Chat" para reiniciar la conversación

## 🔧 API Endpoints

### Chat
- `POST /chat` - Enviar mensaje al modelo
- `GET /models` - Listar modelos disponibles
- `POST /switch-model` - Cambiar modelo activo

### Configuración
- `GET /config` - Obtener configuración actual
- `POST /config` - Actualizar configuración

### Prompts
- `GET /prompts` - Listar todos los prompts guardados
- `POST /prompts` - Guardar nuevo prompt
- `POST /prompts/use` - Aplicar prompt específico
- `GET /prompts/{id}` - Obtener prompt específico
- `DELETE /prompts/{id}` - Eliminar prompt

## 📁 Estructura del Proyecto

```
ollama-lab/
├── main.py              # Aplicación FastAPI principal
├── run.py               # Script de ejecución
├── requirements.txt     # Dependencias Python
├── config.json          # Configuración del modelo
├── saved_prompts.json   # Prompts guardados
├── static/
│   └── index.html       # Interfaz web
└── venv/               # Entorno virtual
```

## 🛠️ Tecnologías

- **Backend:** FastAPI, Python 3.8+
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **API:** Ollama REST API
- **Streaming:** Server-Sent Events
- **Persistencia:** JSON files

## 🎯 Características Técnicas

### Backend
- **Streaming asíncrono** con FastAPI
- **Proxy transparente** hacia Ollama
- **Gestión de configuración** persistente
- **Sistema de prompts** con UUIDs únicos
- **Manejo robusto de errores**

### Frontend
- **Interfaz responsiva** con CSS Grid/Flexbox
- **Streaming en tiempo real** con Fetch API
- **Gestión de estado** con JavaScript
- **Controles de cancelación** con AbortController
- **Modales y formularios** dinámicos

## 🔄 Flujo de Trabajo

1. **Configuración inicial** del modelo y prompts
2. **Inicio de conversación** con prompt del sistema
3. **Intercambio de mensajes** con streaming
4. **Control de respuestas** (detener/continuar)
5. **Gestión de contexto** (limpiar/reiniciar)

## 📝 Configuración por Defecto

```json
{
  "model": "llama3.2",
  "temperature": 0.7,
  "top_p": 0.9,
  "system_prompt": "You are a helpful assistant.",
  "max_tokens": 4096,
  "stream": true,
  "num_ctx": 2048,
  "repeat_penalty": 1.1
}
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🐛 Reporte de Bugs

Si encuentras algún bug, por favor abre un [issue](https://github.com/dioniDR/ollama-lab/issues) con:
- Descripción del problema
- Pasos para reproducir
- Comportamiento esperado
- Screenshots (si aplica)

## 🚧 Roadmap

- [ ] Historial de conversaciones
- [ ] Exportar conversaciones
- [ ] Temas personalizables
- [ ] Soporte para imágenes
- [ ] Integración con más modelos
- [ ] API REST completa

## 👤 Autor

**Dioni DR**
- GitHub: [@dioniDR](https://github.com/dioniDR)

---

⭐ **¡Si te gusta el proyecto, no olvides darle una estrella!**