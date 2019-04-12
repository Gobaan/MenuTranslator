function render(url, xs, ys) {
   let sWidth = xs[1] - xs[0];
   let sHeight = ys[1] - ys[0];
   let img = new Image();
   img.crossOrigin = "Anonymous";
   img.onload = function() {
     let canvas = document.getElementById("view");
     var ctx = canvas.getContext('2d');
     ctx.canvas.width = 1000;
     ctx.canvas.height = 1000;
     stackBlurImage(img, canvas, 5, false);
     ctx.rect( xs[0], ys[0], sWidth, sHeight);
           ctx.strokeStyle = "#FF0000";
           ctx.stroke();
     ctx.clip();
     ctx.drawImage(img, 0,  0);
   }
   img.src = url;
}
