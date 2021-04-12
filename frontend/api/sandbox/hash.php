
<?php
/**
 * We just want to hash our password using the current DEFAULT algorithm.
 * This is presently BCRYPT, and will produce a 60 character result.
 *
 * Beware that DEFAULT may change over time, so you would want to prepare
 * By allowing your storage to expand past 60 characters (255 would be good)
 */
if( isset($_POST['hash'])) {
	echo $_POST['hash'] . "<br>";
	echo password_hash($_POST['hash'], PASSWORD_DEFAULT);
}
?>


<html>
<body>

<form method="POST">
  <p>Enter password to hash:</p>
  <input type="hash" name="hash">
  <button type="submit">Submit</button>
</form>

</body>
</html>