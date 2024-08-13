import decimal
import tkinter
import customtkinter
from siegeapi import Auth
import asyncio

async def track_player(*args):# tracks a player

    selected_platform = platform.get() # gets radio button checked value

    auth = Auth("email", "password")
    player = await auth.get_player(name=username.get(), platform=selected_platform)

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

    results = customtkinter.CTkToplevel() # Creates a new window
    results.title(f"{player.name}")
    results.geometry("300x290")

    frame = customtkinter.CTkFrame(results)


    player_name = customtkinter.CTkLabel(results, text=f"Name: {player.name}")
    player_name.pack()

    player_level = customtkinter.CTkLabel(results, text=f"Level: {player.level}")
    player_level.pack()

    time_played = customtkinter.CTkLabel(results, text=(f"Total Time Played: {player.total_time_played:,} seconds"))
    time_played.pack()

    ranked_points = customtkinter.CTkLabel(results, text=f"Ranked Points: {player.ranked_profile.rank_points}")
    ranked_points.pack()

    player_rank = customtkinter.CTkLabel(results, text=f"Rank: {player.ranked_profile.rank}")
    player_rank.pack()

    max_ranked_points = customtkinter.CTkLabel(results, text=f"Max Rank Points: {player.ranked_profile.max_rank_points}")
    max_ranked_points.pack()

    max_rank = customtkinter.CTkLabel(results, text=f"Max Rank: {player.ranked_profile.max_rank}")
    max_rank.pack()

    season_kills = customtkinter.CTkLabel(results, text=f"Season Kills: {player.ranked_profile.kills}")
    season_kills.pack()

    season_deaths = customtkinter.CTkLabel(results, text=f"Season Deaths: {player.ranked_profile.deaths}")
    season_deaths.pack()

    kd_ratio = customtkinter.CTkLabel(results, text="K/D Ratio: " + str(ratio))
    kd_ratio.pack()

root = customtkinter.CTk()
root.title("Tracker")

header_frame = customtkinter.CTkFrame(root)
header_frame.pack()

checkbox_frame = customtkinter.CTkFrame(root)
checkbox_frame.pack()

username = tkinter.StringVar()
username_entry = customtkinter.CTkEntry(header_frame, textvariable = username)
username_entry.pack(padx=10, pady=10)

platform = customtkinter.StringVar(value="N/A")

ubi = tkinter.IntVar()
ubi_radio_button = customtkinter.CTkRadioButton(checkbox_frame, text="ubi", value="uplay", variable=platform)
ubi_radio_button.pack(side=customtkinter.LEFT, padx=10, pady=10)

xbl_radio_button = customtkinter.CTkRadioButton(checkbox_frame, text="XBOX", value="xbl", variable=platform)
xbl_radio_button.pack(side=customtkinter.LEFT)

psn_radio_button = customtkinter.CTkRadioButton(checkbox_frame, text="PSN", value="psn", variable=platform)
psn_radio_button.pack(side=customtkinter.LEFT)

track_button = customtkinter.CTkButton(header_frame, text="Track", command=lambda : asyncio.run(track_player()))
track_button.pack(padx=10, pady=10)

root.mainloop()