# Simulador de Máquina de Turing Determinista
## MM3032 - Lógica Matemática - Parcial 4

---

## 📋 **Descripción del Proyecto**

Simulador completo de Máquina de Turing Determinista que sigue exactamente la notación vista en clase. El proyecto incluye múltiples máquinas de ejemplo, desde casos simples hasta algoritmos complejos como verificadores de palíndromos.

---

## 🗂️ **Estructura del Proyecto**

```
MM3032-Parcial-4/
│
├── maquina_turing.py      # Clase principal MaquinaTuring
├── parser_mt.py           # Parser de especificaciones
├── sim_mt.py              # Interfaz CLI
├── sim_mt_pdf.py          # Menú interactivo
│
├── MT1/                   # Máquinas simples
│   ├── mt_acepta.txt
│   ├── mt_rechaza.txt
│   ├── mt_infinito.txt
│   └── mt_diagrama.dot
│
└── MT2/                   # Máquinas complejas
    ├── mt_suma.txt
    ├── mt_palindromo.txt
    ├── mt_palindromo_rechaza.txt
    ├── mt_palindromo_infinito.txt
    ├── mt_mult2.txt
    └── *.dot (diagramas)
```

---

## 🚀 **Uso**

### **Opción 1: Menú Interactivo**
```bash
python sim_mt_pdf.py
```
Muestra un menú con todas las máquinas disponibles en `MT1/` y `MT2/`.

### **Opción 2: Línea de Comandos**
```bash
python sim_mt.py <archivo.txt> [-o salida.txt] [--max-steps N] [--dot]
```

**Ejemplos:**
```bash
# Ejecutar palíndromo y guardar salida
python sim_mt.py MT2/mt_palindromo.txt -o salida.txt

# Con límite de pasos y generar diagrama
python sim_mt.py MT2/mt_suma.txt --max-steps 100 --dot

# Ver ayuda
python sim_mt.py --help
```

**Símbolos de resultado:**
- `[OK]` → Aceptado
- `[X]` → Rechazado  
- `[LOOP]` → Ciclo infinito detectado

---

## 📦 **Módulos del Proyecto**

### **1. `maquina_turing.py`** - Simulador Core

Implementa la clase `MaquinaTuring` con:

```python
class MaquinaTuring:
    def __init__(self, Q, Sigma, Gamma, delta, q0, qaccept, qreject, blank='⊔')
    def validate()              # Verifica definición correcta
    def simulate(w, max_steps)  # Ejecuta la máquina
    def to_dot()                # Genera diagrama Graphviz
```

**Características clave:**
- Cinta infinita implementada con `defaultdict(lambda: blank)`
- Cabezal inicia en posición 0 (`left_boundary`)
- Si intenta moverse L desde posición 0, se queda ahí (tope izquierdo)
- Configuraciones en formato `u q v`:
  - `u` = contenido antes del cabezal
  - `q` = estado actual
  - `v` = contenido desde cabezal hacia derecha

### **2. `parser_mt.py`** - Parser de Especificaciones

Lee archivos `.txt` con formato:

```
Q = {q0, q1, q2, qacc, qrej}
Sigma = {a, b}
Gamma = {a, b, X, ⊔}
blank = ⊔
q0 = q0
qaccept = qacc
qreject = qrej

delta:
(q0, a) -> (q1, X, R)
(q1, b) -> (q2, b, L)

input = aabba
```

### **3. `sim_mt.py`** - CLI

Interfaz de línea de comandos con opciones:
- `-o FILE`: Guardar configuraciones en archivo
- `--max-steps N`: Límite de pasos (detecta ciclos)
- `--dot`: Generar diagrama automáticamente

### **4. `sim_mt_pdf.py`** - Menú Interactivo

Sistema de menú que:
- Auto-descubre todas las MTs en `MT1/` y `MT2/`
- Ejecuta máquinas con un solo clic
- Genera diagramas automáticamente
- Filtra warnings de encoding

---

## 🔄 **Máquina Destacada: Verificador de Palíndromos**

### **Algoritmo**

El verificador de palíndromos (`mt_palindromo.txt`) usa la estrategia de **"pelar desde los extremos"**:

**Estados:**
```
Q = {q0, q_busca_a, q_busca_b, q_ret_a, q_ret_b, q_verif, qacc, qrej}
```

**Alfabeto de cinta:**
```
Σ = {a, b}          # Entrada
Γ = {a, b, X, ⊔}    # Cinta (X = marcador)
```

### **Funcionamiento Paso a Paso**

#### **1. Marcar extremo izquierdo**
```
q0:
  - Lee 'a' → Marca con X, va a q_busca_a (recordando que era 'a')
  - Lee 'b' → Marca con X, va a q_busca_b (recordando que era 'b')
  - Lee 'X' → Salta (ya verificado)
  - Lee '⊔' → Todo verificado → ACEPTA ✓
```

#### **2. Buscar extremo derecho**
```
q_busca_a / q_busca_b:
  - Avanzan → hasta encontrar '⊔'
  - Retroceden ← un paso para leer último símbolo
```

#### **3. Verificar coincidencia**
```
Si venimos de q_busca_a:
  - Último debe ser 'a' → Marca con X, va a q_ret_a ✓
  - Si es 'b' o 'X' → RECHAZA ✗

Si venimos de q_busca_b:
  - Último debe ser 'b' → Marca con X, va a q_ret_b ✓
  - Si es 'a' o 'X' → RECHAZA ✗
```

