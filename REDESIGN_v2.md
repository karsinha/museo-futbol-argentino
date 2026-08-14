# Rediseño de Layouts v2.0

## Cambios Implementados

### 1. Landing Page - Arreglo de Scrolling ✅

**Problema**: El rondó causaba scroll infinito en la página principal

**Solución**:
```css
/* Antes */
html, body { overflow: hidden; }
.home-shell { overflow: hidden; }

/* Después */
html, body { margin: 0; }
.home-shell { 
  min-height: 100vh;
  overflow: auto;      /* Permite scroll si es necesario */
  flex-direction: column;
}
```

**Resultado**: El landing ahora respeta el tamaño del viewport sin forzar scroll horizontal en el rondó.

---

### 2. Club Page - Novo Layout con Sidebar Fijo ✅

**Antes**: Diseño lineal vertical
```
┌─────────────────────────────┐
│ Header (Volver al museo)    │
├─────────────────────────────┤
│ Hero Section                │
│ Dashboard Stats (4 cards)   │
│ Resumen + Perfil Panels     │
│ Standings Table             │
│ Fixtures Calendar           │
│ [Nav buttons: Historia...]  │  ← En medio del flujo
│ History Panel               │
└─────────────────────────────┘
```

**Después**: Layout grid 2-columnas
```
┌─────────────────────────────┬──────────┐
│ Header (Volver al museo)    │          │
├─────────────────────────────┼──────────┤
│                             │ SIDEBAR  │
│ Hero Section                │ (Fijo)   │
│ Dashboard Stats             │          │
│ Standings Table             │ 📖 Hist. │
│ Fixtures Calendar           │ ⚔ Rival. │
│ History Panel (dinámico)    │ 🏟 Stad. │
│ (Contenido carga vía HTMX)  │ 🏆 Títul │
│                             │ 🌎 Int'l │
│                             │ 👕 Cami. │
│                             │ ⚽ Plant. │
│                             │ ⭐ Ídol. │
└─────────────────────────────┴──────────┘
```

**Features**:
- ✅ Sidebar **sticky** en desktop (sigue al scroll)
- ✅ Navegación con **iconos emoji** (🏆, ⚔️, etc.)
- ✅ Estilos hover y active con color del club
- ✅ Responsive: navbar horizontal en mobile < 1024px
- ✅ HTMX actualiza history panel sin recargar
- ✅ Indicador visual de sección activa

---

## Estructura HTML Nueva

### Main Container
```html
<main class="club-page-layout">
  <header class="club-topbar">← Volver</header>
  
  <div class="club-container">
    <article class="club-main">
      <!-- Hero, Stats, Standings, Fixtures, History Panel -->
    </article>
    
    <aside class="club-sidebar">
      <!-- Navegación fija (sticky) -->
    </aside>
  </div>
</main>
```

### CSS Grid Layout
```css
.club-container {
  display: grid;
  grid-template-columns: 1fr 280px;  /* main + sidebar */
  gap: 2rem;
  padding: 2rem 1.5rem;
}

.club-sidebar {
  grid-column: 2;
  position: sticky;
  top: 100px;
  height: fit-content;
  max-height: calc(100vh - 150px);
  overflow-y: auto;
}
```

---

## Mobile Responsiveness

**En pantallas < 1024px**:
- Sidebar se convierte en **navbar horizontal** arriba del contenido
- `grid-template-columns: 1fr` (una sola columna)
- Botones en fila con scroll horizontal si necesario
- Mantiene sticky behavior en top

```css
@media (max-width: 1024px) {
  .club-container {
    grid-template-columns: 1fr;
  }
  
  .club-sidebar {
    order: -1;  /* Aparece primero */
    border-bottom: 1px solid;
    display: flex;  /* Horizontal */
  }
}
```

---

## Interactividad con HTMX

Los botones del sidebar usan HTMX para cargar contenido dinámicamente:

```html
<button class="club-sidebar__link" 
        hx-get="/club/{{ team.slug }}/section/titulos"
        hx-target="#club-history-panel"
        hx-swap="innerHTML">
  <span class="icon">🏆</span>
  <span>Títulos</span>
</button>
```

