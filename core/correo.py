"""Aviso por correo (Outlook / Microsoft 365) cuando llega un mensaje de contacto.

Dos modos, según CORREO_MODO en el .env:
  - "smtp":  usuario + contraseña en smtp.office365.com (simple; Microsoft lo desactiva
             por defecto a fines de 2026, el administrador puede reactivarlo).
  - "graph": Microsoft Graph con una app registrada en Entra ID (OAuth, recomendado).
Si CORREO_MODO está vacío no se envía nada (el mensaje igual queda guardado en el admin).
"""
import json
import logging
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.mail import EmailMessage

log = logging.getLogger(__name__)


def _token_graph():
    url = f'https://login.microsoftonline.com/{settings.MS_TENANT_ID}/oauth2/v2.0/token'
    data = urllib.parse.urlencode({
        'client_id': settings.MS_CLIENT_ID,
        'client_secret': settings.MS_CLIENT_SECRET,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials',
    }).encode()
    with urllib.request.urlopen(url, data=data, timeout=10) as r:
        return json.load(r)['access_token']


def _enviar_graph(asunto, cuerpo, destinos, responder_a):
    payload = {
        'message': {
            'subject': asunto,
            'body': {'contentType': 'Text', 'content': cuerpo},
            'toRecipients': [{'emailAddress': {'address': d}} for d in destinos],
            'replyTo': [{'emailAddress': {'address': responder_a}}] if responder_a else [],
        },
        'saveToSentItems': True,
    }
    req = urllib.request.Request(
        f'https://graph.microsoft.com/v1.0/users/{settings.CORREO_REMITENTE}/sendMail',
        data=json.dumps(payload).encode(),
        headers={'Authorization': f'Bearer {_token_graph()}', 'Content-Type': 'application/json'},
        method='POST',
    )
    urllib.request.urlopen(req, timeout=10).close()


def _enviar_smtp(asunto, cuerpo, destinos, responder_a):
    EmailMessage(
        subject=asunto, body=cuerpo,
        from_email=settings.CORREO_REMITENTE, to=destinos,
        reply_to=[responder_a] if responder_a else None,
    ).send(fail_silently=False)


def enviar_aviso_contacto(nombre, email, mensaje):
    modo = settings.CORREO_MODO
    if not modo:
        return False
    asunto = f'Nuevo contacto web: {nombre or email}'
    cuerpo = f'Nombre: {nombre}\nCorreo: {email}\n\n{mensaje}\n\n— Enviado desde el formulario de vcchile.cl'
    try:
        (_enviar_graph if modo == 'graph' else _enviar_smtp)(asunto, cuerpo, settings.CORREO_DESTINO, email)
        return True
    except Exception:
        # El mensaje ya quedó guardado en la base de datos: no se interrumpe al visitante.
        log.exception('No se pudo enviar el aviso de contacto (modo %s)', modo)
        return False
