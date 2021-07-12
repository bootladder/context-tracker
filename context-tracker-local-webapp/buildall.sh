#!/bin/bash
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
popd

pushd backend
  echo $(pwd)
  go build
popd
