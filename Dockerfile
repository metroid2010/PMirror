FROM python:3-stretch
MAINTAINER metroid2010

# install dependencies
RUN apt-get update && apt-get install -y \
   git \
   wget \
   openjdk-8-jdk-headless \
   libssl-dev \
   libffi-dev \
   unzip \
   nginx

# more dependencies (mainly gpapi)
ADD requirements.txt .
RUN pip3 install -r requirements.txt
# need a fix, the pr has not been merged yet
ADD fix_gpapi.sh .
RUN bash fix_gpapi.sh

# android platform tools dl and conf
RUN mkdir /opt/android-sdk-linux
RUN wget https://dl.google.com/android/repository/sdk-tools-linux-3859397.zip \
    && echo "444e22ce8ca0f67353bda4b85175ed3731cae3ffa695ca18119cbacef1c1bea0  sdk-tools-linux-3859397.zip" | sha256sum -c \
    && unzip sdk-tools-linux-3859397.zip \
    && rm sdk-tools-linux-3859397.zip
RUN echo 'y' | tools/bin/sdkmanager --sdk_root=/opt/android-sdk-linux "platforms;android-26" \
    && tools/bin/sdkmanager --sdk_root=/opt/android-sdk-linux "build-tools;26.0.1" \
    && tools/bin/sdkmanager --sdk_root=/opt/android-sdk-linux "platform-tools"\
    && tools/bin/sdkmanager --sdk_root=/opt/android-sdk-linux "tools" \
    && rm -rvf tools

# install fdroid-server fresh from source
RUN git clone --depth 1 https://gitlab.com/fdroid/fdroidserver.git \
    && cd fdroidserver \
    && pip3 install --no-binary python-vagrant -e . \
    && python3 setup.py compile_catalog build \
    && python3 setup.py install

# copy nginx conf
COPY nginx.conf /etc/nginx/nginx

# change to nonpriviledged user
RUN groupadd -g 1001 fdroid-user && useradd -g 1001 -u 1001 fdroid-user
RUN mkdir -v /data && chown -v 1001:1001 /data
USER fdroid-user
# environment variables for the android-sdk
ENV ANDROID_HOME=/opt/android-sdk-linux
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# make the directories por the repo and pmirror
RUN mkdir -pv /data/fdroid/repo && \
    mkdir -pv /data/pmirror 

# TODO: init repo

# populate pmirror folder
WORKDIR /data/pmirror
ADD pmirror/* .

# pmirror configuration file
VOLUME /data/pmirror/pmirror.conf
# repo (mount the parent, because theres useful stuff in there, like logs and stuff)
VOLUME /data/fdroid

ENTRYPOINT /data/pmirror/run.sh
