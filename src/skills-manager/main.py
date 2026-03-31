from xml.etree.ElementTree import tostring

from domain.User import User

def main():
    testUser = User(1,"Corentin")
    print(testUser)

if __name__ == "__main__":
    main()
