# -*- coding: utf-8 -*-
"""
Autor: [Henry Franco Velez]
Descripción: Sistema de gestión de cola para consultorio odontológico.
Versión: v1.0 - Validación completa de datos (rechaza nombres sin sentido)
"""

import datetime
import os
import re

# ------------------------------
# VARIABLES GLOBALES
# ------------------------------
contador_id = 0
historial_atendidos = []

def generar_id():
    """Genera un ID autoincrementable con formato PXXX"""
    global contador_id
    contador_id += 1
    return f"P{contador_id:03d}"

# ------------------------------
# MODELO DE DATOS
# ------------------------------
class Paciente:
    def __init__(self, id_paciente: str, nombre: str, fecha_cita: str, tipo_procedimiento: str, prioridad: str):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.fecha_cita = fecha_cita
        self.tipo_procedimiento = tipo_procedimiento
        self.prioridad = prioridad
    
    def __repr__(self):
        return f"{self.nombre} (ID:{self.id_paciente}) - {self.fecha_cita} - {self.prioridad}"

# ------------------------------
# FUNCIONES DE VALIDACIÓN
# ------------------------------
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_nombre(nombre: str) -> bool:
    """
    Valida que el nombre sea un nombre REAL:
    - Mínimo 3 caracteres, máximo 50
    - Solo letras, espacios, puntos y guiones
    - No puede ser todo la misma letra (ej: "aaaaaa")
    - Debe tener al menos una vocal y una consonante
    """
    if not nombre or len(nombre.strip()) < 3:
        print("❌ El nombre debe tener al menos 3 caracteres.")
        return False
    
    if len(nombre) > 50:
        print("❌ El nombre es demasiado largo (máximo 50 caracteres).")
        return False
    
    # Permite letras (incluyendo acentos), espacios, puntos y guiones
    patron = r'^[A-Za-záéíóúñÁÉÍÓÚÑ\s\.\-]+$'
    if not re.match(patron, nombre):
        print("❌ El nombre solo puede contener letras, espacios, puntos y guiones.")
        return False
    
    # Eliminar espacios para analizar caracteres
    nombre_sin_espacios = nombre.replace(" ", "").replace(".", "").replace("-", "")
    
    if len(nombre_sin_espacios) < 2:
        print("❌ El nombre es demasiado corto.")
        return False
    
    # Verificar que no sea todo la misma letra (ej: "aaaaaa", "bbbbbb")
    if len(set(nombre_sin_espacios.lower())) == 1:
        print("❌ El nombre no puede consistir solo de letras repetidas (ej: 'aaaaaa').")
        return False
    
    # Verificar que tenga al menos una vocal
    vocales = "aeiouáéíóú"
    tiene_vocal = any(letra in vocales for letra in nombre_sin_espacios.lower())
    if not tiene_vocal:
        print("❌ El nombre debe contener al menos una vocal.")
        return False
    
    # Verificar que tenga al menos una consonante
    consonantes = "bcdfghjklmnpqrstvwxyzñ"
    tiene_consonante = any(letra in consonantes for letra in nombre_sin_espacios.lower())
    if not tiene_consonante:
        print("❌ El nombre debe contener al menos una consonante.")
        return False
    
    return True

def validar_fecha(fecha_str: str) -> bool:
    """
    Valida que la fecha:
    - NO esté vacía
    - Tenga formato YYYY-MM-DD
    - Sea una fecha real
    - No sea anterior a hoy
    - Esté dentro de un rango razonable (2024-2030)
    """
    if not fecha_str or fecha_str.strip() == "":
        print("❌ La fecha no puede estar vacía. Debe ingresar una fecha en formato YYYY-MM-DD")
        return False
    
    try:
        fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hoy = datetime.datetime.now().date()
        
        if fecha.year < 2024 or fecha.year > 2030:
            print(f"❌ El año debe estar entre 2024 y 2030 (ingresó: {fecha.year})")
            return False
        
        if fecha < hoy:
            print(f"❌ No se pueden agendar citas en fechas pasadas. Hoy es {hoy}")
            return False
        
        return True
        
    except ValueError:
        print("❌ Fecha inválida. Use el formato YYYY-MM-DD (ej: 2025-04-18)")
        return False

