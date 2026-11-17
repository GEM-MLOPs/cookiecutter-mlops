# Plantilla Cookiecutter para proyectos de MLOps

## Descripción general

Esta plantilla genera una estructura inicial para proyectos de Machine Learning de la especialización en MLOps Engineer. Establece ubicaciones comunes para código, datos, documentación y otros materiales, de modo que los equipos puedan organizar su trabajo de forma consistente a medida que el proyecto evoluciona.

La estructura sirve como punto de partida para aplicar buenas prácticas de Machine Learning y MLOps; no implementa por sí sola un flujo de entrenamiento o despliegue.

## Características

- Generación de un directorio de proyecto con nombre, descripción, autor y opción de licencia configurables.
- Organización de datos de ejemplo, código fuente, configuración, pruebas, notebooks, documentación y artefactos.
- Archivos `.gitkeep` que mantienen presentes directorios inicialmente vacíos y un `.gitignore` para archivos locales.
- Gestión de dependencias con `pyproject.toml` y `uv.lock`; los archivos de contenedor y tareas son puntos de partida vacíos, no automatizaciones configuradas.

La plantilla puede ampliarse con código de entrenamiento, pruebas, seguimiento de experimentos, CI/CD o infraestructura. Estas capacidades no están implementadas actualmente.

## Estructura del proyecto generado

```text
<repo_name>/
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

- `data/raw/` y `data/processed/`: datos de ejemplo originales y ubicación para datos procesados.
- `src/`: paquete para el código fuente y la configuración del proyecto.
- `configs/`: ubicación para archivos de configuración.
- `tests/`: ubicación para las pruebas del proyecto.
- `notebooks/`: notebook inicial de exploración y experimentación.
- `artifacts/`: ubicación prevista para resultados y artefactos, como modelos serializados.
- `docs/`, `scripts/` e `infra/`: documentación, scripts auxiliares y archivos de infraestructura que se incorporen posteriormente.
- `.github/workflows/`: ubicación prevista para flujos de GitHub Actions; no contiene flujos configurados.

`Dockerfile`, `docker-compose.yml`, `Taskfile.yml`, `.env.example` y `.envrc` se generan vacíos. `pyproject.toml` declara las dependencias y `uv.lock` fija sus versiones. `README.md` y `LICENSE` se generan a partir de las variables de la plantilla.

El `.gitignore` generado excluye `.envrc` y archivos locales como cachés de Python, pero no excluye los datos de `data/`. Tampoco excluye `.venv/`, que es el entorno creado por `uv sync`; añádelo si no quieres incluir ese entorno en Git.

## Requisitos previos

- Para ejecutar la plantilla, usa `uvx` de [uv](https://docs.astral.sh/uv/) o una instalación de [Cookiecutter](https://cookiecutter.readthedocs.io/).
- Para los primeros pasos del proyecto generado, instala [uv](https://docs.astral.sh/uv/). Si instalas Cookiecutter mediante `pip`, necesitas Python 3 con `pip`; utiliza una versión compatible con la versión de Cookiecutter instalada.
- Git es necesario para obtener la plantilla desde una URL de GitHub.

Instalación tradicional opcional de Cookiecutter:

```bash
python3 -m pip install cookiecutter
```

Los ejemplos siguientes usan el ejecutable `cookiecutter`; con `uvx`, sustituye `cookiecutter` por `uvx cookiecutter` en cada comando.

## Cómo utilizar la plantilla

Sustituye la ruta por la ubicación de este repositorio. Cookiecutter solicitará los valores definidos en `cookiecutter.json`:

| Variable | Descripción y valor predeterminado |
| --- | --- |
| `project_name` | Nombre del proyecto; `project_name`. |
| `repo_name` | Nombre del directorio generado; por defecto deriva de `project_name`, en minúsculas y sustituyendo espacios por guiones bajos. Puede modificarse durante la generación. |
| `author_name` | Autor, organización o equipo; `Your name (or your organization/company/team)`. |
| `description` | Descripción breve; `A short description of the project.` |
| `open_source_license` | Selección entre `MIT` (predeterminada), `BSD-3-Clause` y `No license file`. |

Con `No license file`, la implementación actual genera igualmente un archivo `LICENSE` prácticamente vacío, sin texto de licencia; no lo elimina.

### Desde GitHub

Usa la URL real del repositorio que publique esta versión de la plantilla:

```bash
cookiecutter https://github.com/GEM-MLOPs/cookiecutter-mlops.git
```

## Primeros pasos después de generar el proyecto

Entra en el directorio generado y utiliza `uv` para crear el entorno virtual e instalar las dependencias declaradas en `pyproject.toml`, usando las versiones de `uv.lock`. Sustituye `Proyecto-MLOps` por el valor elegido para `repo_name`:

```bash
cd Proyecto-MLOps
uv sync
```

`uv sync` crea `.venv/` automáticamente. Para ejecutar comandos dentro del entorno sin activarlo, usa `uv run <comando>`. Si prefieres activarlo manualmente, ejecuta `source .venv/bin/activate` en macOS/Linux o `.venv\Scripts\activate` en Windows. Añade las dependencias del proyecto en `pyproject.toml` y actualiza `uv.lock` con `uv lock`.

Actualiza el README generado, coloca los datos en `data/` según su etapa y desarrolla el código en `src/`. Usa los demás directorios cuando el proyecto los necesite. Revisa la licencia generada antes de distribuir el proyecto.

## Relación con el ciclo de vida de MLOps

La separación de código, datos y notebooks ayuda a ordenar la preparación de datos y la experimentación; `artifacts/` ofrece un lugar para guardar resultados o modelos. Esta organización no garantiza la reproducibilidad de experimentos: para ello habrá que definir y registrar, entre otros elementos, dependencias, versiones de datos, parámetros y procedimientos de ejecución.

No se incluyen seguimiento de experimentos, versionamiento de datos, orquestación ni CI/CD. Pueden incorporarse posteriormente según las necesidades del proyecto.

## Personalización

1. Modifica `cookiecutter.json` para cambiar valores predeterminados o añadir variables. Actualiza también las expresiones `{{ cookiecutter.* }}` de los archivos que deban utilizarlas.
2. Añade directorios y archivos dentro de `{{ cookiecutter.repo_name }}/`. Usa `.gitkeep` en los directorios vacíos que deban conservarse en Git y revisa las reglas de `.gitignore`.
3. Prueba la generación desde la copia local en un directorio temporal, con valores y opciones de licencia representativos. Comprueba los nombres, el contenido renderizado y las rutas antes de publicar los cambios.

## Atribución y licencia

Esta plantilla deriva de [Cookiecutter MLOps](https://github.com/Chim-SO/cookiecutter-mlops), basada a su vez en [Cookiecutter Data Science](https://github.com/drivendata/cookiecutter-data-science). La licencia de este repositorio se encuentra en [LICENSE](LICENSE); la licencia del proyecto generado se configura por separado.
