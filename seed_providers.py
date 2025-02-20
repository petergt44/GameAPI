# seed_providers.py
from app import create_app, db
from app.models import Provider

app = create_app()

# List of providers to insert
providers = [
    # Category 1 Providers
    {"name": "Gameroom", "category": "CATEGORY1", "username": "admin1", "password": "pass1", "base_url": "https://agentserver.gameroom777.com"},
    {"name": "CashMachine", "category": "CATEGORY1", "username": "admin2", "password": "pass2", "base_url": "http://agentserver.cashmachine777.com:8003"},
    # Category 2 Providers
    {"name": "GameVault", "category": "CATEGORY2", "username": "agent1", "password": "pass3", "base_url": "https://agent.gamevault999.com"},
    {"name": "VegasSweeps", "category": "CATEGORY2", "username": "agent2", "password": "pass4", "base_url": "https://agent.lasvegassweeps.com"},
    # Category 3 Providers
    {"name": "FireKirin", "category": "CATEGORY3", "username": "admin3", "password": "pass5", "base_url": "https://firekirin.xyz:8888"},
    {"name": "PandaMaster", "category": "CATEGORY3", "username": "admin4", "password": "pass6", "base_url": "https://www.pandamaster.vip"},
    # Category 4 Providers
    {"name": "Vblink", "category": "CATEGORY4", "username": "admin5", "password": "pass7", "base_url": "https://gm.vblink777.club"},
    {"name": "UltraPanda", "category": "CATEGORY4", "username": "admin6", "password": "pass8", "base_url": "https://ht.ultrapanda.mobi"},
]

with app.app_context():
    # Clear existing providers (optional)
    db.session.query(Provider).delete()
    db.session.commit()

    # Insert new providers
    for provider_data in providers:
        provider = Provider(**provider_data)
        db.session.add(provider)
    db.session.commit()

    print("Providers inserted successfully!")
    for provider in Provider.query.all():
        print(provider.to_dict())