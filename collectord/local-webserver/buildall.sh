#!/bin/bash
#
# Install Dependencies
#
# Elm
#
pushd /opt/installs/
mkdir -p /opt/installs/elm-install

  pushd /opt/installs/elm-install
  wget https://github.com/elm/compiler/releases/download/0.19.0/binary-for-linux-64-bit.gz
  gunzip binary-for-linux-64-bit.gz
  mv binary-for-linux-64-bit elm
  chmod +x elm
  sudo rm /usr/bin/elm
  sudo ln -s /opt/installs/elm-install/elm /usr/bin/elm
  popd
popd


pushd frontend
  pushd shell-history
  echo $(pwd)
  ./runner.sh
  popd

  pushd firefox-history
  echo $(pwd)
  ./runner.sh
  popd

  pushd context-summary
  echo $pwd
  ./runner.sh
  popd

  pushd context-viewer
  echo $pwd
  ./runner.sh
  popd

  pushd local-system-status
  echo $pwd
  ./runner.sh
  popd
popd

pushd backend
  echo $(pwd)
  go build
popd
