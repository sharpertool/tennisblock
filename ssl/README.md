# Creating ssl keys and certs

The following commands will create a local set of keys that you can use for the django dev server and the webpack dev server for local development using https.

    # From the project root
    mkdir ssl
    cd ssl
    openssl genrsa -out private.key 4096
    openssl req -new -sha256 -out private.csr -key private.key -config ssl.conf
    openssl x509 -req \
        -days 3650 \
        -in private.csr \
        -signkey private.key \
        -out private.crt \
        -extensions req_ext \
        -extfile ssl.conf

    # Make my system trust this cert
    sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain private.crt

    openssl x509 -in private.crt -out private.pem -outform PEM




