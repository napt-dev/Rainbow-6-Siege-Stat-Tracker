# ignore my shit code I promise ill get better <3

import asyncio
import decimal
import tkinter
import threading
import time

import aiohttp.client_exceptions
import customtkinter as tk
import siegeapi.exceptions
from aiohttp import ClientSession, TCPConnector
from siegeapi import Auth

logged_in = threading.Event()
global_username = "None"
global_password = "None"

def main() -> None:
    global in_game_name, platform, ubi, error_label, main_account,  main_account_button, main_account_textbox, main_account_checkbox_frame, main_account_username, main_account_ubi
    root = tk.CTk()
    root.title("Tracker")

    root_frame = tk.CTkFrame(root)
    root_frame.pack(padx=20, pady=20)

    main_account_frame = tk.CTkFrame(root_frame)
    main_account_frame.pack(side="left", padx="20", pady="10")

    header_frame = tk.CTkFrame(root_frame)
    header_frame.pack(padx=20, pady=10)

    main_account_checkbox_frame = tk.CTkFrame(main_account_frame)


    main_account_ubi = tkinter.StringVar()
    main_account_ubi_radio_button = tk.CTkRadioButton(main_account_checkbox_frame, text="ubi", value="uplay", variable=main_account_ubi)
    main_account_ubi_radio_button.pack(side="left", padx=10, pady=10)

    main_account_xbl_radio_button = tk.CTkRadioButton(main_account_checkbox_frame, text="XBOX", value="xbl", variable=main_account_ubi)
    main_account_xbl_radio_button.pack(side="left")

    main_account_psn_radio_button = tk.CTkRadioButton(main_account_checkbox_frame, text="PSN", value="psn", variable=main_account_ubi)
    main_account_psn_radio_button.pack(side="left")

    main_account = tk.CTkLabel(main_account_frame)
    main_account.pack()

    main_account_username = tkinter.StringVar()
    main_account_textbox = tk.CTkEntry(main_account_frame, textvariable=main_account_username)

    main_account_button = tk.CTkButton(main_account_frame, text='Link', command=lambda: asyncio.run(link_account()))

    checkbox_frame = tk.CTkFrame(root_frame)
    checkbox_frame.pack(padx=20, pady=10)

    in_game_name = tkinter.StringVar()
    username_entry = tk.CTkEntry(header_frame, textvariable=in_game_name)
    username_entry.pack(padx=10, pady=10)

    platform = tk.StringVar(value="N/A")

    ubi = tkinter.IntVar()
    ubi_radio_button = tk.CTkRadioButton(checkbox_frame, text="ubi", value="uplay", variable=platform)
    ubi_radio_button.pack(side="left", padx=10, pady=10)

    xbl_radio_button = tk.CTkRadioButton(checkbox_frame, text="XBOX", value="xbl", variable=platform)
    xbl_radio_button.pack(side="left")

    psn_radio_button = tk.CTkRadioButton(checkbox_frame, text="PSN", value="psn", variable=platform)
    psn_radio_button.pack(side="left")

    track_button = tk.CTkButton(header_frame, text="Track", command=lambda: asyncio.run(track_player()))
    track_button.pack(padx=10, pady=10)

    login_button = tk.CTkButton(header_frame, text="Login", command=lambda: login_window())
    login_button.pack(padx=10, pady=10)

    error_label = tk.CTkLabel(header_frame, text="")
    login_thread.start()

    if (asyncio.run(test_login()) == "Invalid Credintials"):
        main_account.configure(text="Please login to link stats.")

    root.mainloop()


def check_if_logged_in():
    while not logged_in.is_set() :
        time.sleep(2)
        print("not logged in")
    else:
        main_account.configure(text="Link an account below")
        main_account_textbox.pack(padx=10, pady=10)
        main_account_checkbox_frame.pack(padx=10)
        main_account_button.pack(padx=10, pady=10)


login_thread = threading.Thread(target=check_if_logged_in, daemon=True)

def result_window( player, ratio) -> None:
    results = tk.CTkToplevel()  # Creates a new window
    results.title(f"{player.name}")
    results.geometry()

    title = tk.CTkLabel(results, text=f"{player.name}")
    title.pack()

    frame = tk.CTkFrame(master=results)
    frame.pack(padx=20, pady=20)

    player_name = tk.CTkLabel(frame, text=f"{player.name}")
    player_name.pack()

    player_level = tk.CTkLabel(frame, text=f"Level: {player.level}")
    player_level.pack()

    time_played = tk.CTkLabel(frame, text=(f"Total Time Played: {player.total_time_played:,} seconds"))
    time_played.pack()

    ranked_points = tk.CTkLabel(frame, text=f"Ranked Points: {player.ranked_profile.rank_points}")
    ranked_points.pack()

    player_rank = tk.CTkLabel(frame, text=f"Rank: {player.ranked_profile.rank}")
    player_rank.pack()

    max_ranked_points = tk.CTkLabel(frame, text=f"Max Rank Points: {player.ranked_profile.max_rank_points}")
    max_ranked_points.pack()

    max_rank = tk.CTkLabel(frame, text=f"Max Rank: {player.ranked_profile.max_rank}")
    max_rank.pack()

    season_kills = tk.CTkLabel(frame, text=f"Season Kills: {player.ranked_profile.kills}")
    season_kills.pack()

    season_deaths = tk.CTkLabel(frame, text=f"Season Deaths: {player.ranked_profile.deaths}")
    season_deaths.pack()

    kd_ratio = tk.CTkLabel(frame, text="K/D Ratio: " + str(ratio))
    kd_ratio.pack()


