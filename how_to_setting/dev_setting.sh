#!/bin/bash

# このスクリプトは、一般的な開発ツール（GCC、G++、Make、NVM、rbenv、pyenv、AWS CLI、Docker、SAM CLI、CDK）をインストールします。
# バージョンは以下の変数を設定することで変更できます。

# 変数の定義
nvm_ver="0.40.3"   # NVM (Node Version Manager) のバージョン
ruby_ver="3.4.4"   # Ruby のバージョン (rbenvでインストール)
python_ver="3.13.5" # Python のバージョン (pyenvでインストール)

echo "--- 開発ツールのインストールを開始します ---"

# 1. 必須パッケージのインストール
echo "1. 必須パッケージのインストール..."
sudo apt-get update
sudo apt-get install -y \
  gcc \
  g++ \
  make \
  build-essential \
  libssl-dev \
  zlib1g-dev \
  openssl \
  libz-dev \
  libffi-dev \
  libreadline-dev \
  libyaml-dev \
  liblzma-dev \
  libbz2-dev \
  libsqlite3-dev \
  unzip
echo "必須パッケージのインストールが完了しました。"

# 2. NVM (Node Version Manager) のインストール
echo "2. NVM (Node Version Manager) のインストール..."
# NVMのインストールスクリプトを実行
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v${nvm_ver}/install.sh | bash

# NVMが正しくロードされるように環境変数を設定
# bashrc/zshrcに追記された設定を現在のシェルに適用
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" # This loads nvm bash_completion

# 最新のLTS版Node.jsをインストールして使用
echo "Node.js LTSバージョンをインストールして使用します..."
nvm install --lts
nvm use --lts
echo "NVMとNode.jsのインストールが完了しました。"

# 3. rbenv (Ruby Version Manager) のインストール
echo "3. rbenv (Ruby Version Manager) のインストール..."
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build

# .bashrcにrbenvのパスと初期化を追加
echo 'export PATH="~/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc

# 現在のシェルにrbenv環境変数を適用
export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"

# 指定されたバージョンのRubyをインストール
echo "Ruby ${ruby_ver} をインストールします..."
rbenv install ${ruby_ver}
rbenv global ${ruby_ver}
export RUBYOPT="-EUTF-8" # 文字コード設定
echo "rbenvとRubyのインストールが完了しました。"

# 4. pyenv (Python Version Manager) のインストール
echo "4. pyenv (Python Version Manager) のインストール..."
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
# pyenv-updateプラグインはもはやyyuuのものではないので、公式のリポジトリを使用します。
# または、pyenvのバージョンが新しい場合は内蔵されていることが多いです。
# git clone https://github.com/pyenv/pyenv-update.git ~/.pyenv/plugins/pyenv-update

# .bashrcにpyenvのパスと初期化を追加
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# 現在のシェルにpyenv環境変数を適用
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# 指定されたバージョンのPythonをインストール
echo "Python ${python_ver} をインストールします..."
pyenv install ${python_ver}
pyenv global ${python_ver}
pyenv rehash
echo "pipをアップグレードします..."
pip install --upgrade pip
echo "pyenvとPythonのインストールが完了しました。"

# 5. AWS CLI v2 のインストール
echo "5. AWS CLI v2 のインストール..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install --update # 既存のインストールを更新するオプションも追加
rm -rf aws awscliv2.zip # インストール後にファイルをクリーンアップ
echo "AWS CLI v2のインストールが完了しました。"

# 6. Docker のインストール
echo "6. Docker のインストール..."
# 以前のバージョンのDockerをアンインストール（もしあれば）
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

# Dockerの公式GPGキーを追加
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# リポジトリをaptソースに追加
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Docker Engineのインストール
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Dockerをsudoなしで実行できるようにユーザーをdockerグループに追加
echo "現在のユーザーを 'docker' グループに追加しています。変更を適用するには、一度ログアウトして再度ログインしてください。"
sudo usermod -aG docker "$USER"

# Dockerサービスの開始と有効化
sudo systemctl start docker
sudo systemctl enable docker
echo "Dockerのインストールが完了しました。"
echo "Dockerをsudoなしで実行するには、一度ログアウトして再度ログインするか、新しいターミナルセッションを開いてください。"

# 7. AWS SAM CLI のインストール
echo "7. AWS SAM CLI のインストール..."
wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install
rm -rf aws-sam-cli-linux-x86_64.zip sam-installation # インストール後にファイルをクリーンアップ
echo "AWS SAM CLIのインストールが完了しました。"

# 8. AWS CDK のインストール
echo "8. AWS CDK (Cloud Development Kit) のインストール..."
# NVMによってインストールされたNode.jsのnpmを使用
npm install -g aws-cdk
echo "AWS CDKのインストールが完了しました。"

echo "--- 全ての開発ツールのインストールが完了しました！ ---"
echo "変更を適用するために、ターミナルを再起動するか、'source ~/.bashrc' を実行してください。"


