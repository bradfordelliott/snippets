import string

template_html = string.Template('''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
      class="translated-ltr">
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>$title</title>
<meta name="keywords" content="">
<meta name="description" content="">
<!--<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/smoothness/jquery-ui.css">-->
<link rel="stylesheet" href="/css/theme.css" type="text/css">
<link rel="stylesheet" href="/css/split-pane.css" />
<link rel="stylesheet" href="/codemirror/lib/codemirror.css">
<link rel="stylesheet" href="/codemirror/addon/hint/show-hint.css">

<!--<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>-->
<script src="/js/jquery-1.7.min.js"></script>
<script type="text/javascript" src="/js/split-pane.js"></script>

<!--<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>-->
<script type="text/javascript" src="/js/jquery.jeditable.js" charset="utf-8"></script>
<script type="text/javascript" src="/js/snippets.js" charset="utf-8"></script>

<script src="/codemirror/lib/codemirror.js"></script>
<script src="/codemirror/addon/mode/simple.js"></script>
<script src="/codemirror/addon/hint/show-hint.js"></script>

<style>
$styles
.CodeMirror {border-top: 1px solid black;border-bottom:1px solid black; margin-left:20px; margin-right:20px; height:auto;clear:both;}
.cm-tab {
         background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAMCAYAAAAkuj5RAAAAAXNSR0IArs4c6QAAAGFJREFUSMft1LsRQFAQheHPowAKoACx3IgEKtaEHujDjORSgWTH/ZOdnZOcM/sgk/kFFWY0qV8foQwS4MKBCS3qR6ixBJvElOobYAtivseIE120FaowJPN75GMu8j/LfMwNjh4HUpwg4LUAAAAASUVORK5CYII=);
         background-position: right;
         background-repeat: no-repeat;
      }

</style>

<script type="text/JavaScript">

$script

function expense_add()
{
    $$.get("/expenses/add", {}, function(data) {
        location.reload();
    });

    return false;
}

function expense_delete(eid)
{
    var resp = confirm("Are you sure you want to delete this expense?");
    if(resp == true) {
        $$.get("/expenses/delete", {"id":eid}, function(data) {
            location.reload();
        });
    }

    return false;
}

$$(document).ready(function() {
    //fetch_images();
    // setInterval(function () {fetch_images();}, 5000);
});

</script>
</head>

<body $onload>
<div id='page_wrapper'>
  <header>
     <!--<img src="/css/logo.png" style='position:absolute;height:50px;'></img>-->
     <div id="menu_div">
         <ul>
             <li><a href='/snippets'><div>Home</div></a></li>
             <li style='float:right;'><a href='/system/about'><div>About v${version}</div></a></li>
         </ul>
     </div>
  </header>
  <div id='content_wrapper'>
    <!--<input type='button' value='fullscreen' onclick='go_fullscreen();'/><br/>-->
    <div id='photos' style='height:100%;width:100%;overflow:scroll;'>
    $body
    </div>
  </div>

<!--
  <div id='nav_wrapper' style='clear:both;'>
  </div>
-->
</body>
</html>
''')
