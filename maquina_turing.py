#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase MaquinaTuring - Representa y simula una Máquina de Turing determinista.
"""

from collections import defaultdict
from typing import Dict, Tuple, Set, List, Optional

Move = str  # 'L' | 'R' | 'S'
State = str
Symbol = str
Delta = Dict[Tuple[State, Symbol], Tuple[State, Symbol, Move]]


class MaquinaTuring:
    """
    Máquina de Turing determinista según notación de clase.
    M = (Q, Σ, Γ, δ, q0, q_accept, q_reject)
    """
    
    def __init__(self,
                 Q: Set[State],
                 Sigma: Set[Symbol],
                 Gamma: Set[Symbol],
                 blank: Symbol,
                 q0: State,
                 qacc: State,
                 qrej: State,
                 delta: Delta,
                 allow_S: bool = False,
                 left_boundary: int = 0):
        """
        Inicializa la Máquina de Turing.
        
        Args:
            Q: Conjunto de estados
            Sigma: Alfabeto de entrada
            Gamma: Alfabeto de la cinta
            blank: Símbolo blanco
            q0: Estado inicial
            qacc: Estado de aceptación
            qrej: Estado de rechazo
            delta: Función de transición
            allow_S: Permitir movimiento S (quedarse)
            left_boundary: Índice mínimo de la cinta (tope izquierdo)
        """
        self.Q = Q
        self.Sigma = Sigma
        self.Gamma = Gamma
        self.blank = blank
        self.q0 = q0
        self.qacc = qacc
        self.qrej = qrej
        self.delta = delta
        self.allow_S = allow_S
        self.left_boundary = left_boundary
        self.validate()

    def validate(self):
        """Valida la especificación de la MT."""
        # Validar estados especiales
        if self.q0 not in self.Q:
            raise ValueError(f"Estado inicial {self.q0} no está en Q.")
        if self.qacc not in self.Q:
            raise ValueError(f"Estado de aceptación {self.qacc} no está en Q.")
        if self.qrej not in self.Q:
            raise ValueError(f"Estado de rechazo {self.qrej} no está en Q.")
        
        # Validar alfabetos
        if self.blank not in self.Gamma:
            raise ValueError(f"Símbolo blanco '{self.blank}' no está en Gamma.")
        if self.blank in self.Sigma:
            raise ValueError(f"El símbolo blanco '{self.blank}' NO debe pertenecer a Sigma.")
        if not self.Sigma.issubset(self.Gamma):
            raise ValueError("Sigma debe ser subconjunto de Gamma.")

        # Validar transiciones
        allowed_moves = {'L', 'R'} | ({'S'} if self.allow_S else set())
        for (q, a), (qp, b, m) in self.delta.items():
            if q not in self.Q or qp not in self.Q:
                raise ValueError(f"Estados en δ({q},{a}) deben pertenecer a Q.")
            if a not in self.Gamma or b not in self.Gamma:
                raise ValueError(f"Símbolos en δ({q},{a}) deben pertenecer a Gamma.")
            if m not in allowed_moves:
                raise ValueError(f"Movimiento inválido '{m}'. Permitidos: {sorted(allowed_moves)}")

    def simulate(self,
                 w: str,
                 max_steps: Optional[int] = None,
                 config_variant: str = 'u q v',
                 implicit_reject_on_undef: bool = True) -> List[str]:
        """
        Simula la ejecución de la MT sobre la cadena w.
        
        Args:
            w: Cadena de entrada
            max_steps: Límite de pasos (None = sin límite)
            config_variant: Formato de configuración ('u q v' o 'uqv')
            implicit_reject_on_undef: Si True, rechaza cuando no hay transición
            
        Returns:
            Lista de configuraciones desde la inicial hasta el paro
        """
        # Inicializar cinta con blanco por defecto
        tape = defaultdict(lambda: self.blank)
        head = self.left_boundary
        
        # Escribir la palabra de entrada
        for i, ch in enumerate(w):
            if ch not in self.Sigma:
                raise ValueError(f"Símbolo de entrada '{ch}' no pertenece a Sigma.")
            tape[i] = ch
        
        q = self.q0
        configs: List[str] = []
        configs.append(self._format_config(tape, q, head, config_variant))

        steps = 0
        while True:
            # Verificar si alcanzamos un estado de paro
            if q == self.qacc or q == self.qrej:
                break
            
            # Leer símbolo actual
            a = tape[head]
            key = (q, a)
            
            # Buscar transición
            if key not in self.delta:
                if implicit_reject_on_undef:
                    q = self.qrej
                    configs.append(self._format_config(tape, q, head, config_variant))
                break
            
            # Aplicar transición
            qp, b, m = self.delta[key]
            tape[head] = b
            
            # Mover cabeza
            if m == 'L':
                if head > self.left_boundary:
                    head -= 1
                # Si head == left_boundary, no se mueve (tope izquierdo)
            elif m == 'R':
                head += 1
            elif m == 'S':
                if not self.allow_S:
                    raise RuntimeError("Movimiento 'S' no permitido.")
                # No mover
            else:
                raise RuntimeError(f"Movimiento inválido '{m}' en ejecución.")
            
            # Cambiar estado
            q = qp
            configs.append(self._format_config(tape, q, head, config_variant))

            steps += 1
            if max_steps is not None and steps >= max_steps:
                configs.append(f"# [Aviso] Se alcanzó el límite de pasos ({max_steps}). Posible ciclo infinito.")
                break
        
        return configs

    def _format_config(self, tape: defaultdict, q: State, head: int, variant: str) -> str:
        """
        Formatea una configuración en notación u q v.
        
        Args:
            tape: Cinta actual
            q: Estado actual
            head: Posición de la cabeza
            variant: 'u q v' (con espacios) o 'uqv' (compacto)
            
        Returns:
            Configuración formateada
        """
        L, R = self._window_bounds(tape, head)
        
        # Parte izquierda (antes de la cabeza)
        u = ''.join(tape[i] for i in range(L, head))
        
        # Parte derecha (desde la cabeza)
        v = ''.join(tape[i] for i in range(head, R + 1))
        
        if variant == 'u q v':
            return f"{u} {q} {v}"
        elif variant == 'uqv':
            return f"{u}{q}{v}"
        else:
            raise ValueError("config_variant debe ser 'uqv' o 'u q v'")

    def _window_bounds(self, tape: defaultdict, head: int) -> Tuple[int, int]:
        """
        Determina el rango [L, R] de la cinta a mostrar.
        Incluye celdas no-blanco y la posición de la cabeza.
        """
        nonblank = [i for i, s in tape.items() if s != self.blank]
        if nonblank:
            L = min(min(nonblank), head)
            R = max(max(nonblank), head)
        else:
            L = R = head
        
        # No permitir L < left_boundary
        L = min(L, self.left_boundary)
        return L, R

    def to_dot(self) -> str:
        """
        Genera representación en formato Graphviz DOT.
        
        Returns:
            String con el código DOT del diagrama
        """
        lines = []
        lines.append("digraph MT {")
        lines.append("  rankdir=LR;")
        lines.append('  node [shape = circle, fontname="Helvetica"];')
        lines.append("")
        
        # Determinar estados que realmente se usan
        used_states = {self.q0}  # Siempre incluir estado inicial
        for (q, _), (qp, _, _) in self.delta.items():
            used_states.add(q)
            used_states.add(qp)
        
        # Declarar solo estados usados
        for state in sorted(used_states):
            if state == self.qacc or state == self.qrej:
                lines.append(f'  {state} [shape=doublecircle, label="{state}"];')
            else:
                lines.append(f'  {state} [label="{state}"];')
        
        lines.append("")
        lines.append(f'  start [shape=point]; start -> {self.q0};')
        lines.append("")
        
        # Agrupar transiciones por (estado_origen, estado_destino)
        transitions = defaultdict(list)
        for (q, a), (qp, b, m) in sorted(self.delta.items()):
            label = f"{a}→{b},{m}"
            transitions[(q, qp)].append(label)
        
        # Generar aristas
        for (q, qp), labels in sorted(transitions.items()):
            label_str = "\\n".join(labels)
            lines.append(f'  {q} -> {qp} [label="{label_str}"];')
        
        lines.append("}")
        return "\n".join(lines)
