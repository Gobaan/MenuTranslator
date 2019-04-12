import pickle
from . import searcher
from . import word_extractor
import os.path

def translate_image(image_url):
    with searcher.Searcher() as google:
      ocr_json = google.get_ocr(image_url)
      with open(os.path.join('cache, menu.pickle'), 'wb') as fp:
        pickle.dump(ocr_json, fp)

      text = ocr_json[1:]
      names = [name for name in word_extractor.get_names(text)]
      print (names)
      with open(os.path.join('cache, names.pickle'), 'wb') as fp:
          pickle.dump(names, fp)
    
      translations = google.get_translations(names)
      images = google.get_images(names)
      data = [{
          'name': str(name), 
          'images':image, 
          'translation': translation, 
          'xs': name.x_bounds, 
          'ys': name.y_bounds
          }
          for name, image, translation in zip(names, images, translations)]
      return data
