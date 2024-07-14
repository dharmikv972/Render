<!doctype html>
<html lang="en">
<head>
    <title>Bootstrap Demo</title>
    <link href="bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=2.0">
    <title>Loader Example</title>
    <style>
        #content {
            display: none;
        }
    </style>
</head>
<body>

<div id="loader">
    <?php include 'loader.html'; ?>
</div>

<div id="content">
   
    <?php include 'navbar.html';
    include 'dashboard.html';
    include 'modal2.html';
     ?>
</div>

<script>
    // Show loader for 3 seconds and then display content
    setTimeout(function() {
        document.getElementById('loader').style.display = 'none';
        document.getElementById('content').style.display = 'block';
    }, 3000);
</script>

<script src="bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>