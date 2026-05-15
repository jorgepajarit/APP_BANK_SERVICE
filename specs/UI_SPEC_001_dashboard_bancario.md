# UI_SPEC_001_dashboard_bancario.md -- Interfaz de Usuario (Glassmorphism)

## 1. Objetivo Visual
Crear una experiencia de usuario premium y moderna basada en la estética **Glassmorphism** (efecto cristal). La interfaz debe sentirse ligera, tecnológica y segura.

## 2. Paleta de Colores y Estilos
- **Fondo:** Gradiente oscuro (ej. `linear-gradient(135deg, #0f172a 0%, #1e293b 100%)`).
* **Tarjetas (Glass):**
  - Color: `rgba(255, 255, 255, 0.05)` a `rgba(255, 255, 255, 0.1)`.
  - Desenfoque: `backdrop-filter: blur(12px)`.
  - Bordes: `1px solid rgba(255, 255, 255, 0.1)`.
  - Sombra: `0 8px 32px 0 rgba(0, 0, 0, 0.37)`.
- **Tipografía:** 'Inter' o 'Segoe UI' (Sans-serif limpia).
- **Acciones (Accent):** Azul vibrante (`#3b82f6`) o Esmeralda (`#10b981`) para éxitos.

## 3. Componentes Principales
### A. Pantalla de Login
- Card centralizada con efecto glass.
- Campos de texto con bordes sutiles y foco iluminado.
- Botón de acción con hover dinámico.

### B. Dashboard Principal
- **Header:** Resumen del usuario con icono de perfil y botón de Logout.
- **Sección de Cuentas:** Grid de tarjetas horizontales mostrando:
  - Tipo de cuenta (Ahorros, Corriente, Billetera).
  - Balance formateado (ej. `$1.234.567,00`).
  - Iconos representativos (Font Awesome).
- **Tabla de Movimientos:** 
  - Lista de transacciones recientes.
  - Indicadores visuales: Flecha verde arriba para ingresos (CREDIT), flecha roja abajo para egresos (DEBIT).
- **Acceso Rápido:** Botón flotante o barra lateral para "Transferir" y "Pagar PSE".

### C. Formulario de Transferencias
- **Selector de Origen:** Menú desplegable con las cuentas disponibles y sus saldos.
- **Campos de Destino:** Input numérico para el ID de la cuenta destino.
- **Monto:** Input de moneda con validación de dos decimales.
- **Confirmación:** Botón prominente de transferencia con aviso de seguridad.

## 4. Comportamiento (UX)
- **Carga (Spinners):** Todos los botones deben mostrar un estado de carga al ser clickeados mientras se espera la respuesta de la API.
- **Notificaciones (Toasts):** Mensajes emergentes para confirmar transferencias exitosas o mostrar errores de "Saldo Insuficiente".
- **Responsive:** Diseño adaptable para visualización correcta en dispositivos móviles (apilamiento vertical de tarjetas).

## 5. Integración Técnica
- **Motor:** Flask (Python).
- **Consumo API:** Uso de `requests` para conectar con el contenedor `banco_fastapi` en el puerto 8000.
- **Seguridad:** Manejo de sesión mediante tokens JWT obtenidos del backend.
