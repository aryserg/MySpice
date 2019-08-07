# MySpice
Маленькая обёртка над PySpice для работы с ngspice.
# Instalation
Установка проверялась на Ubuntu 19.04. PySpice по умолчанию требует ngspice как разделяемую библиотеку. Ngspice в свою очередь в репозитории такую библиотеку не поставляет, нужно собирать самому. Ставим тулчейн и необходимые dev пакеты:

`sudo apt install -y libreadline-dev make build-essential wget python3-pip`

Собираем ngspice:

```
wget http://sourceforge.net/projects/ngspice/files/ng-spice-rework/30/ngspice-30.tar.gz
tar -xvzf ./ngspice-30.tar.gz
cd ./ngspice-30/
./configure --prefix=/usr/local --enable-xspice --disable-debug --enable-cider --with-readline=yes --enable-openmp --with-ngshared
make -j4
sudo make install
sudo ldconfig
``` 
