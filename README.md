### 🗝️ Gere os certificados iniciais

Crie um diretório na raiz do projeto chamado `certs`. Para criar as chaves ssl você precisará utilizar o comando

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem
```
Após isso, dê ENTER nas perguntas, pois você irá alterar os dois certificados posteriormente
O comando digitado anteriormente fará com que seja gerado duas chaves não assinadas dentro do diretório ``certs`` com isso você poderá acessálos e alteralos com os certificados assinados que você pode adquirir na cloudflare ou em qualquer outro lugar.