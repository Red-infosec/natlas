# Natlas Security
Natlas is a project born out of a desire for improving security, and as such, the team behind Natlas strives to take into account security considerations during the design and development of the platform. Built by hackers, Natlas is extremely receptive to constructive criticisms and research into trying to break our project.


## Reporting Vulnerabilities
As there is not currently much of a team behind natlas, there is no `security@` email address, however vulnerabilities can be submitted directly to [dade](https://github.com/0xdade) via his email [dade@tutanota.com](mailto:dade@tutanota.com). Tutanota has built in encryption between tutanota accounts, however for non-Tutanota users, you can use dade's PGP information, found on [keybase.io/dade](https://keybase.io/dade). For non-critical security concerns, please feel free to file a [github issue](https://github.com/natlas/natlas/issues/new).

## Password Security
Natlas uses werkzeug's `generate_password_hash` function in order to generate salted hashes for passwords. This uses `pbkdf2:sha256` by default, and a salt length of `8`. It does not currently use any PBKDF2 iterations.

## CSRF Protection
All of Natlas' routes are protected with Flask WTF's CSRF protection and a randomly generated server-side `SECRET_KEY`. The only routes that are not protected by CSRF protection are the `/api/` routes, as they are only used by the agents. The API agent authentication is separate from user authentication, so when Natlas has `Agent Authentication` turned on, those routes aren't accessible without the relevant API keys.

## Nginx Security Options
While Natlas itself doesn't set any security headers, the provided nginx configuration `natlas-server/deployment/nginx` provides a number of security related settings, including `X-Frame-Options DENY`, `X-Content-Type-Options nosniff;` and `X-XSS-Protection "1; mode=block";`. It also contains a number of TLS related security settings that provide some of the best TLS configurations available. More information can be found by reviewing the [config file](https://github.com/natlas/natlas/blob/main/natlas-server/deployment/nginx#L17-L34) yourself.