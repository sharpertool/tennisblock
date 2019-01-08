# Creating ssl keys and certs
Found a new tool, mkcert, that solves all of these issues, and creates a local "CA" authority that works on your local machine, and will give you a local development cert without the "warnings"

## Install mkcert

Find it online here: https://github.com/FiloSottile/mkcert

Install using HomeBrew, or download the pre-built binary. For Mac, download the 'darwin' version from here: https://github.com/FiloSottile/mkcert/releases

Move the downloaded file to a 'bin' directory or some directory in your path, rename it to 'mkcert'.

### Create your local CA

Just follow the instructions, or do this:

	mkcert -install
	
This requires your password to install the new CA

### Create a certificate and key for your project.

So far the project is configured with a top level directory 'ssl'. This directory has 3 key files:

- private.crt
- private.key
- private.pem

mkcert will create 2 of those, but the 3rd is the .pem file for the CAROOT. To create the first 2, you need to run mkcert and give it a list of local domain names you want to support.

	mkcert tennisblock.local localhost ::1
	
That will generate 2 files, named something like this:

	tennisblock.local+2.pem
	tennisblock.local+2-key.pem
	
We need to move these and rename them:

	mv tennisblock.local+2.pem ./ssl/private.crt
	mv tennisblock.local+2-key.pem ./ssl/private.key
	
That takes care of 2 files. Now, we need to copy the CAROOT file from where mkcert installed it to our local ./ssl directory. This command outputs the path:

	mkroot -CAROOT
	
So, build a command like this:

	cp "$(mkroot -CAROOT)/rootCA.pem" ./ssl/private.pem
	
That should do it. Now, make sure that runsrver_plus references the private.crt

	runserver_plus --cert-file ../ssl/private.crt
	
Note that runserver_plus runs from the django root folder, which is one level below the ./ssl dir, so that is why there is a .. in the path

The nodejs hot module replacement is already configured for the private files, in this code found in hot.js

	https: env.https ? {
      key: fs.readFileSync('../ssl/private.key'),
      cert: fs.readFileSync('../ssl/private.crt'),
      ca: fs.readFileSync('../ssl/private.pem')
    } : false,
    
That is why we needed the rootCA.pem file copied to ./ssl. If we didn't do that, we would have to modify hot.js for each user, since

	mkcert -install
	
will put those files in the local system.


# Old Way

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




