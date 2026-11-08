# DorkBuster
*DorkBuster es una herramienta de código abierto avanzada de reconocimiento OSINT y Google Dorking automatizado con interfaz gráfica moderna en PyQt5 y generación de dorks asistida por IA (OpenRouter).*

---

##  Novedades de la Versión 2.0 (V2)

* **Interfaz Gráfica Moderna con PyQt5**: Sustitución de `tkinter` por una GUI minimalista en escala de grises oscuros, negro y blanco.
*  **Generación de Dorks con Cualquier Modelo de OpenRouter**: Entrada de texto libre para usar cualquier modelo disponible en OpenRouter (por ejemplo, `deepseek/deepseek-v4-flash-0731`, `google/gemma-4-26b-a4b-it`, `nvidia/nemotron-3-ultra-550b-a55b:free`, etc.).
*  **Seguridad y Persistencia en `config.json`**: Guarda tu configuración y oculta tu API key una vez configurada (mostrada como `apikey-xxxxxxxxxx` o deshabilitada), con botón para editarla cuando desees.
* **Soporte de Proxy (HTTP / HTTPS / SOCKS5)**: Posibilidad de enrutar todas las consultas a través de servidores proxy o la red Tor (`socks5://127.0.0.1:9050`), con botón integrado para probar la conectividad y verificar la IP pública de salida antes de iniciar las búsquedas.
* **Búsqueda Multi-Motor Simultánea**: Consulta en Bing, Yahoo, DuckDuckGo, Google (vía `googlesearch-python`) y Google directo (`requests`) a la vez, con soporte de fingerprinting TLS de navegador (`primp`) para máxima fiabilidad.
*  **Deduplicación de Enlaces en Tiempo Real**: Si múltiples motores devuelven las mismas URLs o parámetros de tracking duplicados, el sistema normaliza y descarta los duplicados, manteniendo una lista limpia de resultados únicos.
*  **Control Total (Hilos en Segundo Plano y Cancelación)**: La interfaz nunca se congela (`QThread`) e incluye un botón **Detener** para cancelar la búsqueda en curso en cualquier momento (`threading.Event`).
*  **Compatibilidad Hacia Atrás**: Si no cuentas con una API key o prefieres no usar IA, puedes ingresar dorks manuales o utilizar los dorks estáticos tradicionales de la versión original.

---

## Requisitos para utilizar la IA
* Cuenta y clave de API en [OpenRouter](https://openrouter.ai/) si deseas utilizar la generación de dorks mediante LLM.
* Es posible utilizar modelos gratiutos o de paga con openrouter.

---

##  Instalación

1. **Clonar o descargar el proyecto:**
   ```bash
   git clone https://github.com/Euronymou5/DorkBuster.git
   cd DorkBuster
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

---

##  Ejecución

Puedes iniciar la herramienta ejecutando:

```bash
python dorkbuster.py
```

# Licencia 

**[MPL-2.0 license](https://github.com/Euronymou5/DorkBuster/blob/main/LICENSE)**

# Contacto

[![discord](https://img.shields.io/badge/Discord-euronymou5-a?style=plastic&logo=discord&logoColor=white&labelColor=black&color=7289DA)](https://discord.com/users/452720652500205579)

![email](https://img.shields.io/badge/ProtonMail-mr.euron%40proton.me-a?style=plastic&logo=protonmail&logoColor=white&labelColor=black&color=8B89CC)

[![X](https://img.shields.io/twitter/follow/Euronymou51?style=plastic&logo=X&label=%40Euronymou51&labelColor=%23000000&color=%23000000)](https://x.com/Euronymou51)
