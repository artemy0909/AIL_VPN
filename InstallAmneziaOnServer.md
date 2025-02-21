# 📌 Памятка по созданию Amnezia WG сервера

✅ **Проверено на Ubuntu 22.04**

---

## 🔗 Подключение к серверу

```sh
ssh root@<ip>
```

Введите пароль.

Если не под рутом, выполните:

```sh
sudo su
```

---

## ⚙️ Настройка системы

Перейдите в домашнюю директорию:

```sh
cd ~
```

Подключаем полный список репозиториев:

```sh
cp -f /etc/apt/sources.list /etc/apt/sources.list.backup
sed "s/# deb-src/deb-src/" /etc/apt/sources.list.backup > /etc/apt/sources.list
```

Обновляем систему:

```sh
apt update -y && apt upgrade -y
```

Разрешаем маршрутизацию трафика:

```sh
echo "net.ipv4.ip_forward = 1" > /etc/sysctl.d/00-amnezia.conf
```

Перезагружаем систему:

```sh
reboot
```

---

## 📂 Проверка свободного места

Убедитесь, что на диске свободно минимум 1.5GB:

```sh
df -h
```

После перезагрузки снова войдите под рутом:

```sh
sudo su
```

---

## 📥 Установка Amnezia WG

Создаём директорию и переходим в неё:

```sh
mkdir -p ~/awg
cd ~/awg
```

Добавляем репозиторий и устанавливаем пакет Amnezia WG:

```sh
add-apt-repository -y ppa:amnezia/ppa
apt install -y amneziawg
```

---

## 🔍 Проверка установки

Проверяем версию установленного пакета:

```sh
awg --version
```

Проверяем наличие драйверов в системе:

```sh
lsmod | grep amnezia
```

Ожидаемый вывод:

```
amneziawg              98304  0
curve25519_x86_64      36864  2 amneziawg,wireguard
libchacha20poly1305    16384  2 amneziawg,wireguard
libcurve25519_generic  49152  3 amneziawg,curve25519_x86_64,wireguard
ip6_udp_tunnel         16384  2 amneziawg,wireguard
udp_tunnel             20480  2 amneziawg,wireguard
```

Если драйвер **amneziawg** не загружен, попробуйте выполнить:

```sh
modprobe amneziawg
```

Проверяем актуальность версии драйвера:

```sh
modinfo amneziawg | grep ver
```

Ожидаемый вывод:

```
version:        1.0.0
srcversion:     5C0E002076C0223605D8472
vermagic:       5.15.0-118-generic SMP mod_unload modversions
```

---

## 🛠 Установка и настройка WGDashboard

Перейдите в домашнюю директорию:

```sh
cd ~
```

Создаем папку:

```sh
mkdir wgd
```

Заходим в папку:

```sh
cd ./wgd
```

Устанавливаем WGDashboard (обязательно не ниже версии 4.2):

```sh
sudo apt-get update -y && \
sudo apt install wireguard-tools net-tools --no-install-recommends -y && \
git clone https://github.com/donaldzou/WGDashboard.git && \
cd ./WGDashboard/src && \
chmod +x ./wgd.sh && \
./wgd.sh install && \
sudo echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf && \
sudo sysctl -p /etc/sysctl.conf
```

Запускаем:

```sh
./wgd.sh install
```

---

## 🔒 Настройка SSL/TLS

Обновите список пакетов:

```sh
sudo apt update
```

Установите Certbot:

```sh
sudo apt install certbot
```

Создайте сертификаты:

```sh
sudo certbot certonly --config ./certbot.ini -d <домен>
```

Откройте файл **ssl-tls.ini** в любимом редакторе, укажите абсолютный путь к вашему сертификату и закрытому ключу, например:

```ini
[SSL/TLS]
certificate_path = /etc/letsencrypt/live/<домен>/fullchain.pem
private_key_path = /etc/letsencrypt/live/<домен>/privkey.pem
```

Если вы создавали сертификат с помощью Certbot, вы можете найти путь с помощью команды:

```sh
certbot certificates
```

Запустите WGDashboard:

```sh
./wgd.sh start
```

Ожидаемый вывод:

```
[Gunicorn][HTTPS] Found certificate and private key file
[Gunicorn][HTTPS] Certificate: /etc/letsencrypt/live/<домен>/fullchain.pem
[Gunicorn][HTTPS] Private Key: /etc/letsencrypt/live/<домен>/privkey.pem
...
[WGDashboard] WGDashboard w/ Gunicorn started successfully
```

🚀 \*\*Попробуйте открыть WGDashboard по HTTPS и проверьте его работу!&#x20;
