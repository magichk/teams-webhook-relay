# Teams Webhook Relay via GitHub Actions

Sistema de relay de webhooks hacia Microsoft Teams usando GitHub Actions como intermediario, diseñado para contextos donde hay restricciones de allowlist de red.

## 🎯 Objetivo

Permitir que sistemas con acceso limitado a dominios (como Claude AI) puedan enviar mensajes a Teams escribiendo en un repositorio de GitHub, mientras GitHub Actions se encarga de hacer el relay.

## 🏗️ Arquitectura

```
Sistema origen → Commit a queue/pending.jsonl → GitHub Actions (cada minuto) → Teams Webhook
   (Claude)         (github.com ✅)                   (procesa cola)          (Power Automate)
```

## ⚙️ Configuración inicial

### 1. Configurar el secret del webhook de Teams

En tu repositorio:
1. Ve a **Settings** → **Secrets and variables** → **Actions**
2. Click en **New repository secret**
3. Name: `TEAMS_WEBHOOK_URL`
4. Value: Tu URL de webhook de Power Automate

### 2. Habilitar GitHub Actions

1. Ve a **Actions** en tu repositorio
2. Habilita los workflows si están deshabilitados
3. El workflow `process-queue.yml` se ejecutará automáticamente cada minuto

### 3. Dar permisos de escritura a GitHub Actions

1. **Settings** → **Actions** → **General**
2. Scroll hasta "Workflow permissions"
3. Selecciona **Read and write permissions**
4. Guarda cambios

## 📤 Métodos de envío

### Método 1: Script Python (recomendado)

```bash
# Envío simple
python send_message.py "Tu mensaje aquí"

# Con opciones completas
python send_message.py "Alerta de seguridad detectada" \
  --title "Security Alert" \
  --severity high \
  --source "Armis Centrix"
```

### Método 2: Manual con echo y git

```bash
# Añadir mensaje a la cola
echo '{"text":"Test message","severity":"info","title":"Test"}' >> queue/pending.jsonl

# Commit y push
git add queue/pending.jsonl
git commit -m "Add message"
git push
```

### Método 3: Desde Claude AI (o cualquier sistema con acceso a github.com)

```bash
cd /ruta/al/repo
git pull

# Añadir mensaje
echo '{"text":"Mensaje desde Claude","severity":"info","source":"Claude AI"}' >> queue/pending.jsonl

git add queue/pending.jsonl
git commit -m "Add message from Claude"
git push
```

## 🔔 Formato de mensajes

Cada mensaje es un JSON en una línea del archivo `queue/pending.jsonl`:

```json
{
  "text": "Contenido del mensaje (requerido)",
  "title": "Título opcional",
  "severity": "info|low|medium|high|critical (opcional, default: info)",
  "source": "Origen del mensaje (opcional)"
}
```

## ⏱️ Latencia

- **Máxima**: 1 minuto (intervalo del cron)
- **Típica**: 30-60 segundos

## 🧪 Testing

### Test manual del workflow

1. Ve a **Actions** → **Process Message Queue**
2. Click en **Run workflow**
3. Verifica los logs

### Test de envío

```bash
# Enviar mensaje de prueba
python send_message.py "Test de conectividad" --severity info

# Esperar ~1 minuto y verificar en Teams
```

## 📊 Monitorización

Los logs de cada ejecución están disponibles en:
- **Actions** → **Process Message Queue** → Click en cualquier run

Cada ejecución muestra:
- ✅ Mensajes procesados
- 📤 Payloads enviados
- 🧹 Estado de limpieza de cola
- ❌ Errores si los hay

## 🎓 Uso en laboratorios educativos

### Para profesores (MCSEH)

Este setup es ideal para labs de seguridad donde:
- Los alumnos practican envío de alertas
- Se simula integración SOAR → SIEM → Alerting
- Se audita cada acción (commits visibles en GitHub)

### Ejercicios graduales

**Nivel 1: Envío básico**
```bash
echo '{"text":"Primera alerta del alumno X"}' >> queue/pending.jsonl
git add . && git commit -m "Alumno X - Ejercicio 1" && git push
```

**Nivel 2: Alertas estructuradas**
```python
import json
alert = {
    "text": "Detección de tráfico sospechoso",
    "severity": "high",
    "source": "Suricata IDS",
    "title": f"Alumno {nombre} - Práctica 2"
}
with open("queue/pending.jsonl", "a") as f:
    f.write(json.dumps(alert) + "\n")
```

**Nivel 3: Automatización**
Integrar con Shuffle SOAR o scripts Python para envío automático basado en eventos.

## 🔧 Troubleshooting

### Los mensajes no se procesan

1. Verifica que `TEAMS_WEBHOOK_URL` esté configurado en Secrets
2. Revisa que GitHub Actions tenga permisos de escritura
3. Comprueba los logs en Actions para ver errores

### El workflow no se ejecuta cada minuto

- GitHub Actions puede tener delays en cron schedules (especialmente en repos gratuitos)
- Alternativa: ejecutar manualmente con "Run workflow"

### Errores de permisos en git push

Asegúrate de que "Workflow permissions" esté en "Read and write"

## 📝 Notas de seguridad

- ⚠️ El webhook URL en secrets es sensible - no lo expongas en código
- ⚠️ Considera rate limiting si múltiples personas/sistemas escriben en la cola
- ✅ Todos los mensajes son auditables vía commits de Git
- ✅ GitHub Actions logs registran cada envío

## 🤝 Contribuciones

Este es un proyecto educativo de PRHGE. Fork libre para tus propios labs.

## 📄 Licencia

MIT - Úsalo como quieras para tus cursos y labs de seguridad.

---

**Desarrollado para:** Máster en Ciberseguridad (MCSEH)  
**Instructor:** Joan - Senior Security Automation Engineer @ PRHGE  
**Stack:** GitHub Actions, Power Automate, Teams Webhooks
