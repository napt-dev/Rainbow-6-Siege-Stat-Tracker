import aiohttp.client_exceptions
import siegeapi.exceptions
from aiohttp import ClientSession, TCPConnector
from siegeapi import Auth
import decimal
import tkinter
import customtkinter as tk
import asyncio

def login_window():

    def on_login():
        global global_username, global_password
        global_username = email.get()
        global_password = user_password.get()
        if (asyncio.run(test_login()) == "connection"):
            error_label.configure(text="Check Your Connection")
            print("An error has occurred while attempting to log in. Check your login credential or internet connection.")
        elif (asyncio.run(test_login()) == True):
            error_label.configure(text="Check User/Password")
        else:
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

    enter_button = tk.CTkButton(login, text="Enter", command=lambda : on_login())
    enter_button.pack(pady=10)

async def test_login():
    connector = TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:
        auth = Auth(global_username, global_password, session=session)
        try:
            player = await auth.get_player(name="xyz swxngnn", platform="xbl")
            print(f"{player.name}")
        except siegeapi.exceptions.FailedToConnect:
            login_error = True
            return login_error
        except aiohttp.client_exceptions.ClientConnectorError:
            login_error = "connection"
            return login_error
        await auth.close()

async def track_player():# tracks a player
    connector = TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:

        try:
            auth = Auth(global_username, global_password, session=session)
            player = await auth.get_player(name=in_game_name.get(), platform=platform.get())
        except TypeError:
            print("missing value")
        except siegeapi.exceptions.InvalidRequest:
            print("No results found")
            error_label.configure(text="No Resuts found")
        except NameError:
            print("please login to your ubisoft account")
            error_label.configure(text="Please login to ubisoft")
        else:
            print(f"Name: {player.name}")
            print(f"Profile pic URL: {player.profile_pic_url}")

            await asyncio.sleep(1)
            await player.load_playtime()
            print(f"Total Time Played: {player.total_time_played:,} seconds")
            print(f"Level: {player.level}")

            await asyncio.sleep(1)
            await player.load_ranked_v2()
            print(f"Ranked Points: {player.ranked_profile.rank_points}")
            print(f"Rank: {player.ranked_profile.rank}")
            print(f"Max Rank Points: {player.ranked_profile.max_rank_points}")
            print(f"Max Rank: {player.ranked_profile.max_rank}")
            print(f"Total Kills: {player.ranked_profile.kills}")
            print(f"Total Deaths: {player.ranked_profile.deaths}")

            def find_games_played():
                wins = int(player.ranked_profile.wins)
                losses = int(player.ranked_profile.losses)
                games_played = int(wins + losses)
                print(games_played)

            find_games_played()

            kills = int(player.ranked_profile.kills)
            deaths = int(player.ranked_profile.deaths)
            with decimal.localcontext() as ctx:
                ctx.prec = 3
                ratio = decimal.Decimal(kills) / decimal.Decimal(deaths)
            print(ratio)

            results = tk.CTkToplevel()  # Creates a new window
            results.title(f"{player.name}")
            results.geometry("300x290")

            player_name = tk.CTkLabel(results, text=f"Name: {player.name}")
            player_name.pack()

            player_level = tk.CTkLabel(results, text=f"Level: {player.level}")
            player_level.pack()

            time_played = tk.CTkLabel(results, text=(f"Total Time Played: {player.total_time_played:,} seconds"))
            time_played.pack()

            ranked_points = tk.CTkLabel(results, text=f"Ranked Points: {player.ranked_profile.rank_points}")
            ranked_points.pack()

            player_rank = tk.CTkLabel(results, text=f"Rank: {player.ranked_profile.rank}")
            player_rank.pack()

            max_ranked_points = tk.CTkLabel(results, text=f"Max Rank Points: {player.ranked_profile.max_rank_points}")
            max_ranked_points.pack()

            max_rank = tk.CTkLabel(results, text=f"Max Rank: {player.ranked_profile.max_rank}")
            max_rank.pack()

            season_kills = tk.CTkLabel(results, text=f"Season Kills: {player.ranked_profile.kills}")
            season_kills.pack()

            season_deaths = tk.CTkLabel(results, text=f"Season Deaths: {player.ranked_profile.deaths}")
            season_deaths.pack()

            kd_ratio = tk.CTkLabel(results, text="K/D Ratio: " + str(ratio))
            kd_ratio.pack()
            await auth.close()

root = tk.CTk()
root.title("Tracker")

header_frame = tk.CTkFrame(root)
header_frame.pack()

checkbox_frame = tk.CTkFrame(root)
checkbox_frame.pack()

in_game_name = tkinter.StringVar()
username_entry = tk.CTkEntry(header_frame, textvariable = in_game_name)
username_entry.pack(padx=10, pady=10)

platform = tk.StringVar(value="N/A")

ubi = tkinter.IntVar()
ubi_radio_button = tk.CTkRadioButton(checkbox_frame, text="ubi", value="uplay", variable=platform)
ubi_radio_button.pack(side=tk.LEFT, padx=10, pady=10)

xbl_radio_button = tk.CTkRadioButton(checkbox_frame, text="XBOX", value="xbl", variable=platform)
xbl_radio_button.pack(side=tk.LEFT)

psn_radio_button = tk.CTkRadioButton(checkbox_frame, text="PSN", value="psn", variable=platform)
psn_radio_button.pack(side=tk.LEFT)

track_button = tk.CTkButton(header_frame, text="Track", command=lambda : asyncio.run(track_player()))
track_button.pack(padx=10, pady=10)

login_button = tk.CTkButton(header_frame, text="Login", command=lambda : login_window())
login_button.pack(padx=10, pady=10)

error_label = tk.CTkLabel(header_frame, text="")
error_label.pack()

root.mainloop()