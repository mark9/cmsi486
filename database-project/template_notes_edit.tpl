<!doctype HTML>
<html>

<head><title>Notes database</title></head>

<body>
<a href="/notesmain">return to home</a><br>
<form action="/tags/new" method="get">
{{errors}}
<br><br>
view note:<br>
<a href="/notes/{{id-1}}">previous</a>      <a href="/notes/{{id+1}}">next</a>
<br>
<br>
<h2>Edit Note</h2>
id number: {{id}}
<br>
{{text}}
<br>
<br>tags: 
%for tag in tags:
<a href="/tags/{{tag}}">{{tag}}</a> 
%end
<br>
<br>
created: {{date_created}}
<br>
<br>
Add new tags. Comma separated.<br>
<input type="text" name="tags" size="120" value=""><br>

<p>
<input type="submit" value="submit">

</body>
</html>