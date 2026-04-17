# 🦷 Sistema de Gestión de Cola para Consultorio Odontológico

Sistema completo para la gestión de pacientes, priorización de citas y simulación de atención en consultorios odontológicos.

## 📋 Versión
**v1.0** - Validación completa de datos (rechaza nombres sin sentido)

## ✨ Características Principales

- ✅ **Registro inteligente de pacientes** con validación avanzada de nombres
- 🎯 **Sistema de prioridades**: Urgente → Normal → Baja
- 📅 **Ordenamiento por fecha** dentro de cada nivel de prioridad
- 🔥 **Plan de contingencia** para extracciones urgentes
- 🎲 **Simulación de atención por lotes** (atender 1, varios o todos)
- 📊 **Historial completo** de pacientes atendidos
- 🔄 **Reinicio de datos** cuando sea necesario
- 🛡️ **Validaciones robustas** para todos los campos

## 🚀 Funcionalidades

### 1. Registro de Pacientes
- ID autoincremental con formato `P001`, `P002`, etc.
- Validación inteligente de nombres:
  - Mínimo 3 caracteres, máximo 50
  - Solo letras, espacios, puntos y guiones
  - Rechaza nombres sin sentido (ej: "aaaaaa")
  - Requiere al menos una vocal y una consonante
- Validación de fechas:
  - Formato YYYY-MM-DD
  - No permite fechas pasadas
  - Rango 2024-2030
- Selección de tipo de procedimiento:
  - Extracción, Limpieza, Caries, Ortodoncia u Otro
- Asignación de prioridad:
  - 🔴 Urgente (máxima prioridad)
  - 🟡 Normal
  - 🟢 Baja

### 2. Plan de Contingencia
- Filtra específicamente pacientes con:
  - Tipo: Extracción
  - Prioridad: Urgente
- Ordena por fecha más cercana
- Genera informe especial con prioridad absoluta

### 3. Cola de Atención
- Ordenamiento automático por:
  1. Prioridad (Urgente → Normal → Baja)
  2. Fecha más cercana
- Visualización clara con íconos de prioridad
- Muestra total de pacientes pendientes

### 4. Simulación de Atención
- Permite atender por lotes:
  - Solo el siguiente paciente
  - Cantidad específica
  - Todos los pacientes
- Muestra desglose por prioridad
- Registro automático en historial
- Confirmación antes de proceder

### 5. Historial de Atendidos
- Registro con fecha y hora de atención
- Detalle completo del paciente atendido
- Estadísticas por prioridad

### 6. Gestión de Datos
- Reinicio completo del sistema
- Resumen final al salir con estadísticas detalladas

## 💻 Requisitos del Sistema

- Python 3.6 o superior
- Sistema operativo: Windows, Linux o macOS

## 🔧 Instalación

1. **Clonar o descargar el repositorio**
```bash
git clone https://github.com/jupis2015/contingencia_odontologico.git
cd contingencia_odontologico