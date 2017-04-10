<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>MQTT WebViewer</title>
		<script src="https://code.jquery.com/jquery-3.2.0.min.js"></script>
		<script src="https://mbraak.github.io/jqTree/tree.jquery.js"></script>
        <link rel="stylesheet" src="https://mbraak.github.io/jqTree/jqtree.css"></link>
    </head>
    <body>
	    <h1> MQTT WebViewer</h1>
		<div id="topic_tree"></div>
		<script>
		  $.getJSON(
			'/get_topics',
			function(data) {
				$('#topic_tree').tree({
					data: data,
					autoOpen: true
				});
			}
		 ); 

		 function update(){
		  $.getJSON(
			'/get_topics',
			function(data) {
				$('#topic_tree').tree(
				'loadData',
				data
				);
			}
		 ); 
	     }
		 setInterval(update, 1000);
		</script>
    </body>
</html>
