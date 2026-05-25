# Maestro Arrocero — Design Brief

## Concepto

Aplicación web progresiva (PWA) de recetas de arroces de autor y guías de brasa. Funciona como app nativa en móvil (instalable, offline). Audiencia: cocineros apasionados y profesionales del arrocería.

Tono visual: **artesanal, cálido, sofisticado** — sin caer en lo rústico. Referentes: cookbooks de alta gama, Monocle, Osteria Francescana.

---

## Tipografía

| Uso | Familia | Peso |
|---|---|---|
| Títulos, nombres de receta | Playfair Display | 700 (regular) / 400 italic |
| Cuerpo, UI, etiquetas | DM Sans | 300 · 400 · 500 |

La combinación serif/sans crea contraste editorial. Playfair en italic aparece en subtítulos para un toque magazine.

---

## Paleta de color

### Semántica de color

| Token | Hex | Uso |
|---|---|---|
| `--rice` | `#C8864A` | Acento principal — CTA, activos, resultados destacados |
| `--rice-dark` | `#8B5A2B` | Hover sobre rice, texto sobre fondos claros |
| `--rice-light` | `#F5E6D3` | Fondos de badges, tabs activos, highlights suaves |
| `--saffron` | `#E8A020` | Acento secundario — estrellas, etiquetas "eyebrow" |
| `--water` | `#3A7CA5` | Sección de agua — botones, resultados hídricos |
| `--success` | `#4A7C59` | Estados correctos, check, completado |
| `--danger` | `#B5372A` | Acciones destructivas |

### Tema claro (default)

| Token | Hex |
|---|---|
| `--bg` | `#C8BFB0` — beige cálido medio, fondo de pantalla |
| `--surface` | `#BEB5A5` — superficie levemente más oscura |
| `--card-bg` | `rgba(255,255,255,0.45)` — tarjetas translúcidas sobre beige |
| `--text` | `#2A1F14` — marrón muy oscuro, casi negro cálido |
| `--text-muted` | `#7A6555` — marrón medio, texto secundario |
| `--nav-bg` | `#2A1F14` — nav superior oscura, contraste máximo |

### Tema oscuro

| Token | Hex |
|---|---|
| `--bg` | `#0F1923` — azul muy oscuro, no negro puro |
| `--surface` | `#151E28` |
| `--card-bg` | `rgba(255,255,255,0.04)` — tarjetas casi invisibles |
| `--text` | `#F0EBE3` — blanco cálido |
| `--nav-bg` | `#0A1018` |

El oscuro es azul marino, no gris neutro. Evoca la noche en cocina.

---

## Estructura de pantallas

La app tiene **navegación en dos niveles**:

```
┌─────────────────────────────┐
│  NAV SUPERIOR (sticky 52px) │  Logo + toggle tema claro/oscuro
├─────────────────────────────┤
│                             │
│     PANTALLA ACTIVA         │  padding 1.5rem 1rem 5rem
│     max-width 680px         │
│     centrada                │
│                             │
├─────────────────────────────┤
│  BOTTOM TABS (fixed 54px)   │  Inicio · Recetas · Config. · Guías
└─────────────────────────────┘
```

### Pantallas principales

| ID | Nombre | Descripción |
|---|---|---|
| `home` | Inicio | Hero rotatorio de recetas destacadas + grid de sugeridas |
| `recetas` | Recetas | Lista completa de recetas |
| `recipe` | Receta | Detalle: guía paso a paso + ingredientes escalables |
| `agua` | Config. | Calculadora de agua + gestión de equipos + calibración |
| `instrucciones` | Guías | Vídeos + guía de tipos de arroz |
| `nivel` | Nivel | Giroscopio / nivelador de paella |
| `bascula` | Báscula | Báscula experimental por presión táctil |

---

## Componentes

### Nav superior
- Fondo `#2A1F14` · altura 52px · sticky
- Logo: "Maestro **Arrocero**" en Playfair, la palabra en saffron
- Derecha: toggle claro/oscuro (botón pill con borde translúcido)

### Bottom tabs
- 4 tabs de igual anchura · texto uppercase 0.78rem DM Sans
- Estado activo: texto rice, fondo `rgba(200,134,74,.12)`, borde rice 0.5px
- Estado inactivo: text-muted

### Tarjetas de receta (home)
- Fondo `card-bg` (translúcido) · borde suave · border-radius 12px
- Emoji grande centrado + nombre + badge de dificultad
- Hover: sombra + ligero scale up

### Hero de receta (home)
- Imagen a pantalla completa (220px altura) sangrada al borde
- Gradiente `to top` desde `rgba(46,41,37,.97)` → transparente
- Texto superpuesto: eyebrow en saffron uppercase + nombre en Playfair blanco 1.6rem + estrellas + tiempo + botón CTA rice

### Pantalla de receta
- **Tab "Guía paso a paso"**: barra de progreso rice + tarjeta de paso con número, título, texto, tiempo, ingredientes del paso + temporizador de paso (cuenta atrás manual)
- **Tab "Ingredientes"**: slider de comensales (1-20) con escala automática de cantidades + cálculo de agua (incluye evaporación calibrada del equipo) + botón compartir
- **Modo cocina**: toggle en cabecera — activa WakeLock (pantalla siempre encendida), oculta bottom nav, agranda tipografía de pasos
- **Temporizador global**: barra flotante sticky bajo la cabecera cuando se inicia la cocción, con cuenta atrás, pausa y vibración/sonido al terminar

### Result box
- Fondo `#FFF8F0` · borde suave
- Etiqueta uppercase pequeña + valor grande en Playfair rice + unidad muted

### Botones
| Variante | Apariencia |
|---|---|
| `.btn` (primario) | Fondo rice · texto blanco |
| `.btn-secondary` | Transparente · borde rice · texto rice |
| `.btn-water` | Fondo azul water |
| `.btn-danger` | Fondo danger rojo |
| `.btn-ghost` | Transparente · borde border · texto muted |
| `.btn-sm` | padding reducido, 0.78rem |
| `.btn-full` | 100% anchura |

### Badges / pills
- **Comensales**: `rice-light` bg · `rice-dark` text · pill
- **Dificultad / tipo**: misma estética
- **Pendiente**: surface bg · text-muted · borde · italic

---

## Maestro Brasas (brasas.html)

App separada, misma identidad visual pero con paleta más oscura y ahumada. Accesible desde el shortcut de la PWA. Misma estructura nav superior + bottom tabs + screens.

Contenido: recetas de carne a la brasa organizadas por categoría (vacuno, cerdo, aves, cordero, aliños, tipo de leña).

---

## PWA / Instalación

- Icono: logotipo "Arroces de Bandera" sobre fondo transparente, sin enmascarar (el badge sobresale del círculo del launcher intencionalmente)
- `theme_color`: `#2A1F14`
- `background_color`: `#C8BFB0`
- Banner de instalación propio en la parte inferior (fondo `#2A1F14`, botón rice, X para cerrar)

---

## Áreas de mejora identificadas (pendiente de diseño)

- **Guía de arroces**: las variedades sin ratio configurado (Senia, Bahía, Carnaroli, Arborio, Jazmín, Basmati) muestran "pendiente de configurar" en pill gris — necesitan datos reales del chef
- **Modo cocina**: funcional pero sin diseño propio — podría tener una UI más inmersiva (fondo más oscuro, texto más grande, sin distracciones)
- **Autor.html**: módulo de IA para generar recetas — en pausa hasta tener proxy Cloudflare para la API
- **Filtros en pantalla Recetas**: actualmente lista plana, sin filtro por tipo/dificultad/tiempo
