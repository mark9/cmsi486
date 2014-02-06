<!doctype HTML>
<html>

<head><title>Notes Database</title></head>

<body>

Welcome to the notes database<br>
This is the view a note page<p>
{{errors}}

To look at a different table: (click here for contacts, calendar, etc)<br>

<h2>View Note</h2>


<a href="/notesmain">return to home</a><br>
search notes(doesnt work yet)<br>
<br>
Displaying note number {{id}}<br>
view note:
<a href="/notes/{{id-1}}">previous</a> <a href="/notes/{{id+1}}">next</a>
<br><br><hr>

{{text}}<br>
<hr><br>

tags:
%for tag in tags:
<a href="/tags/{{tag}}">{{tag}}</a> 
%end
<br><br>
created {{creation_date}}
<br><br>
<a href="/notes/{{id}}">edit note {{id}} (doesnt work yet)</a><br>

</body>
</html>