# Guía de Scraping - Datos Reales de Fútbol Argentino

## Status Actual

**Datos Mock** (ejemplo): Cargados en BD
- 11 standings simulados
- 4 fixtures de ejemplo
- 48 trofeos reales ✅

**Dato Real Faltante**: Standings y fixtures actuales de 2025

---

## Opciones de Scraping

### Opción 1: Football-Data.org API ⭐ (Recomendado)

**Ventaja**: Oficial, confiable, mantenida
**Desventaja**: No tiene Liga Argentina (solo Ligas Europeas)
**Conclusión**: ❌ No sirve

---

### Opción 2: ESPN Scraping 🎯

**URL**: https://www.espn.com/soccer/standings

**Ventaja**: Tiene datos de Liga Argentina
**Desventaja**: Requiere parsing HTML (puede cambiar)

**Implementación**:
```python
import requests
from bs4 import BeautifulSoup

url = "https://www.espn.com/soccer/standings?league=arg.1"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.content, 'html.parser')

# Buscar tabla de standings
table = soup.find('table', {'class': 'Table'})
rows = table.find_all('tr')

for row in rows[1:]:  # Skip header
    cells = row.find_all('td')
    position = cells[0].text.strip()
    team = cells[1].text.strip()
    # ... extraer resto de datos
```

**Próximos Pasos**:
1. Instalar: `pip install requests beautifulsoup4`
2. Crear `scripts/scrapers_espn.py`
3. Probar y validar datos
4. Integrar a `scripts/init_all.py`

---

### Opción 3: olé.com.ar Scraping 📰

**URL**: https://www.ole.com.ar/futbol

**Ventaja**: Sitio argentino, actualizado en tiempo real
**Desventaja**: Estructura HTML puede cambiar frecuentemente

**Típica estructura**:
```html
<div class="standings">
  <div class="team">
    <span class="position">1</span>
    <a href="/..." class="name">Boca Juniors</a>
    <span class="points">35</span>
    <!-- stats -->
  </div>
</div>
```

---

### Opción 4: AFA Official API (Si existe)

**URL**: https://www.afa.org.ar/

**Status**: Desconocido si tiene API pública
**Próximo Paso**: Investigar documentación

---

## Implementación Recomendada: ESPN

### Paso 1: Crear Script de Scraping

Crear `scripts/scrapers_real.py`:

```python
#!/usr/bin/env python3
"""Scrapers reales para ESPN (Argentina)"""

import requests
from bs4 import BeautifulSoup
from app.db import SessionLocal
from app.models import Team, StandingEntry, Match
from app.models.enums import MatchStatus
from datetime import datetime

def scrape_standings_from_espn():
    """Extrae tabla de posiciones de ESPN"""
    url = "https://www.espn.com/soccer/standings?league=arg.1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar tabla de standings
        # Estructura específica de ESPN puede variar
        standings = []
        
        # Placeholder - estructura real requiere análisis del HTML
        return standings
        
    except requests.RequestException as e:
        print(f"Error scraping ESPN: {e}")
        return None

def scrape_fixtures_from_espn():
    """Extrae próximos partidos de ESPN"""
    url = "https://www.espn.com/soccer/scores?league=arg.1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        fixtures = []
        # Placeholder - análisis del HTML requerido
        return fixtures
        
    except requests.RequestException as e:
        print(f"Error scraping fixtures: {e}")
        return None
```

### Paso 2: Testear Estructura

```bash
# Ver HTML de la página
curl https://www.espn.com/soccer/standings?league=arg.1 | head -n 100

# Con BeautifulSoup
python3 << 'EOF'
import requests
from bs4 import BeautifulSoup

url = "https://www.espn.com/soccer/standings?league=arg.1"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Buscar clases y IDs relevantes
tables = soup.find_all('table')
print(f"Encontradas {len(tables)} tablas")

# Listar clases de divs
for div in soup.find_all('div', limit=50):
    if div.get('class'):
        print(div.get('class'))
EOF
```

### Paso 3: Validar Datos

