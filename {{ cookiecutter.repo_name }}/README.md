# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

**Estado inicial (AS-IS):** estructura de carpetas preparada para añadir pipelines durante el curso. No hay servicios, MLOps, APIs ni infraestructura configurados.

## Punto de partida para ciencia de datos

El ejemplo del notebook estudia **la probabilidad de que un cliente con compras previas vuelva a comprar durante los siguientes 60 días** en diferentes cortes mensuales. El target no depende únicamente de la primera compra.

```bash
uv sync
uv run jupyter lab
```

Abre `notebooks/exploration.ipynb` y ejecuta todas sus celdas. Si no existen datos, el notebook llama a `scripts/generate_transactions.py` para crear 12 meses sintéticos desde enero de 2025.

Para generarlos explícitamente:

```bash
uv run python scripts/generate_transactions.py --init --start 2025-01 --months 12 --customers 1000 --seed 42
```

Los datos observables se guardan en `data/synthetic/raw/`. Los perfiles latentes del generador se guardan en `data/synthetic/simulation/` y no se emplean como variables predictoras.

## Contenido inicial

- `scripts/generate_transactions.py`: generador sintético (único script implementado).
- `notebooks/exploration.ipynb`: EDA, target temporal, feature engineering, split con embargo, modelos y evaluación, implementado totalmente en celdas.
- `src/`, `configs/`, `tests/`, `infra/` y las restantes carpetas: vacías con `.gitkeep`.
- `docker-compose.yml`, `Dockerfile`, `dvc.yaml`, `Taskfile.yml` y entrypoints de pipelines: **archivos vacíos**, intencionalmente.
- `pyproject.toml`: dependencias mínimas para ejecutar el notebook; no instala herramientas de MLOps.

Los pipelines y servicios se incorporarán durante las clases, no desde esta plantilla.
