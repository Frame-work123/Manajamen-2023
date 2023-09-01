<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Untitled Document</title>
<link href="sty_format.css" rel="stylesheet" type="text/css" />
</head>

<body>
<!-- Include jquery.js and jquery.mask.js -->
<script src="jqurey_format.js"></script>
<script src="jquery.mask.min.js"></script>
<script src="js_format.js"></script>

<!-- Input Form -->
<div class="container">
    <h3>Custom Format Input</h3>
    <br>
    <?php 
	if(isset($_POST['hitung'])){
	$a=$_POST['a'];
	$b=$_POST['b'];
	$total=$_POST['total'];
	$total=$a*$b;
	}
	?>
    <form action="#" method="post">
        <div class="group">
            <label>Rp</label>
            <input type="text" class="uang"  name="a" value="<?php echo $a?>">
        </div>
        <div class="group">
            <label>No. HP</label>
            <input type="text" class="no_hp">
        </div>
        <div class="group">
            <label>Tahun Pelajaran</label>
            <input type="text" class="tapel">
        </div>
        <div class="group">
            <label>b</label>
            <input type="text" name="b" value="<?php echo $b?>">
                        <label>ttl</label>
            <input type="text" name="total" class="uang" value="<?php echo $total?>000">
        </div>
       <input type="submit" name="hitung"  />
    </form>
</div>

</body>
</html>