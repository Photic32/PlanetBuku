function updateDisplay(){
    fetch("{% url 'daftar_peminjam:get_all_user_json' %}").then(
     response => response.json()
    ).then(
     data => {
         var i = 1;
         var isiTable = 
         `<tr>
             <th>No</th>
             <th>Username</th>
             <th>Jumlah Buku Dipinjam</th>

             <th>Aksi</th>
         </tr>`;
         data.forEach(function(user){
             isiTable += "<tr>";
             isiTable += "<td>" + i + "</td>";
             isiTable += "<td>" + user.username + "</td>";
             isiTable += "<td>" + user.jumlah_buku_dipinjam + "</td>";
             
             url = "{% url 'daftar_peminjam:show_peminjam_individu' id=0 %}".replace('0', user.user_id);
             isiTable += `<td><a href="${url}" target="_blank">
                 <button class='btn-dark-red' >Lihat/Edit Buku Dipinjam</button>
                 </a></td>`;
             isiTable += "</tr>"
             i++;
         });
         document.getElementById("tabel-user").innerHTML = isiTable;
     }
    );
 }
 updateDisplay();
