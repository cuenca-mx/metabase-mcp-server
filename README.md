# Fast Agave App Template

El propósito de este template es automatizar la creación de la estructura de proyecto y establecer configuraciones estandar así como las buenas prácticas que hemos reunido desde el origen de los tiempos. Todos los pulls son bienvenidos para contribuir a este template :).

También para hacer menos manchados los pull requests de proyectos nuevos pues mucho código de esos pulls pertenece a la estructura del proyecto.

Este repositorio contiene una plantilla para generar nuevos repositorios de aplicaciones usando `fast-agave` y `fast-agave-authed`.
Contiene la estructura básica que ya hemos implementado en proyectos como **Authed** y **Chester**. 
Esta plantilla crea la siguiente estructura de carpetas:

```
{{top-level-package}}/
├─ models/
│  ├─ __init__.py
├─ resources/
│  ├─ __init__.py
│  ├─ base.py
├─ __init__.py
├─ app.py
├─ config.py
├─ types.py
tests/
├─ resources/
│  ├─ __init__.py
├─ __init__.py
├─ conftest.py
├─ test_app.py
.gitignore
env.template
LICENSE
README.md
requirements.txt
requirements-test.txt
setup.cfg

```
## Cómo crear un nuevo proyecto

1. Clic en el botón **Use this template**
   ![image](https://user-images.githubusercontent.com/37890430/135513617-a6e6c410-ca0a-402b-90e9-8032c1a84724.png)
2. Escribir el nombre del repositorio. Este punto es muy importante pues aparte de dar el nombre del repositorio (y su path dentro de github) también se usará para definir  el `{{top-level-package}}/`.
Como el `{{top-level-package}}` debe ser un nombre válido para Python los `-` serán sustituídos por `_` y todo será en minúsculas.
   Clic en **Create repository from template**
   ![image](https://user-images.githubusercontent.com/37890430/135513442-82271ecd-558b-49cb-aa81-c8b0a5323a06.png)
3. Esperar a que github termine de crear el nuevo repositorio. Inicialmente el nuevo repositorio se verá con unos placeholders raros, pero en este punto un Github Action está construyendo la estructura definitiva del proyecto.
   ![image](https://user-images.githubusercontent.com/37890430/135514174-4822ae23-362a-44c8-abca-57d7288e0e94.png)
   ![image](https://user-images.githubusercontent.com/37890430/135514078-0b494551-6577-47eb-a35e-f4cf052a0e32.png)
4. Esperar a que terminen el Github Action llamado `setup-project-structure`. Al terminar, el repositorio debe tener la estructura definitiva (dale refresh a tu navegador).
![image](https://user-images.githubusercontent.com/37890430/135514460-ea77712c-5098-4e50-a7b4-70663e7c7ce6.png)
![image](https://user-images.githubusercontent.com/37890430/135514307-aea93760-0d49-451a-a495-bc1a619c9861.png)

## Paquetes preinstalados

### Fast-Agave + Fast-Agave-Authed
La estructura de este proyecto contiene una aplicación `fast-agave` mínima lista para poder ser montada en un contenedor.
También sus pruebas unitarias pasan correctamente ya que tiene configurado el fixture `client` con el que se pueden llamar endpoints

### Async Mongoengine
Al usar `fast-agave` automáticamente instala el paquete `mongoengine` y  `mongoengine_plus` para poder utilizar métodos `async` de los objetos de mongoengine.

## Cosas que faltan o que no funcionan del todo bien
### Infraestructura
Aun no genera el código necesario para montarlo en ECS. Tampoco contiene el `Dockerfile`. Por ahora eso se tendrá que hacer manual.

### GH Action tests
Desués de crear el nuevo repositorio el GH Action para tests no funciona correctamente después de crear el repositorio pues el primer commit no tiene la estructura adecuada del proyecto. Es hasta después de un segundo re-run (manual) que debe funcionar correctamente y los tests deben pasar sin problema.
