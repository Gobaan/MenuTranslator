import pickle
import searcher
import word_extractor

def translate_image(image_url):
    with searcher.Searcher() as google:
      ocr_json = google.get_ocr(image_url)
      with open('menu.pickle', 'wb') as fp:
        pickle.dump(ocr_json, fp)

      text = ocr_json[1:]
      names = [name for name in word_extractor.get_names(text)]
      print (names)
      with open('names.pickle', 'wb') as fp:
          pickle.dump(names, fp)
    
      translations = google.get_translations(names)
      images = google.get_images(names)
      data = ([{'name': str(name), 'images':image, 'translation': translation}
          for name, image, translation in zip(names, images, translations)])
      return data


# Done:  display axis or auto rotate so text is aligned before slicing
# Done: Shrink image before upload to limit time
#   overly prettily 
# Add debug level logging/debug mode

#  Parsing can be akward since menus go full retard, users need more control
#  investigate translation to see if i can get the hints
#  Location/Source hints may be value town
#  allow users to fix ocr or edit translation 
#  create lookup table for approximate translations (food lookup table)
# Add test cases?
# Canvas code on debug is retarded right now
