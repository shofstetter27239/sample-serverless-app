from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcYdtKi5hWeohA8K4wcrqDd1p9Pj6ux8IhV913DhGnNEX3jIcZavtrlZ0yxbmHs8MrQTHj1LYlYJp4Wx4E1xL5bFoV6Tr8lTP6Hjj74fn-EaWZwqqv4CdvxkuOmEWaylf7dultJfwBJx6bgHqxHP6R_PxQmyRfQjLysv5_x-_uXU2pFi8='

def main():
    f = Fernet(key)
    print(f.decrypt(message).decode('UTF-8'))


if __name__ == "__main__":
    main()
