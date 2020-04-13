
(function($) {
	$(document).ready(function() {

    var modal = $("#myModal"); // Get the modal
    var close = $(".close");   // Get the <span> element that closes the modal
	var couper = $("#couper"); // Get the 'couper' element

// close button
	close.on('click',function(){
		modal.hide();
	});

// When the user clicks on the couper button, close the modal
	couper.on('click',function(){
		modal.hide();
	});

// When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        updateCoords;
        modal.style.display = "none";
      }
    }

// function to show Coords (e.g. using console.log() )
    function showCoords(c)
      {
          // variables can be accessed here as
          // c.x, c.y, c.x2, c.y2, c.w, c.h
      };

// function to update coordinates as elements values
    function updateCoords(c)
      {
          $("#id_x").val(c.x);
          $("#id_y").val(c.y);
          $("#id_w").val(c.w);
          $("#id_h").val(c.h);
      };

// init Jcrop
    function initJcrop( nouvelle_image ){
      $('#target').Jcrop({ },function(){
        new_jcrop = this;

        new_jcrop.setImage( nouvelle_image );
        new_jcrop.setOptions({
              onSelect: showCoords,
              onChange: updateCoords,
              viewMode: 1,
              aspectRatio: 1,
              bgOpacity: .4,
              boxWidth: 600,   // Maximum width you want for  bigger images
              boxHeight: 400,  // Maximum Height for bigger images
              minSize: [200, 200],
              setSelect: [ 0, 0, 200, 200 ]
        });
      });
    };

// function to initialise Jcrop and contains all parameters
    $("#id_picture").on("input", function () {
    $('#target').unbind();

      if (this.files && this.files[0]) {

        var reader = new FileReader();

        reader.onloadend = function (e) {

          $("#target").attr("src", e.target.result);
          $(".jcrop-holder img").attr("src", e.target.result);
          $("#myModal").show();

          initJcrop(e.target.result);
        }
        reader.readAsDataURL(this.files[0]);
      }
    });

	});
}(window.jQuery || window.$));

