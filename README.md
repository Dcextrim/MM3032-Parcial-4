# Simulador de Máquina de Turing Determinista (MM3032 - Parcial 4)

## Estructura del proyecto

```
MM3032-Parcial-4/
├── maquina_turing.py    # Clase MaquinaTuring (lógica de simulación)
├── parser_mt.py         # Parser de especificaciones
├── sim_mt.py            # Programa principal con CLI
├── sim_mt_pdf.py        # Menú interactivo
│
├── MT1/                 # Máquinas de Turing simples
│   ├── mt_acepta.txt    # Caso que acepta (input = 1)
│   ├── mt_rechaza.txt   # Caso que rechaza (input = 01)
│   ├── mt_infinito.txt  # Caso infinito (input = 00)
│   └── mt_diagrama.dot  # Diagrama de estados
│
└── MT2/                 # Máquinas de Turing complejas
    ├── mt_suma.txt              # Suma en unario (111#11 → 11111)
    ├── mt_suma.dot
    ├── mt_palindromo.txt        # Verificador de palíndromos (acepta)
    ├── mt_palindromo.dot
    ├── mt_palindromo_rechaza.txt # Verificador de palíndromos (rechaza)
    ├── mt_palindromo_rechaza.dot
    ├── mt_mult2.txt             # Multiplicación por 2 en binario
    └── mt_mult2.dot
```

## Contenido del proyecto

**CÓDIGO FUENTE (4 archivos):**
- `maquina_turing.py` — Clase MaquinaTuring con la lógica de simulación
- `parser_mt.py` — Parser de archivos de especificación
- `sim_mt.py` — Programa principal con interfaz CLI
- `sim_mt_pdf.py` — Menú interactivo para ejecutar MTs

**MT1/ - Máquinas Simples (3 MTs):**
- `mt_acepta.txt` — Acepta '1'
- `mt_rechaza.txt` — Rechaza '01'
- `mt_infinito.txt` — Bucle infinito con '00'
- `mt_diagrama.dot` — Diagrama de estados