def obtener_opcion_valida(mensaje: str, min_opcion: int, max_opcion: int) -> str:
    """Función genérica para obtener una opción válida del usuario"""
    while True:
        try:
            opcion = input(mensaje).strip()
            if not opcion:
                print(f"❌ Debe seleccionar una opción ({min_opcion}-{max_opcion})")
                continue
            
            opcion_num = int(opcion)
            if opcion_num < min_opcion or opcion_num > max_opcion:
                print(f"❌ Opción inválida. Seleccione {min_opcion}-{max_opcion}")
                continue
            
            return str(opcion_num)
        except ValueError:
            print(f"❌ Debe ingresar un número ({min_opcion}-{max_opcion})")

def ingresar_paciente() -> Paciente:
    """Solicita los datos de un paciente con validaciones completas."""
    print("\n" + "─" * 50)
    print("📝 INGRESO DE NUEVO PACIENTE")
    print("─" * 50)
    
    id_paciente = generar_id()
    print(f"🆔 ID asignado automáticamente: {id_paciente}")
    
    # Nombre con validación inteligente
    while True:
        nombre = input("Nombre completo (ej: Ana López): ").strip()
        if validar_nombre(nombre):
            # Capitalizar primera letra de cada palabra
            nombre = ' '.join(palabra.capitalize() for palabra in nombre.split())
            break
    
    # Fecha con validación
    print("\n📅 Formato de fecha: AÑO-MES-DÍA (ej: 2025-04-18)")
    while True:
        fecha_cita = input("Fecha de cita: ").strip()
        if validar_fecha(fecha_cita):
            break
    
    # Tipo de procedimiento
    print("\n📋 Tipos de procedimiento:")
    print("  1. Extracción")
    print("  2. Limpieza")
    print("  3. Caries")
    print("  4. Ortodoncia")
    print("  5. Otro")
    
    opcion_proc = obtener_opcion_valida("Seleccione opción (1-5): ", 1, 5)
    
    tipos = {"1": "Extracción", "2": "Limpieza", "3": "Caries", "4": "Ortodoncia", "5": "Otro"}
    tipo_procedimiento = tipos[opcion_proc]
    
    if opcion_proc == "5":
        while True:
            otro_proc = input("Especifique el procedimiento: ").strip()
            if otro_proc and len(otro_proc) >= 2:
                tipo_procedimiento = otro_proc.capitalize()
                break
            print("❌ Debe especificar un procedimiento válido (mínimo 2 caracteres)")
    
    # Prioridad
    print("\n⚠️  Prioridades:")
    print("  1. Urgente (máxima prioridad)")
    print("  2. Normal")
    print("  3. Baja")
    
    opcion_prio = obtener_opcion_valida("Seleccione prioridad (1-3): ", 1, 3)
    
    prioridades = {"1": "Urgente", "2": "Normal", "3": "Baja"}
    prioridad = prioridades[opcion_prio]
    
    print(f"\n✅ Paciente registrado correctamente con ID: {id_paciente}")
    print(f"   Nombre: {nombre}")
    print(f"   Fecha: {fecha_cita}")
    print(f"   Procedimiento: {tipo_procedimiento}")
    print(f"   Prioridad: {prioridad}")
    
    return Paciente(id_paciente, nombre, fecha_cita, tipo_procedimiento, prioridad)

# ------------------------------
# FILTRADO PARA PLAN DE CONTINGENCIA
# ------------------------------
def filtrar_urgentes_extraccion(pacientes: list) -> list:
    """Filtra solo pacientes con Extracción y Urgente."""
    filtrados = []
    for p in pacientes:
        if p.tipo_procedimiento.strip().lower() == "extracción" and p.prioridad.strip().lower() == "urgente":
            p.prioridad = "Urgente"
            filtrados.append(p)
    return filtrados

