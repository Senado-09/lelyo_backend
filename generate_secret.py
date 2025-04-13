import secrets

def generate_secret_key(length=64):
    key = secrets.token_urlsafe(length)
    print(f"\n✅ Clé secrète générée ({length} caractères) :\n\n{key}\n")
    print("💡 À copier/coller dans ton fichier .env comme :")
    print(f'SECRET_KEY={key}\n')

if __name__ == "__main__":
    generate_secret_key()