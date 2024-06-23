$(document).ready(function(){
    
    // Handle form submission
    $('#predictionForm').submit(function(event){
        event.preventDefault();
        $.ajax({
            url: '/predict',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                region: $('#region').val(),
                kecamatan: $('#kecamatan').val(),
                "Kamar Tidur": $('#KamarTidur').val(),
                "Kamar Mandi": $('#KamarMandi').val(),
                "Luas Tanah": $('#LuasTanah').val(),
                "Luas Bangunan": $('#LuasBangunan').val(),
                "Daya Listrik": $('#DayaListrik').val() ,
                "Dapur": $('#JumlahDapur').val(),
                "Jumlah Lantai": $('#JumlahLantai').val(),
                "Lebar Jalan": $('#LebarJalan').val(),
                "Carport": $('#MuatanGarasi').val(),
                "Kamar Pembantu": $('#KamarPembantu').val(),
                "Ruang Makan": $('#RuangMakan').val(),
                "Ruang Tamu": $('#RuangTamu').val(),
                "Kondisi Perabotan": $('#KondisiPerabotan').val(),
                "Terjangkau Internet": $('#TerjangkauInternet').val(),
                "Hook": $('#Hook').val(),
                "Kondisi Properti":$('#KondisiProperti').val(),
                "Sertifikat":$('#Sertifikat').val(),
                "water_source":$('#SumberAir').val(),
                // Add other input fields here
            }),
            success: function(response){
                $('#predictionResult').text('Perkiraan Harga Rumah Pasaran: ' + response.prediction);
            }
        });
    });
});

