# Datos de Importación - Biblioteca Calíope

Este directorio contiene archivos CSV para poblar la base de datos con datos de demostración.

## Orden de Importación

**IMPORTANTE:** Respetar el orden de importación debido a las dependencias entre modelos.

| Orden | Archivo | Modelo Odoo | Menú en Odoo |
|-------|---------|-------------|--------------|
| 1 | `usuarios_biblioteca.csv` | `res.partner` | **Contactos** |
| 2 | `categorias.csv` | `libro.categoria` | Biblioteca → Categorías |
| 3 | `autores.csv` | `libro.autor` | Biblioteca → Autores |
| 4 | `libros.csv` | `libro.libro` | Biblioteca → Libros |
| 5 | `prestamos.csv` | `libro.prestamo` | Biblioteca → Préstamos |

## Instrucciones de Importación

### Paso 1: Importar Usuarios (Contactos)

> **IMPORTANTE:** Los usuarios de la biblioteca se importan desde **Contactos**, NO desde Usuarios.

1. Acceder al menú **Contactos** en la barra superior de Odoo
   - Si no aparece el menú, ir a: `Aplicaciones` → Buscar "Contactos" → Instalar
   - O acceder directamente por URL: `http://localhost:8069/web#model=res.partner&view_type=list`
2. Clic en **Favoritos** (estrella) → **Importar registros**
3. Subir el archivo `usuarios_biblioteca.csv`
4. Verificar el mapeo de columnas:
   - `id` → ID externo
   - `name` → Nombre
   - `email` → Correo electrónico
   - `phone` → Teléfono
5. Clic en **Importar**

### Paso 2: Importar Categorías

1. Ir a **Biblioteca Calíope** → **Categorías**
2. Clic en **Favoritos** → **Importar registros**
3. Subir `categorias.csv`
4. Clic en **Importar**

### Paso 3: Importar Autores

1. Ir a **Biblioteca Calíope** → **Autores**
2. Clic en **Favoritos** → **Importar registros**
3. Subir `autores.csv`
4. Clic en **Importar**

### Paso 4: Importar Libros

1. Ir a **Biblioteca Calíope** → **Libros**
2. Clic en **Favoritos** → **Importar registros**
3. Subir `libros.csv`
4. Verificar mapeo:
   - `autor_id` → Autor (busca por nombre)
   - `categoria_id` → Categoría (busca por nombre)
5. Clic en **Importar**

### Paso 5: Importar Préstamos

1. Ir a **Biblioteca Calíope** → **Préstamos**
2. Clic en **Favoritos** → **Importar registros**
3. Subir `prestamos.csv`
4. Verificar mapeo:
   - `libro_id` → Libro prestado (busca por título)
   - `usuario_id` → Usuario que pide (busca por nombre en Contactos)
5. Clic en **Importar**

## Solución de Problemas

### Error: "Múltiples coincidencias encontradas"

Esto ocurre cuando hay contactos duplicados con el mismo nombre.

**Solución:**
1. Ir a **Contactos**
2. Buscar el nombre duplicado (ej: "Mario Ruiz")
3. Eliminar el contacto que NO tenga email `@biblioteca.com`
4. Reintentar la importación

### Error: "No se encontraron registros"

Los registros relacionados (autores, categorías, libros o usuarios) no existen.

**Solución:**
- Verificar que se importaron los archivos anteriores en el orden correcto
- Comprobar que los nombres coinciden exactamente (mayúsculas, tildes, etc.)

## Resumen de Datos

| Archivo | Registros | Descripción |
|---------|-----------|-------------|
| `usuarios_biblioteca.csv` | 5 | Usuarios de la biblioteca (Ana, Carlos, Lucía, Mario, Elena) |
| `categorias.csv` | 5 | Novedades, Clásicos, Infantil, Ciencia y Tecnología, Recomendados |
| `autores.csv` | 8 | Cervantes, García Márquez, Rowling, Orwell, Asimov, King, Allende, Hawking |
| `libros.csv` | 14 | Libros de varios géneros y valoraciones |
| `prestamos.csv` | 25 | Préstamos con diferentes estados (devuelto, prestado, retrasado, perdido) |

## Datos para el Dashboard

Los préstamos incluyen variedad para visualizar estadísticas:

- **Por estado:** 16 devueltos, 6 prestados, 2 retrasados, 1 perdido
- **Por fecha:** Distribuidos de septiembre 2025 a enero 2026
- **Con multas:** 5 préstamos con multas (total: 62.50€)
- **Por usuario:** Distribuidos entre los 5 usuarios
