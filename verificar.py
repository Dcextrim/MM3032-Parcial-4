#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación para el simulador de Máquina de Turing
Ejecuta los casos de prueba desde la carpeta MT1/
"""

import subprocess
import sys
import os

def run_test(spec_file, output_file, max_steps=None, expected_result=None):
    """Ejecuta el simulador y verifica el resultado"""
    print(f"\n{'='*60}")
    print(f"Probando: {spec_file}")
    print(f"{'='*60}")
    
    cmd = ['python', 'sim_mt_pdf.py', spec_file, '-o', output_file, '--conf', 'u q v']
    if max_steps:
        cmd.extend(['--max-steps', str(max_steps)])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"ERROR: El simulador falló")
            print(f"STDERR: {result.stderr}")
            return False
        
        print(f"Simulador ejecutado exitosamente")
        
        # Leer salida
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"Configuraciones generadas: {len(lines)}")
        print(f"\nPrimeras líneas:")
        for i, line in enumerate(lines[:5]):
            print(f"  {i+1}. {line.rstrip()}")
        
        if len(lines) > 5:
            print(f"  ...")
            print(f"  {len(lines)}. {lines[-1].rstrip()}")
        
        # Verificar resultado esperado
        if expected_result:
            last_line = lines[-1] if not lines[-1].startswith('#') else lines[-2]
            if expected_result in last_line:
                print(f"\n✓ Resultado correcto: {expected_result} encontrado")
                return True
            else:
                print(f"\nResultado incorrecto: esperaba '{expected_result}' pero no se encontró")
                print(f"   Última línea: {last_line.rstrip()}")
                return False
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Función principal del verificador."""
    print("=" * 60)
    print("VERIFICACIÓN DEL SIMULADOR DE MÁQUINA DE TURING")
    print("MM3032 - Parcial 4")
    print("=" * 60)
    
    # Verificar que exista la carpeta MT1
    if not os.path.exists('MT1'):
        print("\nERROR: No se encuentra la carpeta MT1/")
        print("Asegúrate de estar en el directorio raíz del proyecto.")
        return 1
    
    # Crear carpeta MT1 para salidas si no existe
    os.makedirs('MT1', exist_ok=True)
    
    tests = [
        {
            'spec': 'MT1/mt_acepta.txt',
            'output': 'MT1/salida_acepta.txt',
            'max_steps': None,
            'expected': 'qacc',
            'description': 'Caso de ACEPTACIÓN (input=1) - MT1'
        },
        {
            'spec': 'MT1/mt_rechaza.txt',
            'output': 'MT1/salida_rechaza.txt',
            'max_steps': None,
            'expected': 'qrej',
            'description': 'Caso de RECHAZO (input=01) - MT1'
        },
        {
            'spec': 'MT1/mt_infinito.txt',
            'output': 'MT1/salida_infinito.txt',
            'max_steps': 200,
            'expected': 'qinf',
            'description': 'Caso INFINITO (input=00, max 200 pasos) - MT1'
        }
    ]
    
    results = []
    for test in tests:
        print(f"\n{test['description']}")
        success = run_test(
            test['spec'],
            test['output'],
            test['max_steps'],
            test['expected']
        )
        results.append(success)
    
    print("\n" + "=" * 60)
    print("RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    for i, (test, success) in enumerate(zip(tests, results)):
        status = "✓ PASS" if success else "FAIL"
        print(f"{status} - {test['description']}")
    
    total = len(results)
    passed = sum(results)
    
    print(f"\nResultado final: {passed}/{total} pruebas pasaron")
    
    if all(results):
        print("\n¡Todos los tests pasaron correctamente!")
        print("\nArchivos generados en MT1/:")
        print("  - salida_acepta.txt")
        print("  - salida_rechaza.txt")
        print("  - salida_infinito.txt")
        print("\n✓ Listo para entregar!")
        return 0
    else:
        print("\n⚠️ Algunos tests fallaron. Revisa los errores arriba.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
