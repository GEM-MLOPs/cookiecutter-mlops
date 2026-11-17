# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Primeros pasos

Instala [uv](https://docs.astral.sh/uv/) y, desde la raíz del proyecto, sincroniza el entorno con las dependencias declaradas en `pyproject.toml` y fijadas en `uv.lock`:

```bash
uv sync
```

`uv sync` crea `.venv/` automáticamente e instala las dependencias del proyecto y las del grupo de desarrollo. Para ejecutar comandos dentro del entorno, usa `uv run <comando>`. Si prefieres activarlo manualmente, ejecuta `source .venv/bin/activate` en macOS/Linux o `.venv\Scripts\activate` en Windows.

## Estructura inicial

```text
{{ cookiecutter.repo_name }}/
├── .env.example
├── .envrc
├── .gitattributes
├── .github/
│   └── workflows/
│       └── .gitkeep
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
├── Taskfile.yml
├── artifacts/
│   └── .gitkeep
├── configs/
│   └── .gitkeep
├── data/
│   ├── processed/
│   │   └── .gitkeep
│   └── raw/
│       ├── order_details.csv
│       ├── orders.csv
│       ├── products.csv
│       └── users.csv
├── docker-compose.yml
├── docs/
│   └── .gitkeep
├── infra/
│   └── .gitkeep
├── notebooks/
│   └── exploration.ipynb
├── pyproject.toml
├── scripts/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   └── settings.py
├── tests/
│   └── .gitkeep
└── uv.lock
```

- `data/raw/` contiene datos de ejemplo; `data/processed/` es la ubicación para datos procesados.
- `src/`: paquete para el código fuente y la configuración del proyecto.
- `configs/`: ubicación para archivos de configuración.
- `tests/`: ubicación para las pruebas del proyecto.
- `notebooks/`: notebook inicial de exploración y experimentación.
- `artifacts/`: resultados y artefactos, como modelos serializados.
- `docs/`, `scripts/` e `infra/`: documentación, scripts auxiliares e infraestructura.
- `.github/workflows/`: ubicación para posibles flujos de GitHub Actions.

Los directorios `artifacts/`, `configs/`, `data/processed/`, `docs/`, `infra/`, `scripts/` y `tests/` están inicialmente vacíos. `Dockerfile`, `docker-compose.yml`, `Taskfile.yml`, `.env.example` y `.envrc` también están vacíos; no hay flujos de CI/CD, entrenamiento, seguimiento de experimentos ni despliegue configurados. Las dependencias se declaran en `pyproject.toml` y sus versiones se fijan en `uv.lock`.

El `.gitignore` excluye `.envrc` y archivos locales como cachés de Python, pero no excluye los datos de `data/` ni el entorno `.venv/` creado por `uv sync`. Añade `.venv/` si no quieres incluir ese entorno en Git.

## Desarrollo del proyecto

Añade el código a `src/`, guarda las configuraciones en `configs/`, organiza los datos según su etapa y escribe las pruebas en `tests/`. La estructura facilita la organización, pero no garantiza la reproducibilidad: documenta y controla las dependencias, versiones de datos, parámetros y procedimientos de ejecución.

## Licencia

{% if cookiecutter.open_source_license == 'No license file' %}
No se ha seleccionado una licencia; el archivo `LICENSE` generado no contiene texto de licencia.
{% else %}
Consulta [LICENSE](LICENSE) para conocer los términos de la licencia seleccionada.
{% endif %}

## Atribución

Proyecto basado en [Cookiecutter MLOps](https://github.com/Chim-SO/cookiecutter-mlops/), a su vez basado en [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/).
