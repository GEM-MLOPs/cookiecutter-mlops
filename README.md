# Plantilla Cookiecutter para proyectos de MLOps

## Descripción general

Esta plantilla genera una estructura inicial para proyectos de Machine Learning de la especialización en MLOps Engineer. Establece ubicaciones comunes para código, datos, documentación y otros materiales, de modo que los equipos puedan organizar su trabajo de forma consistente a medida que el proyecto evoluciona.

La estructura sirve como punto de partida para aplicar buenas prácticas de Machine Learning y MLOps; no implementa por sí sola un flujo de entrenamiento o despliegue.

## Características

- Generación de un directorio de proyecto con nombre, descripción, autor y opción de licencia configurables.
- Separación inicial de datos originales y procesados, código, notebooks, documentación y artefactos.
- Archivos `.gitkeep` que mantienen presentes directorios inicialmente vacíos y un `.gitignore` para archivos locales y datos.
- Archivos iniciales para configuración de entorno, contenedores y tareas. Están vacíos y no proporcionan automatización.

La plantilla puede ampliarse con código de entrenamiento, pruebas, seguimiento de experimentos, CI/CD o infraestructura. Estas capacidades no están implementadas actualmente.

## Estructura del proyecto generado

```text
<repo_name>/
├── .env
├── .envrc
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
├── data/
│   ├── processed/
│   │   └── .gitkeep
│   └── raw/
│       └── .gitkeep
├── docker-compose.yml
├── docs/
│   └── .gitkeep
├── infra/
│   └── .gitkeep
├── notebooks/
│   └── .gitkeep
├── requirements.txt
├── scripts/
│   └── .gitkeep
└── src/
    └── .gitkeep
```

- `data/raw/` y `data/processed/`: ubicaciones previstas para datos originales y procesados, respectivamente.
- `src/`: código fuente del proyecto; inicialmente no contiene código.
- `notebooks/`: notebooks de exploración y experimentación.
- `artifacts/`: ubicación prevista para resultados y artefactos, como modelos serializados.
- `docs/`, `scripts/` e `infra/`: documentación, scripts auxiliares y archivos de infraestructura que se incorporen posteriormente.
- `.github/workflows/`: ubicación prevista para flujos de GitHub Actions; no contiene flujos configurados.

`Dockerfile`, `docker-compose.yml`, `Taskfile.yml`, `.env`, `.envrc` y `requirements.txt` se generan vacíos. `README.md` y `LICENSE` se generan a partir de las variables de la plantilla.

El `.gitignore` generado excluye `data/`, `.env` y `.envrc`. Por tanto, Git también ignorará los `.gitkeep` dentro de `data/` por defecto; si se necesitan esos directorios en un repositorio nuevo, será necesario ajustar el `.gitignore` o añadirlos explícitamente.

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

Entra en el directorio generado y utiliza `uv` para crear el entorno virtual e instalar las dependencias. Sustituye `Proyecto-MLOps` por el valor elegido para `repo_name`:

```bash
cd Proyecto-MLOps
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

En Windows, activa el entorno con `.venv\Scripts\activate` en lugar de `source .venv/bin/activate`. El `.gitignore` generado no excluye `.venv/`; añádelo si no quieres incluir el entorno en Git. El archivo `requirements.txt` generado está vacío, por lo que la instalación inicial no añade dependencias. Registra allí las dependencias que necesite el proyecto.

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