#### **4. Regresar al inicio**
```
q_ret_a / q_ret_b:
  - Se mueven ← (izquierda)
  - Pasan sobre 'a', 'b', 'X'
  - Al encontrar '⊔' → Vuelven a q0 para siguiente iteración
```

### **Ejemplo: Verificación de "aba"**

```
Paso  Configuración          Estado       Acción
──────────────────────────────────────────────────────────────
  1    q0 aba                q0           Lee 'a', marca X
  2   X q_busca_a ba         q_busca_a    Avanza →
  3   Xb q_busca_a a         q_busca_a    Avanza →
  4   Xba q_busca_a ⊔        q_busca_a    Encuentra fin
  5   Xb q_busca_a a         q_busca_a    Retrocede ←
  6   X q_ret_a bX           q_ret_a      Lee 'a', marca X ✓
  7    q_ret_a XbX           q_ret_a      Retrocede ←
  8    q0 XbX                q0           Nueva iteración
  9   X q0 bX                q0           Salta X
 10   Xb q0 X                q0           Salta X
 11   XbX q0 ⊔               q0           Solo X → ACEPTA ✓
```

**Resultado:** `aba` es palíndromo → **ACEPTADO [OK]**

### **¿Por Qué Funciona?**

1. ✅ **"Pela" la cadena** desde extremos hacia el centro
2. ✅ **Cada iteración** verifica que primer y último símbolo coincidan
3. ✅ **Símbolos verificados** se marcan con X (no se revisan dos veces)
4. ✅ **Si solo quedan X** → es palíndromo → ACEPTA
5. ✅ **Si algún par difiere** → NO es palíndromo → RECHAZA

### **Casos de Prueba**

| Archivo                        | Input  | Resultado | Descripción |
|--------------------------------|--------|-----------|-------------|
| `mt_palindromo.txt`            | `aba`  | `[OK]`    | Palíndromo válido |
| `mt_palindromo_rechaza.txt`    | `abb`  | `[X]`     | No es palíndromo |
| `mt_palindromo_infinito.txt`   | `aaa`  | `[LOOP]`  | Transición faltante → ciclo |

---

## 🎯 **Otras Máquinas Incluidas**

### **MT1/ - Máquinas Simples**

| Archivo           | Descripción                    | Input | Resultado |
|-------------------|--------------------------------|-------|-----------|
| `mt_acepta.txt`   | Acepta cadena "1"              | `1`   | `[OK]`    |
| `mt_rechaza.txt`  | Rechaza "01"                   | `01`  | `[X]`     |
| `mt_infinito.txt` | Ciclo infinito con "00"        | `00`  | `[LOOP]`  |

### **MT2/ - Máquinas Complejas**

| Archivo       | Descripción                           | Ejemplo Input | Output |
|---------------|---------------------------------------|---------------|--------|
| `mt_suma.txt` | Suma en unario: `111#11` → `11111`   | `111#11`      | `11111` |
| `mt_mult2.txt`| Multiplicación ×2 en binario          | `101`         | `1010` |

---

## 📊 **Generación de Diagramas**

Los diagramas se generan automáticamente en formato **Graphviz DOT**:

```bash
python sim_mt.py MT2/mt_palindromo.txt --dot
```

Esto crea `MT2/mt_palindromo_diagrama.dot` que puedes visualizar con:
- [Graphviz Online](https://dreampuf.github.io/GraphvizOnline/)
- Graphviz local: `dot -Tpng diagrama.dot -o diagrama.png`

**Características:**
- ✅ Solo muestra estados **realmente usados** en las transiciones
- ✅ Estados de aceptación con **doble círculo**
- ✅ Estados de rechazo con **color rojo**
- ✅ Transiciones etiquetadas con `a/b,M`

---

## 🔧 **Formato de Especificación**

```
# Comentarios empiezan con #

Q = {estado1, estado2, ...}
Sigma = {símbolo1, símbolo2, ...}
Gamma = {símbolo1, símbolo2, ..., ⊔}
blank = ⊔
q0 = estado_inicial
qaccept = estado_aceptacion
qreject = estado_rechazo

delta:
(estado_origen, símbolo_leído) -> (estado_destino, símbolo_escrito, Movimiento)
# Movimiento: L (izquierda) o R (derecha)

input = palabra_de_entrada
```

---

## ✅ **Validaciones**

El simulador verifica automáticamente:
- ✓ `q0 ∈ Q`
- ✓ `qacc, qrej ∈ Q` y `qacc ≠ qrej`
- ✓ `Σ ⊆ Γ`
- ✓ `blank ∈ Γ` y `blank ∉ Σ`
- ✓ Todas las transiciones usan estados y símbolos definidos
- ✓ Movimientos válidos: solo L o R

---

## 🎓 **Notación de Clase**

El simulador respeta exactamente la notación vista en clase:

**Definición formal:**
```
M = (Q, Σ, Γ, δ, q0, qacc, qrej)
```

**Configuración:**
```
u q v
```
Donde:
- `u` = contenido de la cinta antes del cabezal
- `q` = estado actual
- `v` = contenido desde el cabezal (inclusive) hacia la derecha

**Función de transición:**
```
δ: Q × Γ → Q × Γ × {L, R}
```

---

## 📝 **Requisitos**

- Python 3.7+
- Solo librerías estándar (no requiere instalación adicional)

---

## 👨‍💻 **Autor**

Daniel Chet  
Universidad del Valle de Guatemala  
MM3032 - Lógica Matemática - Semestre 6

---

## 📄 **Licencia**

Proyecto académico - MM3032 Parcial 4