```python
# Después de scrapear, validar coherencia
def validate_standings(standings):
    """Verifica que los datos sean válidos"""
    for s in standings:
        played = s['played']
        won = s['won']
        drawn = s['drawn']
        lost = s['lost']
        
        # Validación 1: Total partidos
        if won + drawn + lost != played:
            print(f"⚠️ Error: {s['team']} - G+E+P != PJ")
            return False
        
        # Validación 2: Puntos (3 por victoria, 1 por empate)
        expected_points = won * 3 + drawn
        if expected_points != s['points']:
            print(f"⚠️ Error: {s['team']} - Puntos inconsistentes")
            return False
    
    return True
```

### Paso 4: Integrar a Init All

Modificar `scripts/init_all.py`:

```python
def main() -> int:
    scripts = [
        "seed_teams.py",
        "seed_trophies.py",
        ("scrapers_real.py", "Scraper real de ESPN"),  # Nuevo
        # "scrapers.py",  # Comentar el mock
    ]
    
    for script_info in scripts:
        script = script_info if isinstance(script_info, str) else script_info[0]
        if not run_script(script):
            failed.append(script)
    
    # Si falla scraper real, usar mock como fallback
    if "scrapers_real.py" in failed:
        print("⚠️ Scraper real falló, usando datos mock...")
        run_script("scrapers.py")
```

---

## Alternativa Rápida: Manual + Automático

Para temporada actual:

1. **Manualmente** (1 vez):
   - Copiar tabla de ESPN/olé
   - Pegar en `scripts/standings_2025.json`
   - Script lee JSON e inserta en BD

2. **Automático** (diario):
   - Cron job ejecuta scraper
   - Verifica cambios en standings
   - Actualiza DB si cambiaron

---

## Checklist para Implementación

- [ ] Instalar: `pip install requests beautifulsoup4`
- [ ] Crear `scripts/scrapers_real.py`
- [ ] Analizar estructura HTML de ESPN
- [ ] Implementar funciones de parsing
- [ ] Validar datos extraídos
- [ ] Testear con múltiples clubs
- [ ] Agregar error handling
- [ ] Integrar a `init_all.py`
- [ ] Documentar fuentes
- [ ] Agregar versioning de datos

---

## Problemas Comunes

### "Acceso denegado" (403)
```python
# Solución: User-Agent headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.espn.com",
}
response = requests.get(url, headers=headers)
```

### Estructura HTML cambiada
```python
# Solución: Parsear múltiples selectores
def find_table(soup):
    # Intento 1
    table = soup.find('table', {'class': 'Table'})
    if table:
        return table
    
    # Intento 2
    table = soup.find('table', role='grid')
    if table:
        return table
    
    # Fallback
    return soup.find_all('table')[0]
```

### Nombres de equipos no coinciden
```python
# Mapear nombres
TEAM_MAPPING = {
    "Boca Juniors": "boca",
    "River Plate": "river",
    "Racing Club de Avellaneda": "racing",
    # ...
}

def normalize_team_name(espn_name):
    return TEAM_MAPPING.get(espn_name, espn_name.lower())
```

---

## Status Actual vs Requerido

| Dato | Actual | Real | Fuente |
|------|--------|------|--------|
| Clubes | ✅ Mock | ✅ Real | BD manual |
| Trofeos | ✅ Real | ✅ Real | scripts/seed_trophies.py |
| Standings | ⚠️ Mock | ❌ Falta | ESPN/olé |
| Fixtures | ⚠️ Mock | ❌ Falta | ESPN/olé |
| Jugadores | ❌ Nada | ❌ Falta | Futuro |
| Estadios | ❌ Nada | ⚠️ Parcial | DB manual |

---

## Próximo Paso

Para implementar scraping real ahora:

```bash
# 1. Instalar dependencias
pip install requests beautifulsoup4

# 2. Crear script base
touch scripts/scrapers_real.py

# 3. Analizar ESPN
python3 << 'EOF'
import requests
from bs4 import BeautifulSoup

url = "https://www.espn.com/soccer/standings?league=arg.1"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.content, 'html.parser')

# Imprimir estructura de primera tabla
table = soup.find('table')
if table:
    print("Tabla encontrada!")
    print(table.prettify()[:1000])
else:
    print("No hay tabla - estructura puede ser diferente")
    # Listar divs principales
    for div in soup.find_all('div', class_=True, limit=20):
        print(f"DIV: {div.get('class')}")
EOF
```

