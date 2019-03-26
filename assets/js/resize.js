function ResizeImage(e, file) {
    var img = document.createElement("img");

    img.onload = function(e) {
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
       var ctx = canvas.getContext("2d");
       ctx.drawImage(img, 0, 0, width, height);

       dataurl = canvas.toDataURL(file.type);
       document.getElementById('output').src = dataurl;
       document.getElementById('input_image').value = dataurl;
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