def login_window() -> None:
    def on_login() -> None:
        global global_username, global_password
        global_username = email.get()
        global_password = user_password.get()
        if (asyncio.run(test_login()) == "Connection Error"):
            error_label.pack()
            error_label.configure(text="Check Your Connection")
            print(
                "An error has occurred while attempting to log in. Check your login credential or internet connection.")
        elif (asyncio.run(test_login()) == "Invalid Credintials"):
            error_label.pack()
            error_label.configure(text="Check User/Password")
        else:
            logged_in.set()
            login.destroy()

    login = tk.CTkToplevel()
    login.title("Login")
    login.geometry("200x200")

    username_label = tk.CTkLabel(login, text="Username")
    username_label.pack()

    email = tkinter.StringVar()
    username_prompt = tk.CTkEntry(login, textvariable=email)
    username_prompt.pack(padx=5)

    password_label = tk.CTkLabel(login, text="Password")
    password_label.pack()

    user_password = tkinter.StringVar()
    password_prompt = tk.CTkEntry(login, show="*", textvariable=user_password)
    password_prompt.pack(padx=5)

    error_label = tk.CTkLabel(login, text="")
    error_label.pack()

    enter_button = tk.CTkButton(login, text="Enter", command=lambda: on_login())
    enter_button.pack(pady=10)

async def test_login() -> str:
    connector = TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:
        auth = Auth(global_username, global_password, session=session)
        try:
            player = await auth.get_player(name="xyz swxngnn", platform="xbl")
            print(f"{player.name}")
        except siegeapi.exceptions.FailedToConnect:
            login_error = "Invalid Credintials"
            return login_error
        except aiohttp.client_exceptions.ClientConnectorError:
            login_error = "Connection Error"
            return login_error
        await auth.close()


async def link_account() -> None:  # tracks a player
    connector = TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:

        try:
            auth = Auth(global_username, global_password, session=session)
            main_account_player = await auth.get_player(name=main_account_username.get(), platform=main_account_ubi.get())
        except TypeError:
            print("missing value")
            error_label.pack()
            error_label.configure(text='Please select a platform')
        except siegeapi.exceptions.InvalidRequest:
            print("No results found")
            error_label.pack()
            error_label.configure(text="No Resuts found")
        except NameError:
            print("please login to your ubisoft account")
            error_label.pack()
            error_label.configure(text="Please login to ubisoft")
        else:
            print(f'{main_account_player.name}')
            print('working on it bra')
        await auth.close()


async def track_player() -> None:  # tracks a player
    connector = TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:

        try:
            auth = Auth(global_username, global_password, session=session)
            player = await auth.get_player(name=in_game_name.get(), platform=platform.get())
        except TypeError:
            print("missing value")
            error_label.pack()
            error_label.configure(text='Please select a platform')
        except siegeapi.exceptions.InvalidRequest:
            print("No results found")
            error_label.pack()
            error_label.configure(text="No Results found")
        except NameError:
            print("please login to your ubisoft account")
            error_label.pack()
            error_label.configure(text="Please login to ubisoft")
        else:
            print(f"Name: {player.name}")
            print(f"Profile pic URL: {player.profile_pic_url}")

            await asyncio.sleep(1)
            await player.load_playtime()
            print('loading playtime')

            await asyncio.sleep(1)
            await player.load_ranked_v2()
            print('loading ranked statistics')

            def find_games_played():
                wins = int(player.ranked_profile.wins)
                losses = int(player.ranked_profile.losses)
                games_played = int(wins + losses)
                print(games_played)

            find_games_played()

            try:
                kills = int(player.ranked_profile.kills)
                deaths = int(player.ranked_profile.deaths)
                with decimal.localcontext() as ctx:
                    ctx.prec = 3
                    ratio = decimal.Decimal(kills) / decimal.Decimal(deaths)
                print(ratio)
            except decimal.InvalidOperation:
                ratio = "0"


            result_window(player, ratio)
            await auth.close()


if __name__ == '__main__':
    main()
