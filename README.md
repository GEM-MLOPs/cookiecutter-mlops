# Cookiecutter MLOps — plantilla AS-IS (GEM-MLOPs)

Plantilla **intencionalmente vacía** para comenzar proyectos de ciencia de datos y evolucionarlos durante la especialización MLOps. La plantilla no implementa pipelines ni configura infraestructura.

**Únicos recursos con lógica ejecutable dentro del proyecto generado:**

- `scripts/generate_transactions.py`: genera transacciones mensuales sintéticas observables (`customers.csv`, `transactions.csv` particionados). Los perfiles latentes de simulación se guardan por separado y **no son features observables**.
- `notebooks/exploration.ipynb`: un ejercicio AS-IS completo, autocontenido, desde EDA hasta entrenamiento y evaluación de modelos. No importa módulos de `src/`.

El notebook ilustra la predicción de **recompra en los próximos 60 días, evaluada mensualmente para clientes con historial de compra**. No está restringida a los 60 días posteriores a la primera compra.

`docker-compose.yml`, `Dockerfile`, `dvc.yaml`, `Taskfile.yml` y los entrypoints de pipelines están **completamente vacíos** para desarrollarlos en clase. Las carpetas de código/configuración solo contienen `.gitkeep`. No se integran DVC, Feast, RustFS, MLflow, ZenML ni Airflow en la plantilla inicial.

## Generar un proyecto

```bash
uvx cookiecutter https://github.com/GEM-MLOPs/cookiecutter-mlops
cd <repo_name>
uv sync
uv run jupyter lab
```

Abre `notebooks/exploration.ipynb` y ejecuta sus celdas en orden. El notebook invoca el simulador si no existen datos en `data/synthetic/raw/`.

También puedes generar los CSV explícitamente:

```bash
uv run python scripts/generate_transactions.py --init --start 2025-01 --months 12 --customers 1000 --seed 42
```

Un mes adicional es opcional:

```bash
uv run python scripts/generate_transactions.py --advance --scenario normal
```

El simulador no sobrescribe datos existentes. Para reiniciar el ejercicio usa otra carpeta con `--root` o elimina **solo** el estado generado de un proyecto de práctica que ya no necesites.

## Estructura principal del proyecto generado

```text
<repo_name>/
├── artifacts/.gitkeep
├── configs/.gitkeep
├── data/
│   ├── raw/.gitkeep
│   ├── processed/.gitkeep
│   └── synthetic/
│       ├── raw/.gitkeep
│       ├── processed/.gitkeep
│       └── simulation/.gitkeep
├── docs/.gitkeep
├── infra/.gitkeep
├── notebooks/exploration.ipynb
├── scripts/generate_transactions.py
├── src/.gitkeep
├── tests/.gitkeep
├── .github/workflows/.gitkeep
├── docker-compose.yml   # vacío
├── Dockerfile           # vacío
├── dvc.yaml             # vacío
├── Taskfile.yml         # vacío
├── train.py             # vacío
├── evaluate.py          # vacío
├── tune.py              # vacío
├── validate.py          # vacío
├── prepare_data.py      # vacío
└── pyproject.toml       # dependencias ligeras para el notebook
```

El archivo `pyproject.toml` solo contiene bibliotecas de ciencia de datos necesarias para el notebook. No se adjuntan datasets originales, artefactos, modelos ya entrenados ni estado de infraestructura.

## Probar el template localmente

```bash
uvx cookiecutter . --no-input
cd proyecto_mlops
uv sync
uv run jupyter lab
```

## Personalización y desarrollo en clase

Cada alumno puede sustituir el problema de recompra por otro caso de uso. Los directorios y entrypoints existen como posiciones vacías: el alumnado incorporará los pipelines, configuración, seguimiento de experimentos, orquestación y servicios a medida que avance el curso.

La licencia del repositorio de la plantilla y la del proyecto generado son independientes. Cookiecutter permite elegir MIT, BSD-3-Clause o ninguna licencia.
