import pickle
import searcher
import word_extractor

def translate_image(image_url):
    with searcher.Searcher() as google:
      ocr_json = google.get_ocr(image_url)
      with open('menu.pickle', 'wb') as fp:
        pickle.dump(ocr_json, fp)

      text = ocr_json[1:]
      words = [word_extractor.Word(word) for word in text]

      average_slant = sum(word.slant() for word in words) / len(words)
      print (average_slant)
      words = [word.normalize(average_slant) for word in words]
      names = [name for name in word_extractor.get_names(words)]
      print (names)
      with open('names.pickle', 'wb') as fp:
          pickle.dump(names, fp)
    
      translations = google.get_translations(names)
      images = google.get_images(names)
      data = ([{'name': str(name), 'images':image, 'translation': translation}
          for name, image, translation in zip(names, images, translations)])
      return data


# investigate translation to see if i can get the hints
#  allow users to fix ocr or edit translation 
#  create lookup table for approximate translations (food lookup table)
#   overly prettily 
#  display axis or auto rotate so text is aligned before slicing
# fix bugs in ocr
