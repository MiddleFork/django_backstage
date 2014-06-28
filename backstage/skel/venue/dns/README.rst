Backstage DNS package for interacting with PowerDNS
Currently Not Implemented

Should interact with django-powerdns to be able to easily link specific versions of a Backstage Act with an internet URI-space

Should be able to publish to the web for example

production, alpha, beta versions and optional numbered versions

production_version =  backstage_dosie
alpha_version = backstage_quil
beta_version = backstage_hamma

Here we create some standard nicknames and attach names to them:
production_hosts = ['example.com','www.example.com']
alpha_hosts = ['alpha.example.com',]
beta_hosts = ['beta.example.com',]

Thus we can tie the two together and deploy a specific version at any time.....

