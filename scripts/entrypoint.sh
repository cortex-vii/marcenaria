#!/bin/sh

# Este script garante que o usuário 'duser' seja o dono das pastas
# montadas, resolvendo problemas de permissão.
# Ele roda como root antes de passar o controle para o duser.

set -e

chown -R duser:duser /data/web/static
chown -R duser:duser /data/web/media

# Executa o comando principal (o CMD do Dockerfile) como o usuário 'duser'
exec su-exec duser "$@"