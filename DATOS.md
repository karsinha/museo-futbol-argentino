# Inicialización y Actualización de Datos

Guía completa para cargar y mantener los datos del Museo del Fútbol Argentino.

## Estructura de Scripts

```
scripts/
├── init_db.py           # Crea schema de BD (sin datos)
├── seed_teams.py        # Carga clubes, escudos, standings/fixtures de ejemplo
├── seed_trophies.py     # Carga palmarés reales (48 títulos)
├── scrapers.py          # v1: Scraper simple con datos mock
├── scrapers_v2.py       # v2: Scraper mejorado con estructura expandible
├── verify_data.py       # Verifica estado de datos en BD
└── init_all.py          # Ejecuta todo en orden
```

## Inicialización Completa (Primera Vez)

### Opción 1: Automática (Recomendado)
```bash
python scripts/init_all.py
```

Esto ejecuta en orden:
1. `seed_teams.py` → 11 clubes + escudos + standings/fixtures de ejemplo
2. `seed_trophies.py` → 48 títulos históricos reales
3. `scrapers.py` → Actualiza standings/fixtures (actualmente mock)

### Opción 2: Manual
```bash
# Crear tablas vacías
python scripts/init_db.py

# Cargar datos base
python scripts/seed_teams.py

# Cargar palmarés reales
python scripts/seed_trophies.py

# Actualizar standings y fixtures
python scripts/scrapers.py
```

## Verificación de Datos

```bash
# Ver estado actual de la BD
python scripts/verify_data.py
```

Output esperado:
```
✓ Trofeos en BD: 48
  - Boca: 8 trofeos
    Ejemplos: Campeonato 2024, Campeonato 2020, Campeonato 2015

✓ Entradas de standings: 11
  - Boca: Posición 1, 35 pts

✓ Partidos: 4
  - Programados: 4
```

## Actualización de Datos Actuales

### Actualizar solo standings y fixtures
```bash
python scripts/scrapers.py          # v1 simple
# o
python scripts/scrapers_v2.py       # v2 mejorada
```

### Actualizar solo palmarés (si se agregan datos nuevos)
```bash
python scripts/seed_trophies.py
```

## Expandir Scrapers a Fuentes Reales

### Paso 1: Instalar dependencias
```bash
pip install requests beautifulsoup4
```

### Paso 2: Elegir fuente de datos

#### Opción A: football-data.org (API - Recomendado)
1. Registrarse en https://www.football-data.org/
2. Obtener API key gratuita
3. Guardar en variable de entorno:
   ```bash
   export FOOTBALL_DATA_API_KEY="tu-api-key-aqui"
   ```
4. Descomentar función `scrape_standings_football_data()` en `scrapers_v2.py`
5. Implementar parsing del JSON de la API

#### Opción B: ESPN (Web scraping)
1. Analizar HTML de: https://www.espn.com/soccer/standings
2. Usar BeautifulSoup para parsear tabla
3. Implementar función `scrape_standings_espn()` en `scrapers_v2.py`

#### Opción C: Sitio local (olé.com.ar, AFA)
1. Identificar página con standings actuales
2. Implementar scraper específico con BeautifulSoup
3. Agregar como función en `scrapers_v2.py`

### Paso 3: Pruebas
```bash
# Probar scraper sin actualizar BD
python -c "from scripts.scrapers_v2 import get_standings; print(get_standings())"

# Ejecutar actualización
python scripts/scrapers_v2.py
```

## Estructura de Datos

### Teams (11 clubes)
```
slug         name                city         founded_year
boca         Boca Juniors        Buenos Aires 1905
river        River Plate         Buenos Aires 1901
racing       Racing Club         Avellaneda   1903
... etc
```

### Trophies (48 títulos reales)
```
team_id  trophy_type         year  name                  competition
1        liga                2024  Campeonato 2024       Liga Profesional
1        copa_internacional  2007  Copa Libertadores 2007 Copa Libertadores
```

### StandingEntries (11 filas por season/competition)
```
team_id  season  competition         position  played  won  drawn  lost  goals_for  points
1        2025    Liga Profesional    1         15      11   2      2     28         35
```

### Matches (fixtures programados)
```
home_team_id  away_team_id  scheduled_at        venue                          round_label  status
1             2             2025-08-25 21:00    Estadio Alberto J. Armando    Fecha 16     SCHEDULED
```

## Notas Importantes

- **Datos Mock**: Los datos actuales son placeholders. Implementar scrapers reales para datos actualizados.
- **Actualización Manual**: Mientras no haya scrapers automatizados, actualizar fixtures/standings manualmente:
  ```python
  from scripts.scrapers import update_standings, update_fixtures
  update_standings()
  update_fixtures()
  ```
- **Validación**: Los scrapers validan coherencia de datos (ej: G+E+P = PJ)
- **Fallback**: Si scraping falla, usa automáticamente datos mock para no romper la app

## Troubleshooting

### Error: "Club no encontrado"
- Verificar que slugs en datos de scraper coincidan con modelos en `seed_teams.py`
- Los slugs son: `boca`, `river`, `racing`, `independiente`, `san-lorenzo`, `estudiantes`, `velez`, `newells`, `rosario-central`, `huracan`, `talleres`

### Error: "Base de datos bloqueada"
- Asegurar que la app no está corriendo
- O ejecutar desde otro terminal

### Trofeos no se muestran
- Ejecutar `seed_trophies.py` después de `seed_teams.py`
- Verificar con `verify_data.py`

## Roadmap Futuro

- [ ] Implementar API football-data.org
- [ ] Agregar scraper automático de ESPN
- [ ] Web scraper de AFA oficial
- [ ] Sincronización automática (cron/scheduler)
- [ ] Más datos históricos (h2h, cambios de técnico, etc.)