**Cuando se hace clic**:
1. Envía GET a `/club/boca/section/titulos`
2. Recibe HTML parcial
3. Actualiza `#club-history-panel` con fade
4. Script JavaScript marca botón como activo

```javascript
document.addEventListener('htmx:afterSwap', function(event) {
  if (event.detail.target.id === 'club-history-panel') {
    // Marcar botón activo según sección
    const section = event.detail.xhr.responseURL.split('/').pop();
    document.querySelectorAll('.club-sidebar__link').forEach(btn => {
      btn.classList.toggle('is-active', btn.dataset.section === section);
    });
  }
});
```

---

## Estilos Principales

### Sidebar Links
- **Default**: Fondo gris oscuro, hover con borde
- **Active**: Fondo color del club (CSS variable `--primary`), texto oscuro
- **Transition**: Suave 0.2s

### Scrollbar Personalizado
- Ancho: 6px
- Color: `#1e1e2e` (gris oscuro)
- Hover: `#3f46e0` (azul)

### Sticky Positioning
- `top: 100px` desde la parte superior
- `max-height: calc(100vh - 150px)` para que no se salga
- Scrollbar interno si contenido excede altura

---

## Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `app/templates/pages/club.html` | Reorganización completa del layout a grid 2-col + sidebar |
| `app/static/css/main.css` | Nuevos estilos para `.club-page-layout`, `.club-container`, `.club-sidebar`, `.club-sidebar__nav`, `.club-sidebar__link` + responsive |
| `app/static/css/main.css` | Removido estilos antiguos `.history-nav`, `.history-nav__button` (reemplazados por sidebar) |

---

## Testing Manual

### Desktop (1025px+)
```bash
# Ver landing
curl http://127.0.0.1:8000/

# Ver club con sidebar derecho
curl http://127.0.0.1:8000/club/boca | grep -c "club-sidebar"
# Output: 1 (sidebar presente)

# Probar clic en sidebar (HTMX)
curl 'http://127.0.0.1:8000/club/boca/section/titulos'
# Debe retornar panel con trofeos
```

### Mobile (< 1024px)
- Sidebar aparece como navbar horizontal arriba
- Botones scrollean horizontalmente
- History panel debajo

---

## Resultado Visual

### Antes
![alt text needed]
Página del club con navegación en medio del flujo

### Después  
```
┌─────────────────────────────────────┬───────┐
│ ← Volver al museo                   │ 📖 H. │
├─────────────────────────────────────┼───────┤
│  BOCA JUNIORS                       │ ⚔️ Ri │
│  La Boca, CABA · Fundación 1905     │ 🏟️ Es │
│                                      │ 🏆 Tí │
│  🏆 Títulos: 8      ⚽ Jugadores: 0 │ 🌎 In │
│  ⭐ Ídolos: 0       ⚔️ Rivales: 3  │ 👕 Ca │
│                                      │ ⚽ Pl │
│  [Standings Table]                  │ ⭐ Íd │
│                                      │       │
│  [Fixtures Cards]                   │       │
│                                      │       │
│  [History Panel - Dinámico]         │       │
│  Mostrando contenido según botón    │       │
│  seleccionado en sidebar            │       │
└─────────────────────────────────────┴───────┘
```

---

## Ventajas del Nuevo Diseño

1. **Mejor UX**: 
   - Navegación siempre visible (sticky)
   - No necesita scrollear para cambiar sección
   - Indicador visual de sección activa

2. **Más profesional**:
   - Layout tipo dashboard/aplicación
   - Colores y estilos coherentes
   - Responsive desde el inicio

3. **Escalable**:
   - Fácil agregar más secciones al sidebar
   - Contenido dinámico con HTMX
   - Grid flexible para futuras columnas

4. **Accesible**:
   - Emojis + texto en botones
   - Contraste de color suficiente
   - Navegación clara

---

## Próximos Pasos Opcionales

- [ ] Agregar animación de entrada al cambiar sección
- [ ] Indicador de "cargando" mientras HTMX fetcha
- [ ] Breadcrumb mostrando sección actual
- [ ] Guardar sección activa en URL (#anchor)
- [ ] Temporizador visual para próximo partido

