#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador de Máquina de Turing Determinista - Programa principal
MM3032 - Lógica Matemática - Parcial 4

Uso:
    python sim_mt.py SPEC.txt -o SALIDA.txt [opciones]

Ejemplo:
    python sim_mt.py mt_acepta.txt -o salida_acepta.txt --conf "u q v"
"""

import argparse
import sys
from parser_mt import parse_spec


def main():
    """Función principal del simulador."""
    parser = argparse.ArgumentParser(
        description='Simulador de MT determinista conforme al PDF de clase.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python sim_mt.py mt_acepta.txt -o salida_acepta.txt
  python sim_mt.py mt_infinito.txt -o salida_infinito.txt --max-steps 100
  python sim_mt.py mt_custom.txt -o salida.txt --conf uqv --allow-S

Formato de especificación:
  Q = {q0, q1, qacc, qrej}
  Sigma = {0,1}
  Gamma = {0,1,⊔}
  blank = ⊔
  q0 = q0
  qaccept = qacc
  qreject = qrej
  
  delta:
  (q0, 0) -> (q1, 0, R)
  (q0, 1) -> (qacc, 1, R)
  
  input = 0101
        """
    )
    
    # Argumentos
    parser.add_argument(
        'spec',
        help='Archivo de especificación (MT + cadena de entrada).'
    )
    
    parser.add_argument(
        '-o', '--out',
        required=True,
        help='Archivo de salida con las configuraciones.'
    )
    
    parser.add_argument(
        '--max-steps',
        type=int,
        default=None,
        help='Cortar tras N pasos (útil para el caso infinito).'
    )
    
    parser.add_argument(
        '--conf',
        choices=['uqv', 'u q v'],
        default='u q v',
        help='Formato de configuración a imprimir (default: "u q v").'
    )
    
    parser.add_argument(
        '--allow-S',
        action='store_true',
        help='Permitir movimiento S (quedarse) - variante extendida.'
    )
    
    parser.add_argument(
        '--no-implicit-reject',
        action='store_true',
        help='NO enviar a q_reject cuando δ no está definida.'
    )
    
    parser.add_argument(
        '--dot',
        metavar='ARCHIVO',
        help='Generar diagrama DOT en el archivo especificado.'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Mostrar información adicional durante la ejecución.'
    )
    
    args = parser.parse_args()
    
    try:
        # Parsear especificación
        if args.verbose:
            print(f"Leyendo especificación desde: {args.spec}")
        
        mt, w = parse_spec(args.spec, allow_S=args.allow_S)
        
        if args.verbose:
            print(f"MT parseada exitosamente:")
            print(f"  Estados: {len(mt.Q)}")
            print(f"  Sigma: {mt.Sigma}")
            print(f"  Transiciones: {len(mt.delta)}")
            print(f"  Entrada: '{w}' (longitud {len(w)})")
            print()
        
        # Simular
        if args.verbose:
            print("Iniciando simulación...")
        
        configs = mt.simulate(
            w,
            max_steps=args.max_steps,
            config_variant=args.conf,
            implicit_reject_on_undef=not args.no_implicit_reject
        )
        
        # Escribir salida
        with open(args.out, 'w', encoding='utf-8') as f:
            for c in configs:
                f.write(c + '\n')
        
        # Determinar resultado
        ultima_config = [c for c in configs if not c.startswith('#')][-1] if configs else ""
        
        if mt.qacc in ultima_config:
            resultado = "ACEPTADO"
            simbolo = "✓"
        elif mt.qrej in ultima_config:
            resultado = "RECHAZADO"
            simbolo = "✗"
        else:
            resultado = "NO TERMINÓ (posible bucle infinito)"
            simbolo = "∞"
        
        # Mostrar resumen
        print(f"Configuraciones escritas en: {args.out}")
        print(f"Total de configuraciones: {len([c for c in configs if not c.startswith('#')])}")
        print(f"Resultado: {resultado} {simbolo}")
        
        if args.verbose:
            print(f"\nPrimera configuración: {configs[0]}")
            if len(configs) > 1:
                print(f"Última configuración:  {configs[-1]}")
        
        # Generar diagrama DOT si se solicita
        if args.dot:
            dot_content = mt.to_dot()
            with open(args.dot, 'w', encoding='utf-8') as f:
                f.write(dot_content)
            print(f"Diagrama DOT generado en: {args.dot}")
            if args.verbose:
                print(f"  Generar PNG: dot -Tpng {args.dot} -o {args.dot.replace('.dot', '.png')}")
        
        return 0
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{args.spec}'", file=sys.stderr)
        return 1
    
    except ValueError as e:
        print(f"Error de especificación: {e}", file=sys.stderr)
        return 1
    
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