**MT2/ - Máquinas Complejas (4 MTs):**
- `mt_suma.txt` + `mt_suma.dot` — Suma en unario (111#11 → 11111)
- `mt_palindromo.txt` + `mt_palindromo.dot` — Verifica palíndromos (aba)
- `mt_palindromo_rechaza.txt` + `mt_palindromo_rechaza.dot` — Rechaza no-palíndromos (abb)
- `mt_mult2.txt` + `mt_mult2.dot` — Multiplica por 2 en binario (101 → 1010)

**SALIDAS:** Los archivos `salida_*.txt` se generan automáticamente al ejecutar las máquinas

## Marco teórico

Este simulador implementa una Máquina de Turing determinista según la notación de clase:
- M = (Q, Σ, Γ, δ, q0, q_accept, q_reject)
- Σ ⊆ Γ, ⊔ ∈ Γ y ⊔ ∉ Σ (⊔ es el blanco)
- δ: Q × Γ → Q × Γ × {L, R} (movimientos: L=izquierda, R=derecha)
- Configuración: u q v (q incrustado; la cabeza lee el primer símbolo de v)
- Cinta con tope a la izquierda (índice 0); si δ indica L en posición 0, la cabeza NO se mueve
- Por la derecha, la cinta se extiende infinitamente con blancos

## Descripción de las MTs implementadas

### MT1 - Máquina simple de clasificación
Acepta cadenas que empiezan con '1', rechaza cadenas que empiezan con '01' o '⊔', 
y entra en bucle infinito si empiezan con '00'.

**Estados:** Q = {q0, q1, qacc, qrej, qinf}  
**Alfabeto de entrada:** Σ = {0, 1}  
**Alfabeto de cinta:** Γ = {0, 1, ⊔}

**Transiciones:**
- (q0, 1) → (qacc, 1, R)  — acepta si primer símbolo es 1
- (q0, 0) → (q1, 0, R)    — lee 0, va a q1
- (q0, ⊔) → (qrej, ⊔, R)  — rechaza cadena vacía
- (q1, 0) → (qinf, 0, R)  — segundo 0: entra a bucle
- (q1, 1) → (qrej, 1, R)  — segundo 1: rechaza
- (q1, ⊔) → (qrej, ⊔, R)  — solo un 0: rechaza
- (qinf, *) → (qinf, *, R) — bucle infinito para cualquier símbolo

### MT2 - Máquinas complejas

**1. Suma en unario** (`mt_suma.txt`)
- Entrada: `1^n#1^m` → Salida: `1^(n+m)`
- Ejemplo: `111#11` → `11111` (3 + 2 = 5)
- Estados: 6, Transiciones: 10, Pasos: ~15

**2. Verificador de palíndromos** (`mt_palindromo.txt`, `mt_palindromo_rechaza.txt`)
- Entrada: cadenas en `{a,b}*`
- Acepta si w = w^R (palíndromo)
- Ejemplos: `aba` ✓, `abba` ✓, `abb` ✗
- Estados: 8, Transiciones: 24, Pasos: ~12

**3. Multiplicación por 2** (`mt_mult2.txt`)
- Entrada: número binario
- Salida: número × 2 (shift left + añadir 0)
- Ejemplo: `101` → `1010` (5 × 2 = 10)
- Estados: 6, Transiciones: 13, Pasos: ~16

Ver `MT2/README.md` para detalles completos de cada máquina.

## Cómo ejecutar

### Requisitos
- Python 3.x (sin dependencias externas)

### Opción 1: Menú interactivo (recomendado)

```bash
python sim_mt_pdf.py
```

Muestra un menú con todas las máquinas disponibles. Selecciona el número y automáticamente:
- Ejecuta la máquina
- Genera el archivo de salida `salida_*.txt`
- Genera el diagrama `.dot`

### Opción 2: Línea de comandos

**Sintaxis:**
```bash
python sim_mt.py <especificacion.txt> -o <salida.txt> [--dot <diagrama.dot>] [--max-steps N]
```

**Ejemplos:**
```bash
# MT1
python sim_mt.py MT1/mt_acepta.txt -o MT1/salida_acepta.txt --dot MT1/mt_diagrama.dot
python sim_mt.py MT1/mt_infinito.txt -o MT1/salida_infinito.txt --max-steps 200

# MT2
python sim_mt.py MT2/mt_suma.txt -o MT2/salida_suma.txt --dot MT2/mt_suma.dot
python sim_mt.py MT2/mt_palindromo.txt -o MT2/salida_palindromo.txt --dot MT2/mt_palindromo.dot
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

## Generar diagramas visuales

Para generar una imagen PNG del diagrama de estados (requiere Graphviz):

```bash
# MT1
dot -Tpng MT1/mt_diagrama.dot -o MT1/mt_diagrama.png

# MT2
dot -Tpng MT2/mt_suma.dot -o MT2/mt_suma.png
dot -Tpng MT2/mt_palindromo.dot -o MT2/mt_palindromo.png
dot -Tpng MT2/mt_mult2.dot -o MT2/mt_mult2.png
```

Los diagramas muestran solo los estados que realmente tienen transiciones (sin estados sueltos).

## Verificación de resultados

### MT1 - Casos simples

**Caso de aceptación** (mt_acepta.txt con input = 1)
```
 q0 1
1 qacc ⊔
```
**Resultado: ACEPTADO** ✓

**Caso de rechazo** (mt_rechaza.txt con input = 01)
```
 q0 01
0 q1 1
01 qrej ⊔
```
**Resultado: RECHAZADO** ✓

**Caso infinito** (mt_infinito.txt con input = 00)
```
 q0 00
0 q1 0
00 qinf ⊔
00⊔ qinf ⊔
00⊔⊔ qinf ⊔
...
[Aviso] Se alcanzó el límite de pasos (200). Posible ciclo infinito.
```
**Resultado: CICLO INFINITO** ✓

### MT2 - Casos complejos

Ver archivos `MT2/salida_*.txt` para las trazas completas de ejecución.

**Suma:** 111#11 → 11111 (15 pasos)  
**Palíndromo acepta:** aba → ACEPTA (12 pasos)  
**Palíndromo rechaza:** abb → RECHAZA (6 pasos)  
**Multiplicación x2:** 101 → 1010 (16 pasos)

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
