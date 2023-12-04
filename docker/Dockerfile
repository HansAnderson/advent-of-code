from ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
        `: # docker utils` \
        gosu \
        `: # runtime dependencies` \
        pypy3 \
        python3 \
        python3-pip \
        python3-requests \
        python3-requests-oauthlib \
        python3-tz \
        && \
    apt-get clean

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
        python3-numpy \
        python3-scipy \
        && \
    apt-get clean

# Create user and fixup uid/gid on entry
COPY ./entry_fix_user_id.sh /entry_fix_user_id.sh
RUN chmod 700 /entry_fix_user_id.sh && \
    adduser --disabled-password --gecos '' --uid 1000 user
ENTRYPOINT ["/entry_fix_user_id.sh"]

RUN echo "export PS1='es-coding-challenge-hca:\w# '" >> /root/.bashrc && \
    echo "export PS1='es-coding-challenge-hca:\w\$ '" >> /home/user/.bashrc

CMD ["/bin/bash"]
