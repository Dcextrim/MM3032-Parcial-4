

# Simulador de Máquina de Turing Determinista (MM3032 - Parcial 4)

## Estructura del proyecto

```
MM3032-Parcial-4/
├── maquina_turing.py    # Clase MaquinaTuring (lógica de simulación)
├── parser_mt.py         # Parser de especificaciones
├── sim_mt.py            # Programa principal con CLI
├── sim_mt_pdf.py        # Wrapper de compatibilidad
│
├── MT1/                 # Máquina de Turing #1
│   ├── mt_acepta.txt    # Caso que acepta (input = 1)
│   ├── mt_rechaza.txt   # Caso que rechaza (input = 01)
│   ├── mt_infinito.txt  # Caso infinito (input = 00)
│   └── mt_diagrama.dot  # Diagrama de estados
│
└── README.md            # Este archivo
```

**CÓDIGO FUENTE (4 archivos):**
- `maquina_turing.py` — Clase MaquinaTuring con la lógica de simulación
- `parser_mt.py` — Parser de archivos de especificación
- `sim_mt.py` — Programa principal con interfaz CLI
- `sim_mt_pdf.py` — Wrapper para compatibilidad

**ESPECIFICACIONES - MT1/ (4 archivos):**
- `mt_acepta.txt` — Especificación + entrada que **acepta** (input = 1)
- `mt_rechaza.txt` — Especificación + entrada que **rechaza** (input = 01)
- `mt_infinito.txt` — Especificación + entrada que entra en **ciclo infinito** (input = 00)
- `mt_diagrama.dot` — Diagrama de estados en formato Graphviz DOT

**SALIDAS (generadas automáticamente al ejecutar):**
- Las salidas se generan en el mismo directorio donde ejecutes el comando
- O puedes especificar la ruta completa con `-o`

**NOTA:** El código está organizado en módulos para mejor mantenibilidad.
Las especificaciones están en carpetas (MT1/, MT2/, etc.) para probar diferentes MTs.

## Marco teórico

Este simulador implementa una Máquina de Turing determinista según la notación de clase:
- M = (Q, Σ, Γ, δ, q0, q_accept, q_reject)
- Σ ⊆ Γ, ⊔ ∈ Γ y ⊔ ∉ Σ (⊔ es el blanco)
- δ: Q × Γ → Q × Γ × {L, R} (movimientos: L=izquierda, R=derecha)
- Configuración: u q v (q incrustado; la cabeza lee el primer símbolo de v)
- Cinta con tope a la izquierda (índice 0); si δ indica L en posición 0, la cabeza NO se mueve
- Por la derecha, la cinta se extiende infinitamente con blancos

## Descripción de la MT implementada

La máquina acepta cadenas que empiezan con '1', rechaza cadenas que empiezan con '01' o '⊔', 
y entra en bucle infinito si empiezan con '00'.

Estados: Q = {q0, q1, qacc, qrej, qinf}
Alfabeto de entrada: Σ = {0, 1}
Alfabeto de cinta: Γ = {0, 1, ⊔}

Transiciones:
- (q0, 1) -> (qacc, 1, R)  [acepta si primer símbolo es 1]
- (q0, 0) -> (q1, 0, R)    [lee 0, va a q1]
- (q0, ⊔) -> (qrej, ⊔, R)  [rechaza cadena vacía]
- (q1, 0) -> (qinf, 0, R)  [segundo 0: entra a bucle]
- (q1, 1) -> (qrej, 1, R)  [segundo 1: rechaza]
- (q1, ⊔) -> (qrej, ⊔, R)  [solo un 0: rechaza]
- (qinf, *) -> (qinf, *, R) [bucle infinito para cualquier símbolo]

## Cómo ejecutar

### Requisitos
- Python 3.x (sin dependencias externas)

### Comandos para generar las salidas