def ordenar_por_fecha(pacientes: list) -> list:
    """Ordena por fecha más cercana primero."""
    return sorted(pacientes, key=lambda x: x.fecha_cita)

def generar_informe_contingencia(pacientes_ordenados: list) -> None:
    """Informe específico para el plan de contingencia (solo urgentes extracción)."""
    print("\n" + "=" * 75)
    print("📋 PLAN DE CONTINGENCIA - COLA DE EXTRACCIONES URGENTES")
    print("=" * 75)
    print("(Estos pacientes tienen PRIORIDAD ABSOLUTA sobre cualquier otro)\n")
    
    if not pacientes_ordenados:
        print("⚠️  No hay pacientes urgentes con extracción pendiente.\n")
    else:
        print(f"{'N°':<4} {'ID':<8} {'NOMBRE':<25} {'FECHA':<12} {'PRIORIDAD':<10}")
        print("-" * 75)
        for i, p in enumerate(pacientes_ordenados, 1):
            print(f"{i:<4} {p.id_paciente:<8} {p.nombre[:24]:<25} {p.fecha_cita:<12} {p.prioridad:<10}")
        print("\n🔔 Estos pacientes deben ser llamados ANTES que cualquier otro.")
    print("=" * 75)

# ------------------------------
# ORDENAR TODOS LOS PACIENTES POR PRIORIDAD
# ------------------------------
def ordenar_todos_por_prioridad_y_fecha(pacientes: list) -> list:
    """
    Ordena TODOS los pacientes por:
    1. Prioridad: Urgente > Normal > Baja
    2. Dentro de cada prioridad, por fecha más cercana primero
    """
    orden_prioridad = {"Urgente": 1, "Normal": 2, "Baja": 3}
    for p in pacientes:
        p.prioridad = p.prioridad.capitalize()
    return sorted(pacientes, key=lambda x: (orden_prioridad.get(x.prioridad, 99), x.fecha_cita))

def mostrar_cola_completa_ordenada(pacientes: list) -> None:
    """Muestra TODOS los pacientes ordenados por prioridad y fecha."""
    if not pacientes:
        print("\n📭 No hay pacientes pendientes en el sistema.")
        return
    
    cola_ordenada = ordenar_todos_por_prioridad_y_fecha(pacientes)
    
    print("\n" + "=" * 80)
    print("🏥 COLA COMPLETA DE ATENCIÓN (Orden: Urgente → Normal → Baja)")
    print("=" * 80)
    print("Dentro de cada prioridad: fecha más cercana primero\n")
    
    print(f"{'N°':<4} {'ID':<8} {'NOMBRE':<25} {'FECHA':<12} {'PROCEDIMIENTO':<15} {'PRIORIDAD':<10}")
    print("-" * 80)
    
    for i, p in enumerate(cola_ordenada, 1):
        icono = "🔴" if p.prioridad == "Urgente" else ("🟡" if p.prioridad == "Normal" else "🟢")
        print(f"{i:<4} {icono} {p.id_paciente:<6} {p.nombre[:24]:<25} {p.fecha_cita:<12} {p.tipo_procedimiento[:14]:<15} {p.prioridad:<10}")
    
    print("=" * 80)
    print("🔴 = Urgente (primero)  🟡 = Normal (segundo)  🟢 = Baja (tercero)")
    print(f"📌 Total pacientes pendientes: {len(pacientes)}")

