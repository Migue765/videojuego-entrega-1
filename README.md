# PLANTILLA PROYECTO - SEMANA 01
Esta plantilla contiene la estructura básica para comenzar los video-series de la semana 1 de "introeucción al desarrollo de videojuegos con ECS"

## Requisitos

- Python 3.10 o superior
- pip

## Instalación de dependencias

```bash
pip install -r requirements.txt
```

## Cómo correr el proyecto

```bash
python main.py
```

## Archivos de configuración

Los archivos se encuentran en `assets/cfg/`:

- `window.json` — título, tamaño, color de fondo y framerate de la ventana
- `enemies.json` — tipos de enemigos con tamaño, color y velocidades
- `level_01.json` — eventos de aparición: qué enemigo, en qué posición y a qué tiempo

Para cambiar el comportamiento del juego basta con editar esos archivos sin tocar el código.

## Controles

- `ESC` o cerrar la ventana — salir del juego
