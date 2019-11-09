FROM python:3-stretch
MAINTAINER metroid2010

RUN apt-get update && apt-get install -y \
   git \
   wget \
   openjdk-8-jdk-headless \
   libssl-dev \
   libffi-dev \
   fdroidserver \
   unzip

RUN wget https://dl.google.com/android/repository/sdk-tools-linux-3859397.zip \
    && echo "444e22ce8ca0f67353bda4b85175ed3731cae3ffa695ca18119cbacef1c1bea0  sdk-tools-linux-3859397.zip" | sha256sum -c \
    && unzip sdk-tools-linux-3859397.zip \
    && rm sdk-tools-linux-3859397.zip
RUN mkdir /opt/android-sdk-linux
ENV ANDROID_HOME=/opt/android-sdk-linux
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
RUN echo 'y' | tools/bin/sdkmanager --sdk_root=/opt/android-sdk-linux --verbose "platforms;android-26" \
    && tools/bin/sdkmanager --sdk_root=/opt/android-sdk-linux --verbose "build-tools;26.0.1" \
    && rm -rf tools

RUN mkdir -pv /data/fdroid/repo && \
    mkdir -pv /data/pmirror

COPY ./* /data/pmirror/

WORKDIR /data/pmirror

RUN pip install -r requirements.txt

VOLUME /data/fdroid