# ------------------------------
# SIMULACIÓN DE ATENCIÓN POR LOTES
# ------------------------------
def simular_atencion_por_lotes(pacientes: list, historial: list) -> tuple:
    """
    Atiende SOLO la cantidad de pacientes que el usuario elija.
    Permite atender 1, varios, o todos.
    Después de atender, vuelve al menú principal.
    """
    if not pacientes:
        print("\n⚠️  No hay pacientes pendientes para atender.")
        return pacientes, historial
    
    # Ordenar TODOS los pacientes por prioridad y fecha
    cola_ordenada = ordenar_todos_por_prioridad_y_fecha(pacientes)
    
    print("\n" + "=" * 80)
    print("🏥 SIMULACIÓN DE ATENCIÓN (Por lotes)")
    print("=" * 80)
    print("Orden de atención: 🔴 Urgentes → 🟡 Normales → 🟢 Bajos\n")
    
    # Mostrar los primeros 5 pacientes
    print("📋 PRÓXIMOS PACIENTES EN COLA:")
    print(f"{'N°':<4} {'ID':<8} {'NOMBRE':<25} {'FECHA':<12} {'PRIORIDAD':<10}")
    print("-" * 70)
    
    for i, p in enumerate(cola_ordenada[:5], 1):
        icono = "🔴" if p.prioridad == "Urgente" else ("🟡" if p.prioridad == "Normal" else "🟢")
        print(f"{i:<4} {icono} {p.id_paciente:<6} {p.nombre[:24]:<25} {p.fecha_cita:<12} {p.prioridad:<10}")
    
    if len(cola_ordenada) > 5:
        print(f"\n... y {len(cola_ordenada) - 5} pacientes más.")
    
    print(f"\n📊 Total pacientes en espera: {len(cola_ordenada)}")
    
    urgentes = len([p for p in cola_ordenada if p.prioridad == "Urgente"])
    normales = len([p for p in cola_ordenada if p.prioridad == "Normal"])
    bajos = len([p for p in cola_ordenada if p.prioridad == "Baja"])
    
    print(f"\n📊 Desglose por prioridad:")
    print(f"   🔴 Urgentes: {urgentes}")
    print(f"   🟡 Normales: {normales}")
    print(f"   🟢 Bajos: {bajos}")
    
    print("\n" + "─" * 50)
    print("¿CUÁNTOS PACIENTES DESEA ATENDER?")
    print("─" * 50)
    print("1. Atender SOLO el siguiente paciente")
    print("2. Atender una cantidad específica")
    print("3. Atender TODOS los pacientes")
    print("4. Cancelar y volver al menú")
    
    opcion = input("\nSeleccione una opción (1-4): ").strip()
    
    if opcion == "4":
        print("\n❌ Simulación cancelada. Volviendo al menú principal...")
        return pacientes, historial
    
    cantidad = 0
    if opcion == "1":
        cantidad = 1
    elif opcion == "2":
        while True:
            try:
                cantidad = int(input(f"Ingrese cantidad a atender (1-{len(cola_ordenada)}): ").strip())
                if 1 <= cantidad <= len(cola_ordenada):
                    break
                else:
                    print(f"❌ Cantidad inválida. Debe ser entre 1 y {len(cola_ordenada)}")
            except ValueError:
                print(f"❌ Debe ingresar un número válido")
    elif opcion == "3":
        cantidad = len(cola_ordenada)
    else:
        print("❌ Opción inválida. Volviendo al menú...")
        return pacientes, historial
    
    print(f"\n✅ Se atenderán {cantidad} paciente(s) en el orden establecido.")
    confirmar = input("¿Confirmar atención? (s/n): ").strip().lower()
    
    if confirmar != "s":
        print("❌ Simulación cancelada.")
        return pacientes, historial
    
    print("\n" + "🔄 INICIANDO ATENCIÓN...".center(80))
    
    pacientes_eliminar = []
    
    for i in range(cantidad):
        paciente = cola_ordenada[i]
        
        print(f"\n{'─' * 80}")
        print(f"📅 TURNO #{i+1}")
        print(f"{'─' * 80}")
        
        if paciente.prioridad == "Urgente":
            icono = "🔴"
            prioridad_texto = "URGENTE - PRIORIDAD MÁXIMA"
        elif paciente.prioridad == "Normal":
            icono = "🟡"
            prioridad_texto = "NORMAL"
        else:
            icono = "🟢"
            prioridad_texto = "BAJA"
        
        print(f"{icono} ✅ ATENDIENDO: {paciente.nombre}")
        print(f"   🆔 ID: {paciente.id_paciente}")
        print(f"   📅 Fecha de cita: {paciente.fecha_cita}")
        print(f"   🦷 Procedimiento: {paciente.tipo_procedimiento}")
        print(f"   ⚠️  Prioridad: {prioridad_texto}")
        print(f"   📞 → LLAMAR al paciente ahora mismo.")
        
        # Guardar en historial
        historial.append({
            'id': paciente.id_paciente,
            'nombre': paciente.nombre,
            'fecha_atencion': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_cita': paciente.fecha_cita,
            'procedimiento': paciente.tipo_procedimiento,
            'prioridad': paciente.prioridad
        })
        
        # Marcar para eliminar
        pacientes_eliminar.append(paciente.id_paciente)
    
    # ELIMINAR los pacientes atendidos de la lista principal
    pacientes_actualizados = [p for p in pacientes if p.id_paciente not in pacientes_eliminar]
    
    print("\n" + "=" * 80)
    print("🎉 ¡ATENCIÓN COMPLETADA!")
    print("=" * 80)
    print(f"✅ Total atendidos en esta sesión: {len(pacientes_eliminar)} pacientes")
    print(f"📋 Pacientes restantes en el sistema: {len(pacientes_actualizados)}")
    
    if len(pacientes_actualizados) > 0:
        print("\n💡 Para atender más pacientes, seleccione nuevamente la opción 4.")
    else:
        print("🏆 ¡No hay más pacientes pendientes! Todos han sido atendidos.")
    
    print("=" * 80)
    
    return pacientes_actualizados, historial

