import json
import requests
from flask_babel import _
from flask import current_app

def translate(text,source_language,dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: The developer is too poor to buy credits for the api 🙃')
    auth = {'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY']}
    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
                     '/Translate?text={}&from={}&to={}'.format(
                        text, source_language, dest_language),
                            headers=auth)
    if r.status_code!=200:
        return _('Error: The developer is too poor to buy credits for the api 🙃')
    return json.loads(r.content.decode('utf-8-sig'))
    