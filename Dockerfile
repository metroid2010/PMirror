FROM python:3-stretch
MAINTAINER metroid2010

RUN apt-get update && apt-get install -y \
   git \
   wget \
   openjdk-8-jdk-headless \
   libssl-dev \
   libffi-dev \
   unzip \
   nginx

# android platform tools dl and conf
RUN mkdir /opt/android-sdk-linux
RUN wget https://dl.google.com/android/repository/sdk-tools-linux-3859397.zip \
    && echo "444e22ce8ca0f67353bda4b85175ed3731cae3ffa695ca18119cbacef1c1bea0  sdk-tools-linux-3859397.zip" | sha256sum -c \
    && unzip sdk-tools-linux-3859397.zip \
    && rm sdk-tools-linux-3859397.zip
ENV ANDROID_HOME=/opt/android-sdk-linux
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
RUN echo 'y' | tools/bin/sdkmanager --sdk_root=/opt/android-sdk-linux "platforms;android-26" \
    && tools/bin/sdkmanager --sdk_root=/opt/android-sdk-linux "build-tools;26.0.1" \
    && tools/bin/sdkmanager --sdk_root=/opt/android-sdk-linux "platform-tools"\
    && tools/bin/sdkmanager --sdk_root=/opt/android-sdk-linux "tools" \
    && rm -rvf tools

# fdroid server, fresh from source
RUN git clone --depth 1 https://gitlab.com/fdroid/fdroidserver.git \
    && cd fdroidserver \
    && pip3 install --no-binary python-vagrant -e . \
    && python3 setup.py compile_catalog build \
    && python3 setup.py install

RUN mkdir -pv /data/fdroid/repo && \
    mkdir -pv /data/pmirror 

# populate pmirror folder
WORKDIR /data/pmirror
COPY download_app.py .
COPY search_app.py .
COPY login.py .
COPY fix_gpapi.py .

# other conf files
COPY nginx.conf /etc/nginx/nginx

RUN pip install -r requirements.txt

VOLUME /data/fdroid

ENTRYPOINT 