# ------------------------------
# FUNCIONES ADICIONALES
# ------------------------------
def mostrar_lista_completa(pacientes: list) -> None:
    """Muestra todos los pacientes registrados sin ordenar."""
    if not pacientes:
        print("\n📭 No hay pacientes registrados aún.")
        return
    
    print("\n" + "=" * 80)
    print("📊 LISTA COMPLETA DE PACIENTES REGISTRADOS")
    print("=" * 80)
    print(f"{'ID':<8} {'NOMBRE':<25} {'FECHA':<12} {'PROCEDIMIENTO':<15} {'PRIORIDAD':<10}")
    print("-" * 80)
    for p in pacientes:
        icono = "🔴" if p.prioridad == "Urgente" else ("🟡" if p.prioridad == "Normal" else "🟢")
        print(f"{icono} {p.id_paciente:<7} {p.nombre[:24]:<25} {p.fecha_cita:<12} {p.tipo_procedimiento[:14]:<15} {p.prioridad:<10}")
    print("=" * 80)
    print(f"📌 Total de pacientes: {len(pacientes)}")

def mostrar_historial(historial: list) -> None:
    """Muestra el historial de pacientes atendidos."""
    if not historial:
        print("\n📭 No hay pacientes atendidos aún.")
        return
    
    print("\n" + "=" * 90)
    print("📜 HISTORIAL DE PACIENTES ATENDIDOS")
    print("=" * 90)
    print(f"{'ID':<8} {'NOMBRE':<25} {'FECHA CITA':<12} {'PROCEDIMIENTO':<15} {'PRIORIDAD':<10} {'FECHA ATENCIÓN':<20}")
    print("-" * 90)
    for h in historial:
        icono = "🔴" if h['prioridad'] == "Urgente" else ("🟡" if h['prioridad'] == "Normal" else "🟢")
        print(f"{icono} {h['id']:<7} {h['nombre'][:24]:<25} {h['fecha_cita']:<12} {h['procedimiento'][:14]:<15} {h['prioridad']:<10} {h['fecha_atencion']:<20}")
    print("=" * 90)
    print(f"📌 Total atendidos: {len(historial)}")

