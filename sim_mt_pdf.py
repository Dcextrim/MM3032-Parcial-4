#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menú interactivo para ejecutar Máquinas de Turing
"""

import os
import subprocess
from pathlib import Path

def listar_maquinas():
    """Lista todas las máquinas disponibles en MT1/ y MT2/"""
    maquinas = {}
    
    # Buscar en MT1/
    mt1_dir = Path("MT1")
    if mt1_dir.exists():
        for archivo in sorted(mt1_dir.glob("mt_*.txt")):
            nombre = archivo.stem
            maquinas[nombre] = str(archivo)
    
    # Buscar en MT2/
    mt2_dir = Path("MT2")
    if mt2_dir.exists():
        for archivo in sorted(mt2_dir.glob("mt_*.txt")):
            nombre = archivo.stem
            maquinas[nombre] = str(archivo)
    
    return maquinas

def mostrar_menu(maquinas):
    """Muestra el menú de máquinas disponibles"""
    print("\n" + "="*60)
    print("  SIMULADOR DE MÁQUINAS DE TURING - MM3032 Parcial 4")
    print("="*60)
    print("\nMáquinas disponibles:\n")
    
    items = list(maquinas.items())
    for i, (nombre, ruta) in enumerate(items, 1):
        # Extraer carpeta y descripción básica
        carpeta = Path(ruta).parent.name
        print(f"  {i}. [{carpeta}] {nombre}")
    
    print(f"\n  0. Salir")
    print("="*60)
    
    return items

def ejecutar_maquina(ruta_spec, max_steps=200):
    """Ejecuta una máquina de Turing"""
    ruta = Path(ruta_spec)
    carpeta = ruta.parent
    nombre = ruta.stem
    
    # Generar nombres de salida
    salida_txt = carpeta / f"salida_{nombre.replace('mt_', '')}.txt"
    salida_dot = carpeta / f"{nombre}.dot"
    
    print(f"\n{'='*60}")
    print(f"Ejecutando: {ruta}")
    print(f"{'='*60}\n")
    
    # Comando para ejecutar
    cmd = [
        "python", "sim_mt.py", 
        str(ruta),
        "-o", str(salida_txt),
        "--dot", str(salida_dot),
        "--max-steps", str(max_steps)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        # Mostrar salida
        print(result.stdout)
        if result.stderr:
            # Filtrar errores de encoding que no son críticos
            stderr_lines = [line for line in result.stderr.split('\n') 
                           if 'UnicodeDecodeError' not in line and 'Thread' not in line and 'Traceback' not in line]
            if stderr_lines:
                print("Errores:", '\n'.join(stderr_lines))
        
        print(f"\n{'='*60}")
        print(f"[OK] Salida guardada en: {salida_txt}")
        print(f"[OK] Diagrama guardado en: {salida_dot}")
        print(f"{'='*60}")
        
        return True
    except Exception as e:
        print(f"\n[X] Error al ejecutar: {e}")
        return False

def main():
    """Función principal del menú"""
    while True:
        # Listar máquinas disponibles
        maquinas = listar_maquinas()
        
        if not maquinas:
            print("\n[X] No se encontraron maquinas de Turing en MT1/ o MT2/")
            return
        
        # Mostrar menú
        items = mostrar_menu(maquinas)
        
        # Leer opción
        try:
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "0":
                print("\n¡Hasta luego!\n")
                break
            
            num = int(opcion)
            if 1 <= num <= len(items):
                nombre, ruta = items[num - 1]
                ejecutar_maquina(ruta)
                
                # Preguntar si quiere continuar
                input("\nPresione ENTER para continuar...")
            else:
                print(f"\n[X] Opcion invalida. Debe estar entre 0 y {len(items)}")
                input("\nPresione ENTER para continuar...")
        
        except ValueError:
            print("\n[X] Por favor ingrese un numero valido")
            input("\nPresione ENTER para continuar...")
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!\n")
            break

if __name__ == '__main__':
    main()
