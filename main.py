import condb
import pyfiglet
import json

if __name__ == "__main__":
    con = condb.connection()

    result = pyfiglet.figlet_format("Ultimate Job Portal", font="slant")
    print(result)

    print('\n\n')

    with open('data.json','r') as data_file:
            d=json.load(data_file)
    joblist = d['jobs']

    with open('data1.json','r') as data_file:
            d=json.load(data_file)
    loclist = d['cities']


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
    while ch != 4 :
        ch = int(input('\n\t 1.Start Scraping\n\t 2.Available job roles\n\t 3.Available location for jobs\n\t 4.Exit\n\nEnter [1,2,3,4]:   '))
        if ch == 1:
            role = input("Job role: ")
            if role not in joblist:
                print("Please enter valid input or enter 2 to check available roles! ")
                continue
            loc = input("Location: ")
            if loc not in loclist:
                print("Please enter valid input or enter 3 to check available locations! ")
                continue
            con.scrape()
        if ch == 2:
            for job in joblist:
                print(f'{job} \t')
        if ch == 3:
            for job in loclist:
                print(f'{job} \t')
            
