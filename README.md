# MISO Shooter — Semana 4

Arena shooter 2D construido en Python con pygame-ce sobre una arquitectura Entity-Component-System pura.

**Jugar en el navegador:** https://miguel765.itch.io/miso-shooter

---

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

```bash
pip install pygame-ce "esper==2.5"
```

## Cómo correr el proyecto

```bash
python main.py
```

---

## Controles

| Tecla / Acción | Efecto |
|---|---|
| Flechas | Mover la nave |
| Click izquierdo | Disparar hacia el cursor |
| `ESPACIO` | Onda de choque (destruye naves cercanas) |
| `P` | Pausar / reanudar |
| `ESC` | Salir |

---

## Cómo jugar

Sobrevive oleadas de asteroides y cazadores enemigos. Los Hunters te persiguen cuando te acercas y regresan a su posición si te alejas. Usa el disparo normal para eliminarlos uno a uno, o activa la onda de choque para limpiar todo lo que tengas cerca de un solo golpe. La onda tiene un cooldown de 5 segundos — úsala con cabeza. Si un enemigo te toca, la nave explota y el juego reinicia automáticamente.

---

## Archivos de configuración

Todos los parámetros del juego se controlan desde `assets/cfg/` sin tocar el código:

| Archivo | Descripción |
|---|---|
| `window.json` | Título, tamaño, color de fondo y framerate |
| `player.json` | Sprite, velocidad y configuración de habilidad especial |
| `bullet.json` | Sprite, velocidad y sonido de las balas |
| `enemies.json` | Tipos de enemigos con sprites, velocidades y sonidos |
| `explosion.json` | Sprite animado y sonido de explosiones |
| `level_01.json` | Posición inicial del jugador, límite de balas y eventos de spawn |
| `interface.json` | Fuentes, textos, colores y posiciones de todos los elementos de HUD |

---

## Arquitectura

El proyecto sigue el patrón **Entity-Component-System (ECS)** usando la librería `esper`.

### Componentes

| Componente | Descripción |
|---|---|
| `CTransform` | Posición (x, y) de la entidad |
| `CVelocity` | Velocidad (vx, vy) |
| `CSurface` | Superficie pygame y área del frame activo en el spritesheet |
| `CAnimation` | Estado de animación: frame actual, framerate, animación activa |
| `CInputCommand` | Acciones activas del jugador en el frame (patrón Command) |
| `CHunterState` | Máquina de estados del Hunter: IDLE / CHASING / RETURNING |
| `CEnemySpawner` | Cola de eventos de spawn con tiempos y posiciones |
| `CSpecialAbility` | Cooldown y radio de la onda de choque del jugador |
| `CShieldWave` | Estado visual del anillo expansivo de la onda de choque |
| `CTagPlayer` | Etiqueta: entidad jugador |
| `CTagBullet` | Etiqueta: bala |
| `CTagEnemy` | Etiqueta: enemigo |
| `CTagHunter` | Etiqueta: Hunter (subclase de enemigo) |
| `CTagExplosion` | Etiqueta: explosión en curso |

### Sistemas

| Sistema | Responsabilidad |
|---|---|
| `system_player_input` | Lee teclado y ratón, actualiza `CInputCommand` |
| `system_player_movement` | Mueve al jugador según las acciones activas |
| `system_player_boundary` | Mantiene al jugador dentro de la pantalla |
| `system_player_fire` | Crea balas al detectar la acción `PLAYER_FIRE` |
| `system_shield_activate` | Activa la onda de choque y destruye enemigos en radio |
| `system_shield_update` | Expande el anillo visual de la onda cada frame |
| `system_shield_cooldown` | Descuenta el cooldown de la habilidad especial |
| `system_shield_render` | Dibuja el anillo cian con transparencia (SRCALPHA) |
| `system_enemy_spawner` | Lanza enemigos según el calendario del nivel |
| `system_hunter_state` | FSM del Hunter: detecta al jugador y controla el movimiento |
| `system_movement` | Aplica velocidades a todas las entidades móviles |
| `system_bounce` | Rebota asteroides en los bordes de la pantalla |
| `system_bullet_boundary` | Elimina balas que salen de la pantalla |
| `system_bullet_enemy_collision` | Destruye bala y enemigo al colisionar, genera explosión |
| `system_player_enemy_collision` | Destruye al jugador al colisionar, inicia cuenta regresiva de reinicio |
| `system_animation` | Avanza frames del spritesheet según el framerate de la animación |
| `system_explosion` | Elimina entidades de explosión al terminar su animación |
| `system_render` | Dibuja todas las entidades con `CTransform` + `CSurface` |
| `system_hud_render` | Dibuja título, instrucciones e indicador de cooldown |
| `system_hud_pause` | Overlay semitransparente de pausa |
| `system_hud_game_over` | Overlay de "GAME OVER" durante el reinicio |

### Patrón Service Locator

`ServiceLocator` centraliza el acceso a tres servicios con caché:

- **`ImageService`** — carga y cachea `pygame.Surface` por ruta y número de frames
- **`SoundService`** — carga, cachea y reproduce archivos `.ogg`; no-op si el mixer no está disponible
- **`FontService`** — carga y cachea `pygame.font.Font` por ruta y tamaño

---

## Semanas anteriores

<details>
<summary>Semana 3 — Sprites, animaciones y enemigo Hunter</summary>

Extensión de la semana 2. Reemplaza los rectángulos por sprites animados, agrega el enemigo Hunter con IA y explosiones animadas como entidades ECS independientes.

**Componentes nuevos:** `CSurface`, `CAnimation`, `CHunterState`, `CTagHunter`, `CTagExplosion`

**Sistemas nuevos:** `system_animation`, `system_hunter_state`, `system_explosion`

</details>

<details>
<summary>Semana 2 — Jugador, disparo y colisiones</summary>

Extensión de la semana 1. Agrega control del jugador por teclado, disparo con el ratón y colisiones.

**Controles:** flechas para mover, click izquierdo para disparar.

**Patrón Command:** acciones (`PLAYER_LEFT`, `PLAYER_RIGHT`, `PLAYER_UP`, `PLAYER_DOWN`, `PLAYER_FIRE`) almacenadas en `CInputCommand`, desacoplando hardware de lógica.

</details>

<details>
<summary>Semana 1 — Base ECS y spawn de enemigos</summary>

Estructura base del proyecto con movimiento, rebote y spawn de enemigos por eventos temporales configurados en `level_01.json`.

</details>
