## TODO Test for dependency requirements
## TODO Test for existence of correct directories
#
#!/bin/bash
#
# Install Dependencies
#
# Elm
# Go
#
echo "***buildall.sh***"

install_DIR="/opt/installs"

elm_install_DIR="elm-install"
elm_VERSION_REQ="0.19.0"

go_install_DIR="go-install"

elm_install() {
  local DIR=${elm_install_DIR}
  echo "Installing elm at ${install_DIR}/${DIR}"
  if ! mkdir -p "${install_DIR}/${DIR}"; then
   return 2
  fi
  pushd ${DIR}
    echo $(pwd)
  local res=
    wget https://github.com/elm/compiler/releases/download/0.19.0/binary-for-linux-64-bit.gz &&
    gunzip binary-for-linux-64-bit.gz &&
    mv binary-for-linux-64-bit elm &&
    chmod +x elm &&
    (! find /usr/local/bin/elm 2>/dev/null || sudo rm /usr/local/bin/elm) &&
    sudo ln -s ${install_DIR}/${DIR}/elm /usr/local/bin/elm
  popd
  return $res
}

go_install() {
  local DIR=${go_install_DIR}
  echo "Installing go at ${install_DIR}/${DIR}"
  if ! mkdir -p "${install_DIR}/${DIR}"; then
   return 2
  fi
  pushd ${DIR}
    echo $(pwd)
  local res=
    wget https://golang.org/dl/go1.17.2.linux-amd64.tar.gz &&
    tar -xvzf go1.17.2.linux-amd64.tar.gz &&
    chmod +x go &&
    sudo ln -s ${install_DIR}/${DIR}/go/bin/go /usr/local/bin/go
  popd
  return $res
}

if echo "install directory: ${install_DIR}" &&
    ! mkdir -p $install_DIR; then
 exit 2
fi

pushd $install_DIR

  which elm 2>/dev/null
  if [[ $? -ne 0 ]] ||
     (echo "elm install found: $(which elm)-$(elm --version)" &&
            ([[ $(elm --version) != ${elm_VERSION_REQ} ]] &&
               echo "version required: ${elm_VERSION_REQ}")); then
   if ! elm_install; then
    echo "failed to install elm"
   else
     echo "Successfully installed elm!"
    fi
  fi

  which go 2>/dev/null
  if [[ $? -ne 0 ]]; then
   if ! go_install; then
    echo "failed to install go"
   else
    rm ${go_install_DIR}/go*.tar.gz
    echo "Successfully installed go!"
   fi
  else
    echo "go install found: $(which go)-$(go version)"
  fi

popd

exit 0

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
