# NarutoApp - Sistema de Gestión Ninja  
**Trabajo Segundo Corte – Arquitectura de Software**

Aplicación cliente-servidor **monolítica** en Python/Flask que permite a la Aldea Oculta de la Hoja gestionar ninjas, misiones, asignaciones y exportar reportes, cumpliendo con todos los requerimientos del enunciado del **Trabajo Segundo Corte**.

## Requisitos del trabajo cumplidos

-**Arquitectura** Monolítica cliente-servidor (Flask + HTML) 
-**Programación orientada a objetos** Clases: `Ninja`, `Mision`, `Aldea`, `Jutsu`, `AsignacionMision`, `ExportVisitor`, etc. 
-**Persistencia** Base de datos relacional **SQLite**, con modelo MER normalizado 
-**Exportación** Reportes en **CSV y JSON** usando el **patrón de diseño Visitor** 
-**Docker** Contenerización completa con persistencia de datos 
-**Validación**  Asignación de misiones solo si el ninja cumple con el rango mínimo 

## Ejecución con Docker (recomendado)

> **No se necesita instalar Python, Flask ni SQLite localmente. Todo se ejecuta dentro de Docker.**

### Requisitos
- Docker Desktop (Windows/macOS) o Docker Engine + Compose (Linux)
- Acceso a terminal (CMD, PowerShell o bash)

### Pasos
1. Clonar o abrir este repositorio en la máquina.
2. En la raíz del proyecto (`NarutoApp/`), ejecuta:
   ```bash
   docker-compose up --build
