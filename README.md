# ProyectoDiarioEmocionesV.1

## Características Principales
- Interfaz gráfica con tkinter
- 4 módulos integrados: Usuarios, Emociones, Entradas, Reportes
- Operaciones CRUD completas con Stored Procedures
- Validaciones y confirmaciones
- Base de datos MySQL con relaciones

## Instalación
1. Crear base de datos: `mysql -u root -p < database/diario_emociones.sql`
2. Instalar dependencias: `pip install mysql-connector-python tkcalendar pillow`
3. Ejecutar aplicación: `python src/DiarioEmocionesProyecto.py`

## Estructura de Base de Datos
- **usuarios**: Gestión de usuarios del sistema
- **emociones**: Catálogo de emociones disponibles  
- **entradas**: Entradas del diario emocional
- **entrada_emocion**: Relación entre entradas y emociones

## Stored Procedures Implementados
- Gestión completa de usuarios (crear, leer, actualizar, eliminar)
- Gestión de emociones
- Gestión de entradas con emociones múltiples
- Reportes y estadísticas emocionales
