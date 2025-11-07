#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser de especificaciones de Máquina de Turing.
Lee archivos .txt con el formato de clase y construye la MT.
"""

import re
from typing import Set, Tuple
from maquina_turing import MaquinaTuring, Delta, State, Symbol

# Expresiones regulares para parsing
_keyval = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$')
_set = re.compile(r'^\{\s*(.*?)\s*\}$')
_trans = re.compile(r'^\s*\(\s*([A-Za-z0-9_]+)\s*,\s*(.)\s*\)\s*->\s*\(\s*([A-Za-z0-9_]+)\s*,\s*(.)\s*,\s*([LRS])\s*\)\s*$')


def parse_set(s: str) -> Set[str]:
    """
    Parse un conjunto en formato {a, b, c}.
    
    Args:
        s: String con el conjunto
        
    Returns:
        Set con los elementos
        
    Raises:
        ValueError: Si el formato es inválido
    """
    m = _set.match(s)
    if not m:
        raise ValueError(f"Conjunto mal formado: {s}")
    
    body = m.group(1).strip()
    if not body:
        return set()
    
    return {p.strip() for p in body.split(',')}


def parse_spec(path: str, allow_S: bool = False) -> Tuple[MaquinaTuring, str]:
    """
    Parse un archivo de especificación de MT.
    
    Formato esperado:
    ```
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
    ```
    
    Args:
        path: Ruta al archivo de especificación
        allow_S: Si True, permite movimiento S (quedarse)
        
    Returns:
        Tupla (MaquinaTuring, cadena_entrada)
        
    Raises:
        ValueError: Si hay errores en la especificación
    """
    # Variables para almacenar la especificación
    Q = Sigma = Gamma = None
    blank = None
    q0 = qacc = qrej = None
    delta: Delta = {}
    input_w = ''
    in_delta = False

    # Leer archivo
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parsear línea por línea
    for line_num, raw in enumerate(lines, 1):
        line = raw.strip()
        
        # Ignorar comentarios y líneas vacías
        if not line or line.startswith('#'):
            continue
        
        # Detectar inicio de sección delta
        if line.lower().startswith('delta'):
            in_delta = True
            continue
        
        # Parsear transiciones
        if in_delta:
            m = _trans.match(line)
            if m:
                # Es una transición válida
                q, a, qp, b, M = m.groups()
                
                # Validar movimiento S
                if not allow_S and M == 'S':
                    raise ValueError(
                        f"Línea {line_num}: Este archivo usa 'S' pero la variante "
                        f"base solo permite L/R (use --allow-S si es necesario)."
                    )
                
                # Verificar determinismo
                if (q, a) in delta:
                    raise ValueError(
                        f"Línea {line_num}: Determinismo violado, "
                        f"ya existe δ({q},{a})."
                    )
                
                delta[(q, a)] = (qp, b, M)
                continue
            else:
                # No es una transición, salir del modo delta
                in_delta = False
        
        # Parsear definiciones (Q = {...}, q0 = ..., etc.)
        m = _keyval.match(line)
        if not m:
            raise ValueError(f"Línea {line_num}: Línea no reconocida: '{line}'")
        
        key, val = m.groups()
        kl = key.strip().lower()
        
        try:
            if kl == 'q':
                Q = parse_set(val)
            elif kl == 'sigma':
                Sigma = parse_set(val)
            elif kl == 'gamma':
                Gamma = parse_set(val)
            elif kl in ('blank', 'blanco'):
                blank = val.strip()
                if len(blank) != 1:
                    raise ValueError(
                        "El símbolo blanco debe tener un solo carácter (ej: '⊔')."
                    )
            elif kl in ('q0', 'inicial', 'estado_inicial'):
                q0 = val.strip()
            elif kl in ('qaccept', 'q_accept', 'aceptacion', 'qacc'):
                qacc = val.strip()
            elif kl in ('qreject', 'q_reject', 'rechazo', 'qrej'):
                qrej = val.strip()
            elif kl in ('input', 'entrada', 'w'):
                input_w = val.strip()
            else:
                raise ValueError(f"Clave desconocida: '{key}'")
        except ValueError as e:
            raise ValueError(f"Línea {line_num}: {e}")

    # Validar que todos los campos obligatorios estén presentes
    required = [
        ('Q', Q),
        ('Sigma', Sigma),
        ('Gamma', Gamma),
        ('blank', blank),
        ('q0', q0),
        ('qaccept', qacc),
        ('qreject', qrej)
    ]
    
    missing = [name for name, value in required if value is None]
    if missing:
        raise ValueError(f"Faltan especificar los siguientes campos: {', '.join(missing)}")

    # Crear la Máquina de Turing
    mt = MaquinaTuring(
        Q=Q,
        Sigma=Sigma,
        Gamma=Gamma,
        blank=blank,
        q0=q0,
        qacc=qacc,
        qrej=qrej,
        delta=delta,
        allow_S=allow_S
    )
    
    return mt, input_w
