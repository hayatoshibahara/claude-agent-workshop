# GitHub Codespaces / Dev Containers 用イメージ
# devcontainer features は使わず、入るものはすべてこのファイルに明示する。

FROM ubuntu:24.04

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000
# Claude Code のバージョン（"latest" / "stable" / "2.1.89" のような固定バージョン）
ARG CLAUDE_CODE_VERSION=stable

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# 1. 基本ツール（jq は approve-api-key.sh で使う）
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    jq \
    less \
    sudo \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. 作業ユーザー
#    ubuntu:24.04 には UID 1000 の "ubuntu" ユーザーがいるので削除し、Codespaces の慣例どおり "vscode" を作る
RUN userdel -r ubuntu \
    && groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} --create-home --shell /bin/bash ${USERNAME} \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# 3. Claude Code CLI（公式ネイティブインストーラー）
#    インストーラーは ~/.local/bin に入れるため、root で入れてから /usr/local/bin にコピーし、
#    vscode / root のどちらのユーザーでも使えるようにする
RUN curl -fsSL https://claude.ai/install.sh | bash -s ${CLAUDE_CODE_VERSION} \
    && cp -L /root/.local/bin/claude /usr/local/bin/claude \
    && rm -rf /root/.local/bin/claude /root/.local/share/claude /root/.claude /root/.claude.json \
    && claude --version

# ワークショップ中にバージョンが変わらないよう自動アップデートを止める
ENV DISABLE_AUTOUPDATER=1

USER ${USERNAME}
