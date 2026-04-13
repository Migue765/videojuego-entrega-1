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

---

# SEMANA 02

Extensión del ejercicio de la semana 1. Agrega control del jugador por teclado, disparo de balas con el ratón, límite de balas activas y sistemas de colisión.

## Controles nuevos

| Tecla / Acción | Efecto |
|---|---|
| `Flecha izquierda` | Mover jugador a la izquierda |
| `Flecha derecha` | Mover jugador a la derecha |
| `Flecha arriba` | Mover jugador hacia arriba |
| `Flecha abajo` | Mover jugador hacia abajo |
| `Click izquierdo` | Disparar bala hacia el cursor |

## Archivos de configuración nuevos

### `player.json`
Tamaño, color y velocidad de movimiento del jugador (`nP` píxeles/segundo).

```json
{
    "size": { "w": 50, "h": 50 },
    "color": { "r": 0, "g": 200, "b": 0 },
    "speed": 200
}
```

### `bullet.json`
Tamaño, color y velocidad de disparo de las balas (`nV` píxeles/segundo).

```json
{
    "size": { "w": 8, "h": 8 },
    "color": { "r": 255, "g": 255, "b": 0 },
    "speed": 400
}
```

### `level_01.json` (modificado)
Se agregaron `player_spawn` (posición inicial del jugador) y `max_bullets` (límite de balas simultáneas).

```json
{
    "player_spawn": { "x": 295, "y": 155 },
    "max_bullets": 3,
    "enemy_spawn_events": [ ... ]
}
```

## Funcionalidades implementadas

### Jugador
- Creado al inicio en la posición definida por `player_spawn`.
- Se mueve en las cuatro direcciones con las flechas del teclado a `speed` píxeles/segundo.
- No puede salir de los límites de la pantalla.
- Dispara balas hacia el cursor con click izquierdo; la bala sale desde el centro del jugador.

### Balas
- Viajan en línea recta desde el centro del jugador hacia el punto del click.
- Se destruyen al salir de cualquier borde de la pantalla.
- Existe un límite de `max_bullets` balas activas; no se dispara si se alcanza ese límite.

### Colisiones
- **Bala vs Enemigo**: al colisionar, ambas entidades desaparecen.
- **Jugador vs Enemigo**: si el jugador toca un enemigo, el jugador es destruido.

### Sistema de input — patrón Command
- El sistema `s_input` reconstruye cada frame el conjunto de acciones activas a partir del hardware.
- Las acciones (`PLAYER_LEFT`, `PLAYER_RIGHT`, `PLAYER_UP`, `PLAYER_DOWN`, `PLAYER_FIRE`) se almacenan en el componente `CInputCommand`, desacoplando la lectura del hardware del movimiento y el disparo.

## Componentes y sistemas nuevos

### Componentes
| Componente | Descripción |
|---|---|
| `CInputCommand` | Almacena las acciones activas del jugador en el frame actual |
| `CTagPlayer` | Etiqueta que identifica la entidad jugador |
| `CTagBullet` | Etiqueta que identifica una bala |
| `CTagEnemy` | Etiqueta que identifica un enemigo |

### Sistemas
| Sistema | Responsabilidad |
|---|---|
| `system_player_input` | Lee teclado/ratón y actualiza `CInputCommand` (patrón Command) |
| `system_player_movement` | Mueve al jugador según las acciones activas |
| `system_player_boundary` | Evita que el jugador salga de la pantalla |
| `system_player_fire` | Crea balas si la acción `PLAYER_FIRE` está activa |
| `system_bullet_enemy_collision` | Destruye bala y enemigo al colisionar |
| `system_player_enemy_collision` | Destruye al jugador si toca un enemigo |
| `system_bullet_boundary` | Elimina balas que salen de la pantalla |
