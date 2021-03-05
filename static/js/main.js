$(document).ready(function(){
  let namespace = "/flask";
  let video = document.querySelector("#videoElement");
  let canvas = document.querySelector("#canvasElement");

  //let canvas2 = document.createElement("CANVAS");
  let canvas1 = document.querySelector("#canvasBlur");
  let canvas2 = document.querySelector("#canvasTest");

  let ctx = canvas.getContext('2d');
  let ctx1 = canvas1.getContext('2d');
  let ctx2 = canvas2.getContext('2d');

  //photo = document.getElementById('photo');


  var localMediaStream = null;
  var lab = -1;
  var x1 = 30,y1=30,x2=250,y2=250

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

  let ksize = new cv.Size(5, 5);

  let low = new cv.Mat(x2, y2, 16, [0,20,70,1]);
  let high = new cv.Mat(x2, y2, 16, [20,255,255,1]);


  function sendSnapshot() {
    if (!localMediaStream) {
      return;
    }
    ctx.canvas.width = video.videoWidth
    ctx.canvas.height = video.videoHeight
    ctx.drawImage(video, 0, 0);
    ctx.beginPath();
    ctx.lineWidth = "0";
    ctx.strokeStyle = "limegreen";
    ctx.rect(x1, y1, x2, y2);
    ctx.stroke();

    if (lab===-1) {
      ctx.font = "27px Comic Sans MS";
      ctx.fillStyle = "red";
      ctx.fillText("I am not sure !", 55, 25);
      
    } else {
      ctx.font = "27px Comic Sans MS";
      ctx.fillStyle = "green";
      ctx.fillText(lab, 35, 25);
    }

    ctx1.canvas.width = x2
    ctx1.canvas.height = y2
    

    let src = cv.imread('canvasElement');
    let dst = new cv.Mat();
    let rect = new cv.Rect(x1, y1, x2, y2);
    let hsv1 = new cv.Mat();
    let hsv = new cv.Mat();

    dst = src.roi(rect);
    cv.imshow('canvasTest', dst);
    cv.cvtColor(dst, hsv1, cv.COLOR_RGBA2RGB)
    cv.cvtColor(hsv1, hsv, cv.COLOR_RGB2HSV)  
    cv.inRange(hsv, low, high, hsv1);
    cv.GaussianBlur(hsv1, dst, ksize, 0, 0, cv.BORDER_DEFAULT);

    cv.imshow('canvasBlur', dst);

    src.delete();
    dst.delete();
    hsv.delete(); 
    hsv1.delete();

    let dataURL = canvas2.toDataURL('image/jpeg');

    socket.emit('input image', dataURL);

    var img = new Image();
    socket.on('out-image-event',function(data){
      lab = parseInt(data.label)


      /*
      image from python to src of an image tag in html
      img.src = dataURL//data.image_data
      photo.setAttribute('src', data.image_data);
      */

    });

  }


  var constraints = {
    video: {
      width: { min: 640, max: 1920 },
      height: { min: 400, max: 1080 }
    }
  };

  navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
    video.srcObject = stream;
    localMediaStream = stream;

    setInterval(function () {
      sendSnapshot();
    }, 0);
  }).catch(function(error) {
    console.log(error);
  });
});

