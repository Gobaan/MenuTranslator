from jinja2 import Environment, FileSystemLoader

import logging
from base64 import b64decode
import cherrypy
import google.cloud.storage
import hashlib
import menu_translator
import pickle
import uuid
import word_extractor
import html
import json
from google.api_core.exceptions import NotFound

logging.basicConfig(filename='app.log', level=logging.DEBUG)
env = Environment(loader=FileSystemLoader('assets/templates'))
env.filters['escape'] = html.escape
env.filters['to_json'] = json.dumps
# how does google ocr do with 180 rotatation, and can i hugh transfork to fix major rotations
class Root(object):
  # TODO: Make landing page less shitty
  @cherrypy.expose
  def index(self):
    tmpl = env.get_template('viewport2.html')
    return tmpl.render()

  @cherrypy.expose
  def upload(self, menu_image):
    tmpl = env.get_template('render.html')
    bucket_name = "gobaan.com"
    logging.debug (menu_image[:40])
    hasher = hashlib.md5()
    hasher.update(menu_image.encode('utf-8'))
    name = hasher.hexdigest()

    header, encoded = menu_image.split(",", 1)
    data = b64decode(encoded)
    client = google.cloud.storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(str(name))
    logging.debug(f'blobs name is {blob.public_url}')
    try:
        blob.reload()
    except NotFound:
        logging.debug(f'blob does not already exist')
        header = header[header.find(':') + 1:header.find(';')]
        blob.upload_from_string(data, content_type=header)

    logging.debug(f'translating')
    items = menu_translator.translate_image(blob.public_url)
    return tmpl.render(url=blob.public_url, menu=items)
 
  @cherrypy.expose
  def test(self):
    tmpl = env.get_template('render.html')
    url = 'https://storage.googleapis.com/gobaan.com/5ca822dc8a6b25f64c57c99b846da890'
    items = menu_translator.translate_image(url)
    return tmpl.render(url=url, menu=items)


  @cherrypy.expose
  def slice(self):
    tmpl = env.get_template('overlay.html')
    url = 'https://storage.googleapis.com/gobaan.com/368e6892765c8a2b633c52dd60a1cf25'
    items = menu_translator.translate_image(url)
    return tmpl.render(menu=items, url=url)

  @cherrypy.expose
  def debug(self):
      with open('menu.pickle', 'rb') as fp:
        ocr_json = pickle.load(fp)

      tmpl = env.get_template('canvas.html')
      text = ocr_json[1:]
      words = [word_extractor.Word(word) for word in text]

      with open('names.pickle', 'rb') as fp:
          items = pickle.load(fp)
      SIZE = 1000    
      ratio = max(word_extractor.get_bounds(items)) / SIZE
      return tmpl.render(words=words, items=items, ratio=ratio, size=SIZE)

  @cherrypy.expose
  def download(self):
    cherrypy.response.headers['Content-Type'] = 'application/octet-stream'
    cherrypy.response.headers['Content-Disposition'] = 'attachment;filename=menu.pickle'
    with open('menu.pickle', 'rb') as fp:
      return fp.read()
 
if __name__ == '__main__':
  cherrypy.config.update({

   'tools.response_headers.on': True,
            'tools.response_headers.headers': [
                ('Access-Control-Allow-Origin', '*')],
    'server.socket_host': '104.237.154.27',
    'server.socket_port': 8091,
  })
  cherrypy.quickstart(Root(), '/translate', 'prod.conf')
