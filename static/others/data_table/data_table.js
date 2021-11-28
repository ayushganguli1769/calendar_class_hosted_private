$(document).ready(function() {
  $('#example').DataTable();
} );

function showData(){
    /*
      var html = '';
    if ($.fn.DataTable.isDataTable('#example')){
       // destroy table
        $('#example').DataTable().destroy();
    }
      //  create tr td 
      Object.keys(data).forEach(function(key) {
          html += '<tr>'; 
          html += '<td>'+data[key].ID+'</td>';
          html += '<td>'+data[key].Nama+'</td>';
          html += '<td>'+data[key].Age+'</td>'; 
          html += '</tr>';
      });
      $('#showData').html(html);
      // create table
      */
      $("#example").dataTable();
  }

var data = [
    {
          'ID':1,
          'Nama' : 'SAYA',
          'Age' : 21,
      },
      {
          'ID':2,
          'Nama' : 'SIAPA',
          'Age' : 24,
      },
      {
          'ID':3,
          'Nama' : 'KAMU',
          'Age' : 33,
      }
  ];
