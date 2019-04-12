function getRoot(e) {
  if (e.pageX) {
    return e;
  } else if (e.targetTouches[0]) {
    return e.targetTouches[0];
  }
  return e.changedTouches[e.changedTouches.length-1];
}

var app = new Vue({
    el: '#app',
    data: {
        paint: false,
        clickX: [],
        clickY: [],
        clickDrag: [],
        data: 'Draw inside the box',
        progress: false,
        progress_text: '',
        math_answer: null,
        data_array: []
    },
    methods: {
        startDraw(e) {
            var mouseX = getRoot(e).pageX;
            var mouseY = getRoot(e).pageY;
            this.addClick(getRoot(e).pageX, getRoot(e).pageY);
            this.paint = true;
            this.redraw();
	    e.preventDefault();
        },
        endDraw(e) {
            this.paint = false;
            this.data = 'Please wait...';
            Tesseract.recognize(document.getElementById('mainCanvas').getContext("2d"), 'tha')
                .progress((message) => {
                    this.progress = true;
                    this.progress_text = message.status;
			console.log(message.status);
                })
                .then((result) => {
                    this.data = result.text;
                    this.data_array = [];
                    result.symbols.forEach((str) => {
                        this.data_array.push(str.text);
                    })
			console.log (this.data_array);

                })
                .catch((error) => {
                    console.log('Error', error);
                    this.progress = true;
                    this.progress_text = error;
                });
            e.preventDefault();
        },
        leave() {
            if (this.paint) {
                this.endDraw();
            }
        },
        drawing(e) {
            if (this.paint) {
                this.addClick(getRoot(e).pageX, getRoot(e).pageY, true);
                this.redraw();
                e.preventDefault();
            }
        },
        addClick(x, y, dragging) {
            var mainCanvas = document.getElementById('mainCanvas');
            this.clickX.push(x - mainCanvas.offsetLeft);
            this.clickY.push(y - 2 * mainCanvas.offsetTop);
            this.clickDrag.push(dragging)
        },
        redraw() {
            var mainCanvas = document.getElementById('mainCanvas').getContext("2d");
            mainCanvas.clearRect(0, 0, mainCanvas.canvas.width, mainCanvas.canvas.height);

            mainCanvas.strokeStyle = "#FFFFFF";
            mainCanvas.lineJoin = "round";
            mainCanvas.lineWidth = 5;

            for (var i = 0; i < this.clickX.length; i++) {
                mainCanvas.beginPath();
                if (this.clickDrag[i] && i) {
                    mainCanvas.moveTo(this.clickX[i - 1], this.clickY[i - 1]);
                } else {
                    mainCanvas.moveTo(this.clickX[i] - 1, this.clickY[i]);
                }
                mainCanvas.lineTo(this.clickX[i], this.clickY[i]);
                mainCanvas.closePath();
                mainCanvas.stroke();
            }
        },
        clearCanvas() {
            console.log('cleared')
            var mainCanvas = document.getElementById('mainCanvas').getContext('2d');
            mainCanvas.clearRect(0, 0, mainCanvas.canvas.width, mainCanvas.canvas.height);
            this.clickX = []
            this.clickY = []
            this.clickDrag = []
            this.data_array = []
            this.math_answer = null
            this.data = 'Draw inside the box'
        }
    }
})
