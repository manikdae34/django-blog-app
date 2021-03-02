

var script = document.createElement('script');
script.type = 'text/javascript';
script.src = "https://cdn.tiny.cloud/1/u6d6drp5f5nqzvqu6eujg1dnek4vrscdre339fvjpf0ik7bw/tinymce/5/tinymce.min.js"
script.referrerpolicy = 'origin'
document.head.appendChild(script);

script.onload = function(){

tinymce.init({
	selector: '#id_content',
	height: 456,
	plugins: [
  'advlist autolink link image lists charmap print preview hr anchor pagebreak',
  'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
  'table emoticons template paste help maxchars'
],
toolbar: 'fullscreen | undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | ' +
  'bullist numlist outdent indent | link image | print preview media fullpage | ' +
  'forecolor backcolor emoticons | uploadimage help ',

paste_data_images: true,

images_upload_handler: function (blobInfo, success, failure) {
	        // no upload, just return the blobInfo.blob() as base64 data
	        success("data:" + blobInfo.blob().type + ";base64," + blobInfo.base64());
	      },

menu: {
  favs: {title: 'My Favorites', items: 'code visualaid | searchreplace | emoticons'}
},
menubar: 'favs file edit view insert format tools table help',
content_css: 'css/content.css'
  });
  
};

tinymce.PluginManager.add("bdesk_photo", function(editor, f) {
	editor.addCommand("bdesk_photo", function() {
		editor.windowManager.open({
			title: "Insert embedded image",
			width: 450,
			height: 80,
			html: '<input type="file" class="input" name="single-image" style="font-size:14px;padding:30px;" accept="image/png, image/gif, image/jpeg, image/jpg"/>',
			buttons: [{
				text: "Ok",
				subtype: "primary",
				onclick: function() {
					if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
						alert("This feature needs a modern browser.");
						(this).parent().parent().close();
						return;
					}

					var imagefile = document.getElementsByName("single-image")[0].files;

					if (imagefile.length <= 0) {
						// do nothing
						(this).parent().parent().close();
						return;
					}

					if (imagefile[0].size > 512 * 1024) {
						alert("The image cannot be larger than 500KB.");
						return;
					}

					var thisOne = this;

					var classFilereader = new FileReader();
					classFilereader.onload = function(base64) {
						var imgData = base64.target.result;
						var img = new Image();
						img.src = imgData;

						editor.execCommand("mceInsertContent", false, "<img src='" + imgData + "' />");
						thisOne.parent().parent().close();
					};

					classFilereader.onerror = function(err) {
						alert("Error reading file - " + err.getMessage());
					};

					classFilereader.readAsDataURL(imagefile[0]);
				}
			}, {
				text: "Cancel",
				onclick: function() {
					(this).parent().parent().close();
				}
			}]
		});
	});

	editor.addButton("bdesk_photo", {
		icon: "image",
		context: "insert",
		title: "Insert embedded image",
		cmd: "bdesk_photo"
	});

	editor.addMenuItem("bdesk_photo", {
		cmd: "bdesk_photo",
		context: "insert",
		text: "Insert embedded image",
		icon: "image",
		prependToContext: true
	});
});
