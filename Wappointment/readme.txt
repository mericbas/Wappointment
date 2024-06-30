Sunucu localhost ve IPV4 adresinizde başlatılır. 
Bilgisayarınızda başlattığınız bu sunucuya farklı ağlardan bağlanılabilmesi için modem arayüzünüzden cmd de yazan IPV4 adresinize 80 portunu açmanız gerekmektedir.
Gösterilen 2. adres IPV4 adresiniz olup, 1. adres ise sizin localhost unuzdur.

Dilerseniz dilediğiniz IP adresini app.py dosyasından en altta bulunan satırda düzenleyebilirsiniz.

Excel dosyalarının okunmasında bir problem olduğu takdirde data klasöründe bulunan excel dosyalarını silip sunucuyu start.bat üzerinden yeniden başlatın.
Dosyalar otomatik olarak tekrar oluşturulacaktır.

Sunucuyu start.bat programı üzerinden başlatın veya Komut İstemi üzerinden "python app.py" komutu ile başlatabilirsiniz.

Sunucunun çalışması için bilgisayarınızda bazı programların kurulu olması gerekmektedir.
Gerekli programlar ve kurulumları "installation_files.txt" dosyasında belirtilmiştir.

Static/manifest.json
dosyasındaki IP adresinize sunucu ip adresini yazın.

--------------------------------------------------------------------------------

Start the server on localhost and your IPV4 address. To allow connections from different networks to the server you started on your computer, you need to open port 80 on your modem interface with the IPV4 address shown in the command prompt (CMD). The second address shown is your IPV4 address, while the first address is your localhost.

You can edit any IP address you prefer in the app.py file at the bottom.

If there are any issues reading Excel files, delete the Excel files in the data folder and restart the server using start.bat. The files will be recreated automatically.

Launch the server using start.bat or via Command Prompt with the command 'python app.py'.

Certain programs need to be installed on your computer for the server to run properly. The required programs and their installations are specified in the 'installation_files.txt' file.
Static/manifest.json
Write the server IP address to your IP address in the file.