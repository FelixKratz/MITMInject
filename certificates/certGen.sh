#!/bin/sh

DOMAIN=$1
i=0

DNS=""
cd ./certificates/certs
for var in "$@"
do
    let i=i+1
    newLine=$'\n'
    CUR="DNS.$i = $var$newLine"
    TMP="$DNS"
    DNS="$TMP$CUR"
done

openssl genrsa -out $DOMAIN.key 2048
openssl req -new -key $DOMAIN.key -out tmp/$DOMAIN.csr -subj "/C=CO/ST=STA/L=City/O=org/CN=me/emailAddress=name@domain.top"
cat > tmp/$DOMAIN.ext << EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
$DNS
EOF

openssl x509 -req -in tmp/$DOMAIN.csr -CA ../rootCert.pem -CAkey ../rootCert.key -CAcreateserial \
-out $DOMAIN.crt -days 825 -sha256 -extfile tmp/$DOMAIN.ext
