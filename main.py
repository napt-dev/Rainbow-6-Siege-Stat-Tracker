from aiohttp import ClientSession, TCPConnector
import decimal
import tkinter
import customtkinter as tk
from siegeapi import Auth
import asyncio

global_username = None
global_password = None

def login_window():

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
    password_prompt = tk.CTkEntry(login, textvariable=user_password)
    password_prompt.pack(padx=5)

    def on_login():

        global global_username, global_password
        global_username = email.get()
        global_password = user_password.get()
        login.destroy()

    enter_button = tk.CTkButton(login, text="Enter", command=lambda : on_login())
    enter_button.pack(pady=10)

async def track_player(*args):# tracks a player
    connector = TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:

        auth = Auth(global_username, global_password, session=session)
        player = await auth.get_player(name=in_game_name.get(), platform=platform.get())

        print(f"Name: {player.name}")
        print(f"Profile pic URL: {player.profile_pic_url}")

        await player.load_playtime()
        print(f"Total Time Played: {player.total_time_played:,} seconds")
        print(f"Level: {player.level}")

        await player.load_ranked_v2()
        print(f"Ranked Points: {player.ranked_profile.rank_points}")
        print(f"Rank: {player.ranked_profile.rank}")
        print(f"Max Rank Points: {player.ranked_profile.max_rank_points}")
        print(f"Max Rank: {player.ranked_profile.max_rank}")
        print(f"Total Kills: {player.ranked_profile.kills}")
        print(f"Total Deaths: {player.ranked_profile.deaths}")


        await player.load_progress()
        print(f"XP: {player.xp:,}")
        print(f"Total XP: {player.total_xp:,}")
        print(f"XP to level up: {player.xp_to_level_up:,}")

        kills = int(player.ranked_profile.kills)
        deaths = int(player.ranked_profile.deaths)
        with decimal.localcontext() as ctx:
            ctx.prec = 3
            ratio = decimal.Decimal(kills) / decimal.Decimal(deaths)
        print(ratio)

        await auth.close()

    results = tk.CTkToplevel() # Creates a new window
    results.title(f"{player.name}")
    results.geometry("300x290")

    frame = tk.CTkFrame(results)


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

root.mainloop()