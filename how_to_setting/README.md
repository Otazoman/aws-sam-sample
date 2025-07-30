## EC2インスタンス構築時に以下をユーザデータに設定

```
#!/bin/bash
update-alternatives --set editor /usr/bin/vim.basic
apt -y remove nano
apt -y update
apt -y upgrade
```

## EC2起動後に以下のコマンドを実行する

```
sudo su
timedatectl set-timezone Asia/Tokyo
hostnamectl set-hostname dev-ubuntu
USERNAME=matarain
useradd -m ${USERNAME} -s /bin/bash
passwd $USERNAME
sudo cp -r /home/ubuntu/.ssh /home/${USERNAME}/
chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.ssh
gpasswd -a ${USERNAME} sudo
```

## 再ログインしてから以下のコマンドでubuntuユーザを削除する

```
sudo deluser ubuntu
```


## 開発環境構築  

```
./dev_setting.sh
```

## DynamoDB local  

```
cd ~/sam-apps/dynamodb
sudo chmod 777 dbdata
docker compose up -d
```

## SAM API test

```
sam local start-api --docker-network dynamodb_sam-test-network
```