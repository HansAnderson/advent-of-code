#!/bin/bash
set -e

IMAGE_NAME='advent-of-code-2021'

D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USAGE="usage: $(basename "$0") [options]

options:
    -r|--root           run container as root
    -v|--verbose        enable verbose output
    -h|--help           display this help and exit"

OPTS="r"
LONGOPTS="root"

if ! TEMP="$(getopt -o ${OPTS}vh --long ${LONGOPTS},verbose,help -n "$0" -- "$@")"; then
    echo "${USAGE}" >&2
    exit 2
fi

eval set -- "${TEMP}"

ROOT=0
VERBOSE=0

while true; do
    case "$1" in
        -r|--root)
            ROOT=1
            shift 1
            ;;
        -v|--verbose)
            VERBOSE=1
            shift 1
            ;;
        -h|--help) echo "${USAGE}"; exit 0;;
        --) shift; break;;
        *) echo "The script is broken 2" >&2; exit 2;;
    esac
done

docker_build_opts=(
    "--tag=${IMAGE_NAME}"
)

if [[ "${VERBOSE}" -eq 0 ]]; then
    docker_build_opts+=('--quiet')
fi

docker build "${docker_build_opts[@]}" "${D}"

docker_run_opts=(
    "--volume=$(pwd):/local"
    '--net=host'
    '--workdir=/local'
)

if [[ "${ROOT}" -eq 0 ]]; then
    docker_run_opts+=("--env=DOCKER_UID=$(id -u)")
    docker_run_opts+=("--env=DOCKER_GID=$(id -g)")
fi

docker run -it --rm "${docker_run_opts[@]}" "${IMAGE_NAME}" "$@"
