var kecamatanData = {
    "Jakarta Timur": ["Matraman", "Pulo Gadung", "Jatinegara", "Duren Sawit", "Kramat Jati", "Makasar", "Cipayung", "Cakung", "Pasar Rebo", "Ciracas"],
    "Jakarta Pusat": ["Gambir", "Tanah Abang", "Menteng", "Senen", "Cempaka Putih", "Johar Baru", "Kemayoran", "Sawah Besar"],
    "Jakarta Selatan": ["Kebayoran Baru", "Kebayoran Lama", "Cilandak", "Pesanggrahan", "Pasar Minggu", "Jagakarsa", "Mampang Prapatan", "Pancoran", "Tebet", "Setiabudi"],
    "Jakarta Utara": ["Penjaringan", "Pademangan", "Tanjung Priok", "Koja", "Kelapa Gading", "Cilincing"],
    "Jakarta Barat": ["Cengkareng", "Grogol Petamburan", "Taman Sari", "Tambora", "Kebon Jeruk", "Kalideres", "Palmerah", "Kembangan"]
};

$(document).ready(function(){
    // Function to populate kecamatan options based on selected region
    function populateKecamatan(region) {
        // Clear existing options
        $('#kecamatan').empty();
        
        // Add default option
        $('#kecamatan').append($('<option>', {
            value: '',
            text: 'Choose kecamatan',
            disabled:"disabled"
        }));
        
        // Add options based on selected region
        if (region in kecamatanData) {
            $.each(kecamatanData[region], function(index, value){
                $('#kecamatan').append($('<option>', {
                    value: value,
                    text: value
                }));
            });
        }
    }
    
    // Event listener for region select change
    $('#region').change(function(){
        var selectedRegion = $(this).val();
        populateKecamatan(selectedRegion);
    });
});