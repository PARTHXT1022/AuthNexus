from app.config.dev import Keys

def load_config():
    print("App started in dev mode\n")
    return Keys()

config = load_config()
