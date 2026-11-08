
from connector import get_player_stats, record_hand

player_name = "testoor"

print("Before:", get_player_stats(player_name))

record_hand(player_name, won=True)

print("After:", get_player_stats(player_name))
