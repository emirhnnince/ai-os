# ==============================================================================
# AI-OS Docker İmajı Derleme Ortamı
# Bu Dockerfile sayesinde herhangi bir işletim sisteminde (Windows, Mac, Linux)
# AI-OS Debian Live ISO imajı tek komutla derlenebilir.
# ==============================================================================

FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    live-build \
    debootstrap \
    squashfs-tools \
    xorriso \
    isolinux \
    syslinux-common \
    python3 \
    python3-pip \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY scripts/build/build_iso.sh /build/build_iso.sh
RUN chmod +x /build/build_iso.sh

CMD ["/build/build_iso.sh"]
