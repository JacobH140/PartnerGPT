import json

auth_json_str = r"""{"type": "service_account",
  "project_id": "anki-359920",
  "private_key_id": "d78c1a86928fa815451c37b26e7ee9524a85577d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDi54hevz+l6euK\nqVEMg1naMyV4bAQQcoWmVWC3B55a+N0Cj6K1iEBWH15c0QqVJ4ND+vfTejOSJoEt\nG1Ja4Ymb3V0A9ddqjekGe/WIEryD4hdmwwxz4Yu2uvzhNPCrQ0AIopNn1+/3jaym\nQkWEr0wXM1jqAEq4DEYckjBr5gg9M4Fyi+fhlhbUzyje/YZ5N1RCJg57w2Cy19Ke\nk0UqCpkFa8qUcjQcdP7McTciYaQouyqFpnn0tbtE0Etz01VeQ/zyTylUZ0BlBb9s\nEczv84hbwTM9VMacUn/uuvjdmpnWVrQC2zt6Eg7vGONmPr3sZ+ZJmWLTy8F0NlA5\n9nX6pnShAgMBAAECggEAKKGMPmchxxyBtKVIIaT9uIBzI8K34ZgYTaY5ON0w4ppw\nvQ4qdTZOSv24AIfgTMA0Fb7BlQlrZa7mb8TWNPbxFMuJZWwgZHC/+wzEdVbhkf4w\n8ZJYzwFi6thGAy/fLtPOih1Opwg4bMxeT7FLUIyxY/AqalCeEKIGBgS5jgC1lfum\nRCQqQAUjGG+XcaFETYGUgfaUKhpGbpy+7WmgA/nmcPUPHjTUWmwoO/VX/kA6RYI9\nUHDlGM51ar1npgHcSV2+WXhP1QCTx8UhgLiOUyyb66x9NwcscOeyayIRagd5fXLI\nqiT7cqQlGTRXC/Uw7vNbiVEN1/ONPYW1fDXeLrC5VwKBgQD5BzEK9IfT8RCdkIf1\njt2dTaiNKs8CLajnBS4gatFIx6LMBi3eIIG+jAyOLEKpe3FwN9hSMgVHKYGOoq9m\n/twYlZSHVFNox3MiitZzgECUBMep7gkeCYmXAw4tVYTcTcas/liErDNLOGD52uKP\nESEZpuYogC4fSnlVqZk4SrB4CwKBgQDpQcdWE+i/1B8Nd3nlzJwB8LQf/9Q8eIb2\nHDPYWgIPW7bST5L/FP4ca1Upf86gVBQqvbUUQRcVkhm1tRvlqfR9jvETCM4eOGlY\na1jMJuVPc4gM9/ygYWUBP0GWnoXw6E9S/KpLOZjr2Bs3Op7nbEpruO0//4kO+zh6\nvBgJs/R1gwKBgCWzowcnklDSFFPmh87zfDXOhhApRQHta77eF+eshFbicpE09kjE\n3x+8EEKODOGf4MK+ka+QByCI9iZkFu4e8699Jel/KMmaOKIoJuOBrUU7nAbsFNFJ\nXF1Shxjx85Vu6P9T2o7rizB+LqBlNRu32i0KCZpkHZd7LPd9H8dX93OVAoGBAMWZ\n6uNZ5F+1tES1RTfOmQ7vubguAr7jn/mYNLeAsKQQHxWVQcMEJq0upCuO0R1zfM4k\nfeVVqtekOFF9xs9NpghD8qgcWnixc1TrQ4NXJAWlqsjJwGKhf26KBucxDeji9Ggq\nEZ2+gnSxU4T7DSihzX3qYFpKAPMHEXawJ3D42Qw/AoGAQ5Bj4A2Se2DapO0vGzxD\ntI+5hCA43suwFs7Hf4vi/mD8d1MRxbGWZ9cRnSqqcPIE5CpsG+FMkmBYL3FWqpOd\nxCo/Ww5Qi8XOEn7G0baMXFxjghULpg69Wy+zzf3B9ChiWMpb7Jyr4gFOi5n4X8Q0\nt0vVtxM5BtCyXJrDvc8i1Bo=\n-----END PRIVATE KEY-----\n",
  "client_email": "anki-587@anki-359920.iam.gserviceaccount.com",
  "client_id": "104107041307721938753",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/anki-587%40anki-359920.iam.gserviceaccount.com"}
"""


error_position = 168  # adjust this if necessary
print("ERROR EXCEPR:, ", auth_json_str[error_position-10:error_position+10])  # print 10 characters on either side of the error

auth_json = json.loads(auth_json_str)

# Now, replace \\n with \n in the private_key field:
auth_json["private_key"] = auth_json["private_key"].replace("\\n", "\n")


