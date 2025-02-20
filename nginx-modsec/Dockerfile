# Usa l'immagine ufficiale di Nginx come base
FROM nginx:latest

# Installa le dipendenze necessarie per compilare ModSecurity e il modulo Nginx
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libpcre3 \
    libpcre3-dev \
    libpcre2-dev \ 
    libssl-dev \
    libtool \
    autoconf \
    automake \
    curl \
    libcurl4-openssl-dev \
    libxml2 \
    libxml2-dev \
    liblua5.3-dev \
    pkg-config \
    zlib1g-dev \
    wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Clona e compila ModSecurity v3
WORKDIR /usr/src
RUN git clone --depth 1 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity
WORKDIR /usr/src/ModSecurity
RUN git submodule init && git submodule update
RUN ./build.sh && ./configure && make -j$(nproc) && make install

# Clona e compila il modulo Nginx per ModSecurity
WORKDIR /usr/src
RUN git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git

# Ottieni la versione di Nginx correttamente
RUN export NGINX_VERSION=$(apt-cache show nginx | grep 'Version:' | head -n 1 | awk '{print $2}' | cut -d'-' -f1) && \
    wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz && \
    tar -xvzf nginx-${NGINX_VERSION}.tar.gz

# Configura e compila Nginx con il modulo ModSecurity
WORKDIR /usr/src/nginx-${NGINX_VERSION}
RUN ./configure \
    --with-compat \
    --with-pcre \
    --add-dynamic-module=../ModSecurity-nginx && \
    make modules && \
    cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules/

# Esponi le porte 80 (HTTP) e 443 (HTTPS)
EXPOSE 80 443

# Avvia Nginx
CMD ["nginx", "-g", "daemon off;"]
