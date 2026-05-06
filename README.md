# certbot-dns-ipp
[IP-Projects](https://www.ip-projects.de) DNS Authenticator plugin for [certbot](https://certbot.eff.org/).

This plugin automates the process of completing a dns-01 challenge by creating, and subsequently removing, `TXT` records using the IP-Projects API.

Note: This plugin requires certbot ≥ v2.7.

## Installation

Since this package acts as a plugin for [certbot](https://certbot.eff.org/), the installation method can vary depending on how certbot is installed.

### pip

If certbot is installed normally as a python package, the plugin can be installed using:

```
pip install certbot-dns-ipp
```

### docker

The official docker image of this repository is available from [docker.io/ipprojects/certbot-dns-ipp](https://hub.docker.com/r/ipprojects/certbot-dns-ipp) or [ghcr.io/ipp-gmbh/certbot-dns-ipp](https://github.com/ipp-gmbh/certbot-dns-ipp/pkgs/container/certbot-dns-ipp).
Accordingly, you can pull the image as follows:
```
docker pull docker.io/ipprojects/certbot-dns-ipp
```
or
```
docker pull ghcr.io/ipp-gmbh/certbot-dns-ipp
```

## Credentials

Use of this plugin requires a configuration file containing your personal IP-Projects API Key, obtained from your [portal account page](https://portal.ip-projects.de).
An example `credentials.ini` file:
```
dns_ipp_acme_api_key = ...
```

The path to this file can be provided using the `--dns-ipp-credentials` command-line argument. Certbot records the path to this file for use during renewal, but does not store the file's contents.

**CAUTION:** Users who can read this file can use these credentials to issue arbitrary API calls on your behalf. Set the file ownership accordingly!

Certbot will emit a warning if it detects that the credentials file can be accessed by other users on your system. The warning reads "Unsafe permissions on credentials configuration file", followed by the path to the credentials file. This warning will be emitted each time Certbot uses the credentials file, including for renewal, and cannot be silenced except by addressing the issue (e.g., by using a command like chmod 600 to restrict access to the file).

## Usage

| Commandline argument                      | Explanation                                                         |
|-------------------------------------------|---------------------------------------------------------------------|
| `--authenticator dns-ipp`                 | select the authenticator plugin (Required)                          |
| `--dns-ipp-credentials "credentials.ini"` | credentials INI file containing the ip-projects api key. (Required) |

To acquire a single certificate for both `example.com` and `*.example.com`:

```
certbot certonly \
  --authenticator dns-ipp \
  --dns-ipp-credentials /etc/letsencrypt/ipp_credentials.ini \
  -d 'example.com' \
  -d '*.example.com'
```
