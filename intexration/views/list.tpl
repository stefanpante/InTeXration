<!doctype html>

<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="InTeXration">
	<meta name="author" content="InTeXration">

	<title>InTeXration</title>

	<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{base_url}}css/style.css">
</head>

<body>
<div class="container">
	<ul>
	% for identifier in documents:
	    <div class="document">
	    <h2>{{identifier}}</h2>
		<ul>
            <li><a href="{{base_url}}pdf/{{identifier.owner}}/{{identifier.repository}}/{{identifier.name}}">PDF</a></li>
            <li><a href="{{base_url}}log/{{identifier.owner}}/{{identifier.repository}}/{{identifier.name}}">LOG</a></li>
        </ul>
        </div>
	% end

</div>
</body>
</html>