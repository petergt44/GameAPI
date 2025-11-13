# seed_providers.py
from app import create_app, db
from app.models import Provider

app = create_app()

# Updated provider list with corrected credentials and URLs
providers = [
    # Category 1 Providers (6 games)
    {"name": "Gameroom", "category": "CATEGORY1", "username": "store576", "password": "Store576!", "base_url": "https://agentserver.gameroom777.com"},
    {"name": "Cash Machine", "category": "CATEGORY1", "username": "store576", "password": "Store576!", "base_url": "http://agentserver.cashmachine777.com:8003"},
    {"name": "Mr All In One", "category": "CATEGORY1", "username": "store576", "password": "Store576!", "base_url": "http://agentserver.mrallinone777.com"},
    {"name": "Cash Frenzy", "category": "CATEGORY1", "username": "store576", "password": "Store576!", "base_url": "http://agentserver.cashfrenzy777.com:8003"},
    {"name": "Mafia", "category": "CATEGORY1", "username": "store576", "password": "Store576!", "base_url": "http://agentserver.mafia77777.com:8003"},
    {"name": "King of Pop", "category": "CATEGORY1", "username": "Store576", "password": "Store576", "base_url": "http://agentserver.slots88888.com:8003"},

    # Category 2 Providers (3 games)
    {"name": "Game Vault", "category": "CATEGORY2", "username": "store576", "password": "store576", "base_url": "https://agent.gamevault999.com"},
    {"name": "Vegas Sweeps", "category": "CATEGORY2", "username": "store576", "password": "store576", "base_url": "https://agent.lasvegassweeps.com"},
    {"name": "Juwa", "category": "CATEGORY2", "username": "store8392", "password": "store8392", "base_url": "https://ht.juwa777.com"},

    # Category 3 Providers (4 games)
    {"name": "Orion Stars", "category": "CATEGORY3", "username": "Store56789", "password": "Store56789@@", "base_url": "https://orionstars.vip:8781"},
    {"name": "Panda Master", "category": "CATEGORY3", "username": "Store567890", "password": "Store567890", "base_url": "https://www.pandamaster.vip"},
    {"name": "Milkyway", "category": "CATEGORY3", "username": "Store56789", "password": "Store56789", "base_url": "https://milkywayapp.xyz:8781"},
    {"name": "Fire Kirin", "category": "CATEGORY3", "username": "Store56789", "password": "Store56789", "base_url": "https://firekirin.xyz:8888"},

    # Category 4 Providers (1 game)
    {"name": "River Sweeps", "category": "CATEGORY4", "username": "store576", "password": "StoreX576", "base_url": "https://river-pay.com"},

    # Category 5 Providers (3 games)
    {"name": "Vblink", "category": "CATEGORY5", "username": "Store5678", "password": "Store5678", "base_url": "https://gm.vblink777.club"},
    {"name": "Egame", "category": "CATEGORY5", "username": "Store5678", "password": "Store5678", "base_url": "https://pko.egame99.club"},
    {"name": "Ultra Panda", "category": "CATEGORY5", "username": "Storet5678", "password": "Storet5678", "base_url": "https://ht.ultrapanda.mobi"},
]

with app.app_context():
    # Clear existing providers (optional: remove if you want to append instead)
    db.session.query(Provider).delete()
    db.session.commit()

    # Insert updated providers
    for provider_data in providers:
        provider = Provider(**provider_data)
        db.session.add(provider)
    db.session.commit()

    print("Providers inserted successfully!")
    for provider in Provider.query.all():
        print(provider.to_dict())