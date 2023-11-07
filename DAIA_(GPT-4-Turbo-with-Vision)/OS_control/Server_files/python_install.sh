#!/bin/bash

# Check the operating system
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     os="linux";;
    Darwin*)    os="mac";;
    CYGWIN*|MINGW*|MSYS*)    os="windows";;
    *)          os="unknown";;
esac

# Determine the download URL based on the operating system
if [ "${os}" = "linux" ]; then
    url="https://www.python.org/ftp/python/3.x.x/Python-3.x.x.tgz"  # Replace 3.x.x with the desired version
    
elif [ "${os}" = "mac" ]; then
    url="https://www.python.org/ftp/python/3.x.x/python-3.x.x-macosx10.x.pkg"  # Replace 3.x.x with the desired version

elif [ "${os}" = "windows" ]; then
    url="https://www.python.org/ftp/python/3.x.x/python-3.x.x.exe"  # Replace 3.x.x with the desired version

else
    echo "Unsupported operating system."
    exit 1
fi

# Download and install Python
echo "Downloading Python..."
curl -o python-installer.${ext} ${url}  # Replace python-installer.${ext} with the desired output file name and extension

echo "Installing Python..."

if [ "${os}" = "linux" ]; then
    tar -xzvf python-installer.${ext}  # Extract the downloaded tarball
    cd Python-3.x.x/  # Replace Python-3.x.x with the extracted directory name
    ./configure --enable-optimizations
    make -j8
    sudo make altinstall

elif [ "${os}" = "mac" ]; then
    sudo installer -pkg python-installer.${ext} -target /  # Replace python-installer.${ext} with the downloaded package file name

elif [ "${os}" = "windows" ]; then
    python-installer.${ext}  # Replace python-installer.${ext} with the downloaded installer file name

else
    echo "Unsupported operating system."
    exit 1
fi

# Verify the installation
echo "Python installation completed."
python3 --version