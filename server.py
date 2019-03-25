from jinja2 import Environment, FileSystemLoader

from base64 import b64decode
import cherrypy
import google.cloud.storage
import hashlib
import menu_translator
import pickle
import uuid
import word_extractor

env = Environment(loader=FileSystemLoader('assets/templates'))

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
    print (menu_image)
    header, encoded = menu_image.split(",", 1)
    data = b64decode(encoded)
    client = google.cloud.storage.Client()
    bucket = client.get_bucket(bucket_name)
    hasher = hashlib.md5()
    hasher.update(menu_image)
    name = hasher.hexdigest()
    blob = bucket.blob(str(name))

    items = menu_translator.translate_image(blob.public_url)
    return tmpl.render(menu=items)

  @cherrypy.expose
  def debug(self):
      with open('menu.pickle', 'rb') as fp:
        ocr_json = pickle.load(fp)

      tmpl = env.get_template('canvas.html')
      text = ocr_json[1:]
      words = [word_extractor.Word(word) for word in text]

      print (average_slant)
      words = [word.normalize(average_slant) for word in words]

      with open('names.pickle', 'rb') as fp:
          items = pickle.load(fp)
      SIZE = 1800    
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
    'server.socket_host': '104.237.154.27',
    'server.socket_port': 8091,
  })
  cherrypy.quickstart(Root(), '/translate', 'prod.conf')
