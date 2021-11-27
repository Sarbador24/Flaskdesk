$(document).ready(function() {
  $('#table').DataTable({
    'ordering': false
  });

  new FroalaEditor('textarea#body, textarea#comment', {
    toolbarButtons: ['fontFamily', '|', 'bold', 'italic', 'underline', 'undo', 'redo', 'codeView'],
    fontFamilySelection: true,
    pluginsEnabled: ['fontFamily'],
    heightMin: 100,
    heightMax: 200
  });
  
  new PerfectScrollbar(".list-scrollbar");
  var nanobar = new Nanobar();
  nanobar.go(100);
});