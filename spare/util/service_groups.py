from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "replaceme_harvester replaceme_timelord_launcher replaceme_timelord replaceme_farmer replaceme_full_node replaceme_wallet".split(),
    "node": "replaceme_full_node".split(),
    "harvester": "replaceme_harvester".split(),
    "farmer": "replaceme_harvester replaceme_farmer replaceme_full_node replaceme_wallet".split(),
    "farmer-no-wallet": "replaceme_harvester replaceme_farmer replaceme_full_node".split(),
    "farmer-only": "replaceme_farmer".split(),
    "timelord": "replaceme_timelord_launcher replaceme_timelord replaceme_full_node".split(),
    "timelord-only": "replaceme_timelord".split(),
    "timelord-launcher-only": "replaceme_timelord_launcher".split(),
    "wallet": "replaceme_wallet replaceme_full_node".split(),
    "wallet-only": "replaceme_wallet".split(),
    "introducer": "replaceme_introducer".split(),
    "simulator": "replaceme_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
