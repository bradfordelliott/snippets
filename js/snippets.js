

$(document).ready(function() {
  $('#loading').css({opacity:0.8});
});

$(document).ajaxStart(function() {
  $('#loading').show();
}).ajaxStop(function() {
  $('#loading').hide();
});

var hostname="127.0.0.1"; /* macbookpro.Home";*/
var port=8084;
var FORMAT_PDF="pdf";
var FORMAT_HTML="html";


/**
 * This method is used to convert a shorte source document
 * into it's output format.
 *
 * @param editor [I] - The codemirror instance
 * @param format [I] - The output format (FORMAT_PDF or FORMAT_HTML)
 */
function generate(editor, format)
{
    $.post("http://" + hostname + ":" + port + "/shorte/" + format, {data: editor.getValue()})
        .done(function(data) {
             var result = window.open();
             if(result == undefined)
             {
                 alert("Failed opening a new window, you'll need to disable popups for this site");
             }
             else
             {
                 result.document.write(data);
                 if(format == FORMAT_PDF)
                 {
                    window.location = "http://" + hostname + ":" + port + "/shorte/pdfget";
                 }
             }
        })
        .fail(function(xhdr, status, error) {
            var msg = "Failed connecting to shorte server at " + hostname + " on port " + port + "<br/></br>" +
                  "Try starting the shorte server:<br/><pre> shorte --server --port=8084 --srv_format=web</pre>";
            var lbl = document.getElementById('warning_message');
            lbl.innerHTML = msg;
            $('#warning').show();
        });
}

function snippet_open(id)
{
    window.location.href = "/snippets/edit?id=" + id;
}

function snippet_save(id)
{
    $.post("/snippets/save", {"id" : id, "data" : editor.getValue()}, function(data) {
        location.reload();
    });
    return false;
}

function snippet_add()
{
    $.post("/snippets/add", {}, function(data) {
        window.location.href = data;
    });
    return false;
}
