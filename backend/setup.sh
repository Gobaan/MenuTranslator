export GOOGLE_APPLICATION_CREDENTIALS="/home/lordofall/source/gcloudtranslatekey.json"
if [ ! -e "cache" ]; then
  mkdir cache
fi
if [ ! -e static ]; then 
  ln -s ../frontend/dist/static static
fi
if [ ! -e homepage.html ]; then
  ln -s ../frontend/dist/index.html homepage.html
fi

