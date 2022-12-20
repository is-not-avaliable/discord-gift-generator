#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import string, os, time, platform, requests, numpy # import libs
from colorama import Fore, init
init()

# find current OS Name to clear command
clear = ""
osname = platform.system()

if str(osname).lower() == "windows":
    clear = os.system("cls")
else:
    clear = os.system("clear")

# banner
banner = f"""{Fore.GREEN}

░█▄─░█ ─▀─ ▀▀█▀▀ █▀▀█ █▀▀█ 　 ░█▀▀█ █▀▀ █▀▀▄ 　 █▀▀█ █▀▀▄ █▀▀▄ 　 ░█▀▀█ ░█─░█ ░█▀▀▀ ░█▀▀█ ░█─▄▀ ░█▀▀▀ ░█▀▀█
░█░█░█ ▀█▀ ──█── █▄▄▀ █──█ 　 ░█─▄▄ █▀▀ █──█ 　 █▄▄█ █──█ █──█ 　 ░█─── ░█▀▀█ ░█▀▀▀ ░█─── ░█▀▄─ ░█▀▀▀ ░█▄▄▀
░█──▀█ ▀▀▀ ──▀── ▀─▀▀ ▀▀▀▀ 　 ░█▄▄█ ▀▀▀ ▀──▀ 　 ▀──▀ ▀──▀ ▀▀▀─ 　 ░█▄▄█ ░█─░█ ░█▄▄▄ ░█▄▄█ ░█─░█ ░█▄▄▄ ░█─░█

                                    {Fore.MAGENTA}[by is-not-avaliable. https://github.com/is-not-avaliable]{Fore.RESET}
"""

# functions
def slow_print(*args):
    for i in args:
        print(i, flush=True, end="")
        time.sleep(.2)



#config
USE_WEBHOOK = True
clear

# try to install webhook
try:
    from discord_webhook import DiscordWebhook
except ImportError:  # If it chould not be installed
    print(
        f"Lib discord_webhook not installed. Run python3 -m pip install discord_webhook\n\n")
    USE_WEBHOOK = False

# Object
class NitroGenerator:  # Initialise
    def __init__(self, filename):
        self.fileName = filename

    def main(self):
        clear
        print(banner)

        time.sleep(2)

        # set gifts amount
        slow_print("how many gift do you want to generate?: ")
        num = int(input(''))

        if USE_WEBHOOK:
            # Get the webhook url, if the user does not wish to use a webhook the message will be an empty string
            slow_print("If you want to use a Discord webhook, type it here or press enter to ignore: ")
            url = input('')  # Get the awnser

            webhook = url if url != "" else None

            if webhook is not None:
                DiscordWebhook(  # Let the user know it has started logging the ids
                        url=url,
                        content=f"```Started checking urls\nI will send any valid codes here```"
                    ).execute()

        # print() # Print a newline for looks

        valid = []  # Keep track of valid codes
        invalid = 0  # amount of invalid codes
        chars = []
        chars[:0] = string.ascii_letters + string.digits

        # generate codes
        c = numpy.random.choice(chars, size=[num, 16])
        for s in c:  # Loop over the amount of codes to check
            try:
                code = ''.join(x for x in s)
                url = f"{Fore.GREEN}https://discord.gift/{code}{Fore.RESET}"  # Generate the url

                result = self.quickChecker(url, webhook)  # Check the codes

                if result:  # If the code was valid
                    valid.append(url) # add the url to the valid list

                else:  # If the code was not valid
                    invalid += 1  # Increase the invalid counter by one

            except KeyboardInterrupt:
                # If the user interrupted the program. ctrl + c
                while True:
                    x = input("you're sure to stop the generator? (Y/N) ")
                    if x.lower() == "y":
                        print("\nInterrupted by user")
                        break  # Break the loop
                        exit() # and exit
                    elif x.lower() == "n":
                        print("OK!")
                        break # only break the loop and continue
                    else:
                        print("Invalid answer!")

            except Exception as e:  # If the request fails
                print(f"{Fore.RED} Error | {url} {Fore.RESET}")


                print(f'{Fore.MAGENTA}Nitro Generator and Checker - {len(valid)} Valid | {invalid} Invalid\a', end='', flush=True)

        # show data
        print(f"""{Fore.LIGHTBLUE_EX}
Results:
    {Fore.GREEN}Valid: {len(valid)}
    {Fore.RED}Invalid: {invalid}
    {Fore.GREEN}Valid Codes: {', '.join(valid)}
        """)


    def quickChecker(self, nitro:str, notify=None):  # Used to check a single code at a time
        # Generate the request url
        url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        response = requests.get(url)  # Get the response from discord

        if response.status_code == 200:  # If the responce went through
            # Notify the user the code was valid
            print(f" Valid | {nitro} ", flush=True, end="")

            with open("Nitro Codes.txt", "w") as file:  # Open file to write
                # Write the nitro code to the file it will automatically add a newline
                file.write(nitro)

            if notify is not None:  # If a webhook has been added
                DiscordWebhook(  # Send the message to discord
                    url=url,
                    content=f"Valid Nito Code detected! @everyone \n{nitro}"
                ).execute()

            return True  # Tell the main function the code was found

        # If the responce got ignored or is invalid
        else:
            # Tell the user it tested a code and it was invalid
            print(f" Invalid | {nitro} ", flush=True, end="")
            return False  # Tell the main function there was not a code found


if __name__ == '__main__':
    Gen = NitroGenerator(filename=input("write the filename: "))  # Create the nitro generator object
    Gen.main()  # Run the main code
