function editData(id, title){
    const baseUrl = "{% url 'daftar_peminjam:get_pinjaman_json' id=0 %}";
    const url = baseUrl.replace('0', id);
    
    fetch(url).then(
        response => response.json()
    ).then(
        data => {
            $("#exampleModal").find(".modal-title").text("Extend Peminjaman : " + title + " Oleh " + "{{ peminjam.user.username }}");
            
            $("#exampleModal").find(".modal-body").html(
                `
                <form id="formEdit" onsubmit="submitForm(event, ${id})">
                    <div class="mb-3">
                        <label for="tanggal_pengembalian" class="form-label">Tanggal Pengembalian</label>
                        <input type="date" name="tanggal_pengembalian" class="form-control" id="tanggal_pengembalian" value="` + data[0].fields.tanggal_pengembalian + `">
                    </div>
                    <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Extend</button>
                </form>`)
        }
    );
    var modal = new bootstrap.Modal(document.getElementById('exampleModal'));
    modal.show();
}

function kembaliBuku(id, title){
    $("#exampleModal").find(".modal-title").text("{{ peminjam.user.username }}"+" akan mengembalikan buku : " + title);
    $("#exampleModal").find(".modal-title").css("color", "green");
    $("#exampleModal").find(".modal-body").html(
        `
            <h2 style="margin-bottom:30px">Apakah Anda Yakin?<h2>
            
            <button type="submit" class="btn btn-primary" data-bs-dismiss="modal" onclick="kembalikan(${id})">Kembalikan</button>
        `);
    var modal = new bootstrap.Modal(document.getElementById('exampleModal'));
    modal.show();
}

function kembalikan(id){
    fetch("{% url 'daftar_peminjam:kembali_buku' id=0 %}".replace('0', id)).then(
        response => response
    ).then(
        data => {
            if(data.status == 200){
                alert("Buku berhasil dikembalikan");
                updateDisplay();
            } else{
                alert("Buku gagal dikembalikan");
            }
        }
    );
}

// Make sure jQuery is included in your HTML before this script
function submitForm(event, id){
event.preventDefault();
const form = $("#formEdit")[0];
const formData = new FormData(form);
var formUrl = "{% url 'daftar_peminjam:edit_peminjaman' id=0 %}";
formUrl = formUrl.replace('0', id);

$.ajax({
    url: formUrl,
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,  
    success: function(response) {
        alert("Data berhasil diubah");
        updateDisplay({
            'title': '',
            'isbn': '',
            'author': '',
            'year': '',
            'publisher': '',
            'user_id': "{{ id }}",
        });
    },
    error: function(xhr, status, error) {
        alert("Data gagal diubah");
    }
});
}


async function updateDisplay(formData){
    $.ajax({
    type: 'GET',  
    url: "{% url 'daftar_peminjam:search_buku' %}",  // replace with your server-side search endpoint
    data: formData,
    dataType: 'json',  
    success: function(data) {
        let temp = `
        <table class="tableau" style="width:100%;">
            <tr>
                <th>Cover</th>
                <th>Judul</th>
                <th>Return Date</th>
                <th>Status</th>
                <th>Extend</th>
                <th>Kembalikan</th>
            </tr>`;

        data.buku_dipinjam.forEach(function(buku){
            temp += `
                <tr>
                    <td><img src="${buku.image}" alt="Image"></td>
                    <td><h5><strong>${buku.title}</strong></h5><p>${buku.author}</p><p>${buku.isbn}<p></td>
                    <td><p>${buku.deadline}</p></td>
                    <td><p>${buku.status}</p></td>
                    `
                if(buku.status == "dikembalikan"){
                    temp += `
                    <td><button class='btn btn-success' disabled>Buku Sudah Dikembalikan</button></td>
                    <td><button class='btn btn-success' disabled>Buku Sudah Dikembalikan</button></td>
                    `    
                } else{
                    temp +=
                `
                    <td><button class='btn btn-dark-red' onclick='editData("${buku.peminjaman_id}", "${buku.title}")'>Extend Peminjaman</button></td>
                    <td><button class='btn btn-dark-red' onclick='kembaliBuku("${buku.peminjaman_id}", "${buku.title}")'>Kembalikan Buku</button></td>
                </tr>`;
                }
        });

        temp += '</table>';
        document.getElementById("listBuku").innerHTML = temp;
    },
    error: function(jqXHR, textStatus, errorThrown) {
        // Handle error
        console.error("Search failed:", textStatus, errorThrown);
    }
    });
}

//awal2
updateDisplay({
    'title': '',
    'isbn': '',
    'author': '',
    'year': '',
    'publisher': '',
    'user_id': "{{ id }}",
});

$(document).ready(function() {
$('#book-search-form').submit(function(event) {
    // Prevent the default form submit action
    event.preventDefault();

    // Collect the form data
    let formData = {
    'title': $('#example-search-input').val(),
    'isbn': $('#isbn-search-input').val(),
    'author': $('#author-search-input').val(),
    'year': $('#publication-year-search-input').val(),
    'publisher': $('#publisher-search-input').val(),
    'user_id': $('#hidden_id').val(),
    };
    updateDisplay(formData);
});
});