# ------------------------------
# MENÚ PRINCIPAL
# ------------------------------
def mostrar_menu():
    print("\n" + "=" * 55)
    print("   🦷 CONSULTORIO ODONTOLÓGICO - SISTEMA DE ATENCIÓN")
    print("   Versión 7.3 - Validación completa de datos")
    print("=" * 55)
    print("1. 📝 Agregar nuevo paciente (ID automático)")
    print("2. 📋 Ver plan de contingencia (solo urgentes extracción)")
    print("3. 🏥 Ver cola COMPLETA (todos ordenados por prioridad)")
    print("4. 🎯 SIMULAR ATENCIÓN (elige cuántos atender)")
    print("5. 📊 Ver lista completa de pacientes")
    print("6. 📜 Ver historial de atendidos")
    print("7. 🔄 Reiniciar todos los datos")
    print("8. 🚪 Salir")
    print("=" * 55)

# ------------------------------
# EJECUCIÓN PRINCIPAL
# ------------------------------
def main():
    global contador_id, historial_atendidos
    pacientes = []
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-8): ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            nuevo_paciente = ingresar_paciente()
            pacientes.append(nuevo_paciente)
            print(f"\n📊 Total de pacientes registrados: {len(pacientes)}")
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()
        
        elif opcion == "2":
            limpiar_pantalla()
            print("\n🔄 Generando plan de contingencia...")
            urgentes_extraccion = filtrar_urgentes_extraccion(pacientes)
            cola_ordenada = ordenar_por_fecha(urgentes_extraccion)
            generar_informe_contingencia(cola_ordenada)
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()
        
        elif opcion == "3":
            limpiar_pantalla()
            mostrar_cola_completa_ordenada(pacientes)
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()
        
        elif opcion == "4":
            limpiar_pantalla()
            pacientes, historial_atendidos = simular_atencion_por_lotes(pacientes, historial_atendidos)
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()
        
        elif opcion == "5":
            limpiar_pantalla()
            mostrar_lista_completa(pacientes)
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()
        
        elif opcion == "6":
            limpiar_pantalla()
            mostrar_historial(historial_atendidos)
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()
        
        elif opcion == "7":
            limpiar_pantalla()
            confirmar = input("⚠️  ¿Está seguro de que desea eliminar TODOS los datos? (s/n): ").strip().lower()
            if confirmar == "s":
                pacientes = []
                historial_atendidos = []
                contador_id = 0
                print("✅ Todos los datos han sido reiniciados.")
            else:
                print("❌ Operación cancelada.")
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()
        
        elif opcion == "8":
            print("\n👋 Gracias por usar el sistema. ¡Hasta luego!")
            print(f"\n{'=' * 50}")
            print("📊 RESUMEN FINAL")
            print(f"{'=' * 50}")
            print(f"   - Pacientes pendientes: {len(pacientes)}")
            print(f"   - Pacientes atendidos total: {len(historial_atendidos)}")
            
            if len(pacientes) > 0:
                urgentes = len([p for p in pacientes if p.prioridad == "Urgente"])
                normales = len([p for p in pacientes if p.prioridad == "Normal"])
                bajos = len([p for p in pacientes if p.prioridad == "Baja"])
                print(f"\n   Pendientes por prioridad:")
                print(f"     🔴 Urgentes: {urgentes}")
                print(f"     🟡 Normales: {normales}")
                print(f"     🟢 Bajos: {bajos}")
            
            if len(historial_atendidos) > 0:
                atendidos_urgentes = len([h for h in historial_atendidos if h['prioridad'] == "Urgente"])
                atendidos_normales = len([h for h in historial_atendidos if h['prioridad'] == "Normal"])
                atendidos_bajos = len([h for h in historial_atendidos if h['prioridad'] == "Baja"])
                print(f"\n   Atendidos por prioridad:")
                print(f"     🔴 Urgentes: {atendidos_urgentes}")
                print(f"     🟡 Normales: {atendidos_normales}")
                print(f"     🟢 Bajos: {atendidos_bajos}")
            
            print(f"{'=' * 50}")
            break
        
        else:
            print("❌ Opción inválida. Por favor, seleccione 1-8.")
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()

# ------------------------------
# PUNTO DE ENTRADA
# ------------------------------
if __name__ == "__main__":
    main()