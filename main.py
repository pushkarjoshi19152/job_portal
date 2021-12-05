import condb
import pyfiglet


if __name__ == "__main__":
    con = condb.connection()

    result = pyfiglet.figlet_format("Ultimate Job Portal", font="slant")
    print(result)

    print('\n\n')

    res = input('Login (l) \t Signup (s):  ')
    if res.lower() == 'l':
        while con.login():
            print('\nTry Again')
        print('\nLogin Successful!')
    elif res.lower() == 's':
        while con.signup():
            print('\nFailed ! ')
        print('\nRegistration Successful!')
    ch = -1
    while ch != 2:
        ch = int(input(
            '\n\t 1.Start Scraping\n\t2.Exit\n\nEnter [1,2]:   '))
        if ch == 1:
            con.scrape()
