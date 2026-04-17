# AGENTS.md

## Run
- Start app: `python Frontend/src/app.py`

## Entry Points
- `Frontend/src/app.py` - Flet UI (entry point)
- `Back/validador.py` - Data validation + historical concatenation
- `Back/predictor.py` - Prophet prediction engine
- `Back/reglas_negocio.py` - Stock alerts logic

## Data Schema
- Required columns: `Fecha`, `Producto`, `Ventas`
- Prophet format: `ds` (date), `y` (value)

## Rules for Frontend
- Full architecture: see `instrucciones/SKILLS/SKILL_GIT.md`

## Architecture
- No HTTP APIs; Frontend imports Backend classes directly
- All data passes as pandas DataFrames
- Full architecture: see `instrucciones/instrucciones.md`

## Additional Instruccion
- No crees repositorios de git jamas uses git init 
- Instrucciones para GIT : `instrucciones/SKILLS/SKILL_GIT.md`
