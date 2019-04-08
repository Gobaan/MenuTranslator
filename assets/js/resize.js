// TODO: Shrink this file
// TODO: Add buttons to fix the rotation
// TODO: Make these class like (Vueify)

function get_rotation(img) {
  return new Promise ((resolve, reject) => {
    EXIF.getData(img, function() {
      console.log('Exif=', EXIF.getTag(this, "Orientation"));
      var rotation = 0;
      switch(parseInt(EXIF.getTag(this, "Orientation"))) {
        case 3:
          rotation = 180; break;
        case 4:
          rotation = 180; break;
        case 5:
          rotation = 270; break;
        case 6:
          rotation = 90; break;
        case 7:
          rotation = 90; break;
        case 8:
          rotation = 270; break;
      } 
      resolve (rotation);
    })});
}

async function rotate_and_draw(file, img) {
  let rotation = await get_rotation(img);
  const TO_RADIANS = Math.PI / 180;
  const angle = rotation * TO_RADIANS;
  var MAX_WIDTH = 1000;
  var MAX_HEIGHT = 1000;
  var width = img.width;
  var height = img.height;

  if (width > height) {
      if (width > MAX_WIDTH) {
          height *= MAX_WIDTH / width;
          width = MAX_WIDTH;
      }
  } else {
      if (height > MAX_HEIGHT) {
          width *= MAX_HEIGHT / height;
          height = MAX_HEIGHT;
      }
  }
  var canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  if (rotation % 180 == 90) {
    [canvas.width, canvas.height] = [canvas.height, canvas.width] 
  }

  var ctx = canvas.getContext("2d");
  ctx.save(); 
  ctx.translate(canvas.width / 2, canvas.height / 2);
  ctx.rotate(angle);
  ctx.drawImage(img, -width/2, -height/2, width, height);
  ctx.restore(); 

  dataurl = canvas.toDataURL(file.type);
  document.getElementById('output').src = dataurl;
  document.getElementById('input_image').value = dataurl;
}

function ResizeImage(e, file) {
    var img = document.createElement("img");
    img.onload = function(e) {
       rotate_and_draw(file, img);
    };
    img.src = e.target.result;
}

$(document).ready(function() {

    $('#imageFile').change(function(evt) {
        if (!(window.File && window.FileReader && window.FileList && window.Blob)) {
            alert('The File APIs are not fully supported in this browser.');
            return;
        }

        var files = evt.target.files;
        var file = files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload =  function(e)
          {
             ResizeImage(e, file);
          }
            reader.readAsDataURL(file);
        }
    });
});

