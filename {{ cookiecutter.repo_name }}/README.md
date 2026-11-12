# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Primeros pasos

Instala [uv](https://docs.astral.sh/uv/) y, desde la raíz del proyecto, crea un entorno virtual e instala las dependencias:

```bash
uv venv venv
source venv/bin/activate
uv pip install -r requirements.txt
```

En Windows, activa el entorno con `venv\Scripts\activate` en lugar de `source venv/bin/activate`. El archivo `requirements.txt` está inicialmente vacío; añade las dependencias que necesite el proyecto.

## Estructura inicial

```text
{{ cookiecutter.repo_name }}/
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

- `data/raw/` y `data/processed/`: datos originales y procesados.
- `src/`: código fuente del proyecto.
- `notebooks/`: exploración y experimentación.
- `artifacts/`: resultados y artefactos, como modelos serializados.
- `docs/`, `scripts/` e `infra/`: documentación, scripts auxiliares e infraestructura.
- `.github/workflows/`: ubicación para posibles flujos de GitHub Actions.

Estos directorios están inicialmente vacíos. `Dockerfile`, `docker-compose.yml`, `Taskfile.yml`, `.env` y `.envrc` también están vacíos; no hay flujos de CI/CD, entrenamiento, seguimiento de experimentos ni despliegue configurados.

El `.gitignore` excluye `data/`, `.env` y `.envrc`. Los archivos `.gitkeep` dentro de `data/` también se ignoran: ajusta el `.gitignore` o añádelos explícitamente si necesitas conservar esos directorios en Git.

## Desarrollo del proyecto

Añade el código a `src/`, organiza los datos según su etapa y utiliza los demás directorios cuando los necesites. La estructura facilita la organización, pero no garantiza la reproducibilidad: documenta y controla las dependencias, versiones de datos, parámetros y procedimientos de ejecución.

## Licencia

{% if cookiecutter.open_source_license == 'No license file' %}
No se ha seleccionado una licencia; el archivo `LICENSE` generado no contiene texto de licencia.
{% else %}
Consulta [LICENSE](LICENSE) para conocer los términos de la licencia seleccionada.
{% endif %}

## Atribución

Proyecto basado en [Cookiecutter MLOps](https://github.com/Chim-SO/cookiecutter-mlops/), a su vez basado en [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/).