```bash
# Caso de aceptación (input = 1) - MT1
python sim_mt_pdf.py MT1/mt_acepta.txt -o MT1/salida_acepta.txt --conf "u q v"

# Caso de rechazo (input = 01) - MT1
python sim_mt_pdf.py MT1/mt_rechaza.txt -o MT1/salida_rechaza.txt --conf "u q v"

# Caso infinito (input = 00, limitado a 200 pasos) - MT1
python sim_mt_pdf.py MT1/mt_infinito.txt -o MT1/salida_infinito.txt --conf "u q v" --max-steps 200
```

**Para otras Máquinas de Turing:**
```bash
# Si creas MT2/, MT3/, etc., solo cambia la ruta:
python sim_mt_pdf.py MT2/mi_especificacion.txt -o MT2/salida.txt --conf "u q v"
```

### Opciones del simulador

```
Uso: python sim_mt_pdf.py SPEC.txt -o SALIDA.txt [opciones]

Opciones:
  -o, --out ARCHIVO       Archivo de salida (requerido)
  --conf FORMATO          Formato de configuración: "u q v" (con espacios) o "uqv" (compacto)
                          Por defecto: "u q v"
  --max-steps N           Límite de pasos (útil para evitar bucles infinitos)
  --allow-S               Permitir movimiento S (quedarse) - variante extendida
  --no-implicit-reject    No rechazar implícitamente cuando δ no está definida
```

## Formato del archivo de especificación

```
# Comentarios comienzan con #
Q = {q0, q1, qacc, qrej, qinf}
Sigma = {0,1}
Gamma = {0,1,⊔}
blank = ⊔
q0 = q0
qaccept = qacc
qreject = qrej

delta:
(q0, 1) -> (qacc, 1, R)
(q0, 0) -> (q1, 0, R)
...

input = 00
```

### Validaciones automáticas
- q0, qaccept, qreject ∈ Q
- Σ ⊆ Γ
- blank ∈ Γ y blank ∉ Σ
- Determinismo de δ (una única regla por (q, a))
- Símbolos y estados en δ deben existir en Γ y Q

### Comportamiento en ejecución
- Si no hay transición δ(q, a) definida, el simulador envía a qreject (rechazo implícito)
- La ejecución para al llegar a qaccept o qreject
- Con --max-steps N, se detiene después de N pasos y muestra un aviso

## Generar diagrama visual

Para generar una imagen PNG del diagrama de estados (requiere Graphviz):

```bash
dot -Tpng mt_diagrama.dot -o mt_diagrama.png
```

## Verificación de resultados

### Caso de aceptación (mt_acepta.txt con input = 1)
Configuraciones esperadas:
1. ` q0 1` (inicial: cabeza en '1')
2. `1 qacc ⊔` (acepta: escribió '1', movió derecha a blanco)

**Resultado: ACEPTADO** ✓

### Caso de rechazo (mt_rechaza.txt con input = 01)
Configuraciones esperadas:
1. ` q0 01` (inicial)
2. `0 q1 1` (leyó '0', fue a q1)
3. `01 qrej ⊔` (leyó '1' en q1, rechaza)

**Resultado: RECHAZADO** ✓

### Caso infinito (mt_infinito.txt con input = 00)
Configuraciones esperadas:
1. ` q0 00` (inicial)
2. `0 q1 0` (leyó primer '0')
3. `00 qinf ⊔` (leyó segundo '0', entra a bucle)
4. `00⊔ qinf ⊔` (bucle: sigue moviendose derecha)
5. ... (continúa indefinidamente)
N. `# [Aviso] Se alcanzó el límite de pasos (200). Posible ciclo infinito.`

**Resultado: CICLO INFINITO** ✓

## Notación de configuraciones

Formato `u q v`:
- `u` = contenido de la cinta a la izquierda de la cabeza
- `q` = estado actual (incrustado)
- `v` = contenido desde la posición de la cabeza hacia la derecha

La cabeza siempre lee el **primer símbolo de v**.

Ejemplo: `01 q2 10⊔` significa:
- Cinta: ...⊔010⊔...
- Estado: q2
- Cabeza en posición 2 (leyendo '1')
