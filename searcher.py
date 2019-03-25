from io import BytesIO
from pickle import Pickler, Unpickler
import collections
import dbm
import google.cloud.vision, google.cloud.translate
import json 
import jsonpath_ng
import requests
import shelve
import urllib.parse

#TODO: hook up caching
#gcloud auth print-access-token
#put gcloud token here 


# TODO: Secure these
API_KEY = "AIzaSyCcr0VgTjSXpramrw4DmEp1Jm79RD_INSY"
ENGINE_ID = "010234774377017637134:m597rvd0t8c"
TRANSLATION_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"
OCR_ENDPOINT = "https://vision.googleapis.com/v1/images:annotate"
TARGET = "en"
SOURCE = "vi"

def find_image(query):
  #TODO: wrap this in a more gcloud style library 
  params = {
          'q': query, 
          'cx': ENGINE_ID,
          'imgColorType': 'color',
          'imgType': 'photo',
          'safe': 'active',
          'searchType': 'image',
          'key': API_KEY
  }

          
  site = f"https://www.googleapis.com/customsearch/v1?{urllib.parse.urlencode(params)}"
  print (f"searching... {site}")
  response = json.loads(requests.get(site).text)
  link_expr = jsonpath_ng.parse("items[*].link")
  image_expr = jsonpath_ng.parse("items[*].image")
  links = [match.value for match in link_expr.find(response)]
  images = [match.value for match in image_expr.find(response)]
  return [{'image': image, 'link': link} for image, link in zip(images, links)]

def translate_text(query):
  client = google.cloud.translate.Client()
  return client.translate(query, target_language=TARGET)['translatedText']

def ocr_image(image_url):
  client = google.cloud.vision.ImageAnnotatorClient()
  print (image_url)
  response = client.annotate_image({
        "image":{"source":{"image_uri": image_url}},
        "features": [{"type":"TEXT_DETECTION",}]
      })
  annotations = [{
      'description': entity.description,
      'score': entity.score,
      'locale': entity.locale,
      'bounds': [(vertex.x, vertex.y) for vertex in entity.bounding_poly.vertices]
      } for entity in response.text_annotations]
  return annotations

class DefaultShelf(shelve.Shelf):
  #TODO: Share Session Object
  #TODO: Clear cache on error and notify user
  def __init__(self, name, default_fn):
    super().__init__(dbm.open(name, "c"), None, True)
    self.default_fn = default_fn

  def __getitem__(self, key):
    try:
      return super().__getitem__(key)
    except KeyError:
        pass
    print ('triggering default')
    value = self.default_fn(key)
    if self.writeback:
      self.cache[key] = value
    return value

 
"""
Wrapper for google API that finds images, text and ocr results while caching the results for the second two to minimize bandwith
Currently caches to hard disk, maybe upgrade in the future
"""
class Searcher(object):       
  # Possible bug: if two languages have the same name for a different food  
  def __init__(self, cache_name = "google"):  
    self.cache_name = cache_name 
    
  def __enter__(self):        
    self.translation_shelf = DefaultShelf(f"translate_{self.cache_name}", translate_text)
    self.image_shelf = DefaultShelf(f"images_{self.cache_name}", find_image)
    self.ocr_shelf = DefaultShelf(f"ocr_{self.cache_name}", ocr_image)
    return self

  def __exit__(self, *args):
    self.image_shelf.close()
    self.translation_shelf.close()
    self.ocr_shelf.close()
   
  def get_ocr(self, image_url):
      print (image_url)
      return self.ocr_shelf[image_url]

  def get_translations(self, names):  
    return [self.translation_shelf[str(name)] for name in names]
        
  def get_images(self, names):
    return [self.image_shelf[str(name)] for name in names]
        
              
if __name__ == "__main__":
  with Searcher() as searcher:
    words = ["Lo siento", "mi espanol es muy malo"]
    text = searcher.get_translations(words)
    print (text)
    images = searcher.get_images(["chicken noodle soup"])
    images = searcher.get_images(["chicken noodle soup"])
    print (images)
    # Put image bucket url here
    image_url = "https://i.imgur.com/KedtDHK.jpg"
    ocr = searcher.get_ocr(image_url)
    print (ocr)
  
