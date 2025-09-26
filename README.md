# PhotoPy Pro - Advanced Image Editor

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)

*Un editor avanzado de imágenes construido con Python*

[Features](#-características) •
[Installation](#-instalación) •
[Usage](#-uso) •
[Architecture](#️-arquitectura) •
[Contributing](#-contribuir)

</div>

---

## 🌟 Características

### 🎨 Herramientas de Edición Profesionales
- **Selecciones Avanzadas**: Rectangular, elíptica, forma libre, varita mágica con tolerancia ajustable
- **Herramientas de Dibujo**: Pincel personalizable, borrador, líneas, formas geométricas
- **Transformaciones**: Recorte interactivo, corrección de perspectiva, rotación
- **Edición de Texto**: Inserción y edición de texto con fuentes personalizadas
- **Clonado Inteligente**: Herramienta de clonado y reparación de áreas

### 🎭 Filtros y Efectos Artísticos
- **Filtros Básicos**: Gaussian Blur, Unsharp Mask, detección de bordes Sobel
- **Efectos Artísticos**: Pintura al óleo, acuarela, sepia, sketch
- **Ajustes de Color**: Brillo/contraste, saturación, curvas de color, niveles
- **Efectos Creativos**: Posterización, inversión de colores, emboss, eliminación de fondo

### 🏗️ Funcionalidades Profesionales
- **Sistema de Capas Completo**: Múltiples capas con opacidad y modos de mezcla
- **Historial Inteligente**: Deshacer/rehacer ilimitado con compresión automática
- **Soporte Multi-formato**: PNG, JPEG, BMP, TIFF con calidad optimizada
- **Interfaz Profesional**: UI dividida en paneles con herramientas organizadas

## 🚀 Instalación

### Requisitos del Sistema
- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, macOS, Linux
- **RAM**: Mínimo 4GB recomendado

### Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/photopy-pro.git
cd photopy-pro

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python main.py
```

### Instalación desde PyPI (Próximamente)
```bash
pip install photopy-pro
photopy-pro
```

## 💻 Uso

### Inicio Rápido
1. **Ejecutar**: `python main.py`
2. **Abrir imagen**: File → Open o Ctrl+O
3. **Seleccionar herramienta**: Panel izquierdo
4. **Editar**: Usar herramientas en el canvas central
5. **Gestionar capas**: Panel derecho
6. **Guardar**: File → Save o Ctrl+S

### Atajos de Teclado
- `Ctrl+N` - Nueva imagen
- `Ctrl+O` - Abrir imagen
- `Ctrl+S` - Guardar
- `Ctrl+Z` - Deshacer
- `Ctrl+Y` - Rehacer
- `Ctrl+Shift+S` - Guardar como

## 🏗️ Arquitectura

### Diseño Modular
```
photopy_pro/
├── 🏛️ core/              # Sistema central
│   ├── constants.py      # Constantes globales
│   ├── commands.py       # Patrón Command (undo/redo)
│   └── worker.py         # Threading para operaciones pesadas
├── 🖼️ ui/                # Interfaz de usuario
│   ├── main_window.py    # Ventana principal
│   ├── canvas.py         # Canvas de edición
│   └── dialogs/          # Diálogos especializados
├── 🛠️ tools/             # Herramientas de edición
│   └── selection.py      # Gestor de selecciones
├── 🎨 filters/           # Filtros y efectos
│   ├── basic.py          # Filtros básicos
│   ├── artistic.py       # Efectos artísticos
│   └── transforms.py     # Transformaciones geométricas
└── ⚙️ utils/             # Utilidades
    ├── image_utils.py    # Conversiones PIL ↔ Qt
    └── blend_modes.py    # Modos de mezcla de capas
```

### Patrones de Diseño Implementados
- **🎯 Command Pattern**: Sistema robusto de undo/redo
- **🧵 Observer Pattern**: Comunicación entre componentes
- **🏭 Factory Pattern**: Creación de herramientas
- **🔧 Strategy Pattern**: Algoritmos de filtros intercambiables

### Características Técnicas
- **Gestión de Memoria**: Compresión inteligente del historial
- **Procesamiento Asíncrono**: Operaciones pesadas en hilos separados
- **Separación de Responsabilidades**: Alta cohesión, bajo acoplamiento
- **Extensibilidad**: Arquitectura plugin-ready

## 🔧 Desarrollo

### Configuración del Entorno de Desarrollo
```bash
# Clonar y configurar
git clone https://github.com/tu-usuario/photopy-pro.git
cd photopy-pro

# Entorno virtual
python -m venv dev-env
source dev-env/bin/activate

# Dependencias de desarrollo
pip install -r requirements.txt
pip install pytest pytest-qt black flake8

# Pre-commit hooks (opcional)
pip install pre-commit
pre-commit install
```

### Estructura para Extensiones

#### 🎨 Añadir Nuevo Filtro
```python
# En filters/basic.py o filters/artistic.py
def mi_nuevo_filtro(pil_img, parametro=10):
    """Descripción del filtro."""
    # Tu implementación aquí
    return processed_image
```

#### 🛠️ Añadir Nueva Herramienta
```python
# En tools/mi_herramienta.py
class MiHerramienta:
    def __init__(self, canvas):
        self.canvas = canvas

    def mouse_press(self, event):
        # Tu lógica aquí
        pass
```

#### 🖥️ Añadir Nuevo Diálogo
```python
# En ui/dialogs/mi_dialogo.py
from PyQt6.QtWidgets import QDialog

class MiDialogo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Tu UI aquí
```

### Testing
```bash
# Ejecutar tests
pytest

# Coverage
pytest --cov=photopy_pro

# Tests de UI
pytest tests/test_ui.py
```

## 📊 Rendimiento

- **Tiempo de inicio**: < 2 segundos
- **Memoria base**: ~150MB
- **Procesamiento**: Optimizado con NumPy y OpenCV
- **Soporte**: Imágenes hasta 8K resolución

## 🤝 Contribuir

### ¡Las contribuciones son bienvenidas!

1. **Fork** el repositorio
2. **Crea** una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abre** un Pull Request

### Áreas de Contribución
- 🐛 **Bug fixes**
- 🎨 **Nuevos filtros y efectos**
- 🛠️ **Herramientas adicionales**
- 🌐 **Internacionalización**
- 📱 **Mejoras de UI/UX**
- 📖 **Documentación**

### Directrices de Código
- Seguir PEP 8
- Docstrings en todas las funciones
- Tests para nuevas funcionalidades
- Commit messages descriptivos

## 📝 Licencia

Este proyecto está licenciado bajo la **MIT License** - ver el archivo [LICENSE](LICENSE) para más detalles.
---

<div align="center">

**PhotoPy Pro** - *Donde la creatividad se encuentra con la tecnología* 🎨✨

[⭐ Star](https://github.com/tu-usuario/photopy-pro) • [🍴 Fork](https://github.com/tu-usuario/photopy-pro/fork) • [📖 Docs](https://github.com/tu-usuario/photopy-pro/wiki)

</div>
