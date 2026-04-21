#!/usr/bin/env python3
"""
Helper script para añadir mensajes a la cola de Teams webhook relay.

Uso:
    python send_message.py "Tu mensaje aquí"
    python send_message.py "Alerta de seguridad" --severity high --title "Security Alert"
    python send_message.py "Test" --source "Armis Centrix"
"""

import json
import argparse
import subprocess
from datetime import datetime

def add_message_to_queue(text, title=None, severity="info", source=None):
    """Añade un mensaje a la cola y hace commit automáticamente."""
    
    message = {
        "text": text,
        "severity": severity
    }
    
    if title:
        message["title"] = title
    if source:
        message["source"] = source
    
    # Añadir al archivo JSONL
    with open("queue/pending.jsonl", "a") as f:
        f.write(json.dumps(message) + "\n")
    
    print(f"✅ Mensaje añadido a la cola: {text}")
    
    # Git add, commit, push
    try:
        subprocess.run(["git", "add", "queue/pending.jsonl"], check=True)
        subprocess.run(
            ["git", "commit", "-m", f"Add message: {text[:50]}"],
            check=True
        )
        subprocess.run(["git", "push"], check=True)
        print("✅ Cambios pusheados a GitHub")
        print("⏱️  El mensaje será procesado en el siguiente minuto")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al pushear: {e}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Envía mensajes a Teams vía GitHub Actions queue"
    )
    parser.add_argument("text", help="Texto del mensaje")
    parser.add_argument("--title", "-t", help="Título del mensaje")
    parser.add_argument(
        "--severity", "-s",
        choices=["info", "low", "medium", "high", "critical"],
        default="info",
        help="Nivel de severidad"
    )
    parser.add_argument("--source", help="Origen del mensaje")
    
    args = parser.parse_args()
    
    add_message_to_queue(
        text=args.text,
        title=args.title,
        severity=args.severity,
        source=args.source
    )

if __name__ == "__main__":
    main()
