# Message Queue

Este directorio contiene la cola de mensajes pendientes para enviar a Teams.

## Funcionamiento

1. Los mensajes se añaden al archivo `pending.jsonl` (un JSON por línea)
2. GitHub Actions ejecuta cada minuto y procesa todos los mensajes
3. Después de procesarlos, limpia el archivo

## Formato de mensaje

```json
{"text":"Tu mensaje aquí","title":"Título opcional","severity":"info","source":"Origen del mensaje"}
```

## Severidades disponibles
- `info` (default)
- `low`
- `medium`
- `high`
- `critical`

## Ejemplo de uso

Para añadir un mensaje a la cola, simplemente haz commit de una nueva línea en `pending.jsonl`:

```bash
echo '{"text":"Alerta de seguridad detectada","severity":"high","source":"Armis Centrix"}' >> queue/pending.jsonl
git add queue/pending.jsonl
git commit -m "Add security alert"
git push
```

El mensaje será procesado en el siguiente minuto.
