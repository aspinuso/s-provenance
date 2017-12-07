#!/usr/bin/env python3

import connexion
from .encoder import JSONEncoder


if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': '#### S-ProvFlow provenance api Provenance framework for storage and access of data-intensive streaming lineage. It offers a a web API and a range of dedicated visualisation tools and a provenance model (S-PROV) which utilises and extends PROV and ProvONE models '})
    app.run(port=8080)
