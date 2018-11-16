from crypto.configuration.network import set_network
from crypto.identity.address import address_from_passphrase
from crypto.networks.mainnet import Mainnet

set_network(Mainnet)
address = address_from_passphrase('goose program loyal raw receive leisure potato lonely ill riot federal cabbage')

print(address)
