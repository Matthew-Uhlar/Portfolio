import random


UPGRADES = [
    {
        "name": "Rapid Fire",
        "description": "Shoot 15% faster.",
        "apply": lambda player, core: setattr(player, "shot_delay", max(0.07, player.shot_delay * 0.85)),
    },
    {
        "name": "Heavy Rounds",
        "description": "Increase bullet damage by 8.",
        "apply": lambda player, core: setattr(player, "damage", player.damage + 8),
    },
    {
        "name": "Reinforced Armor",
        "description": "Increase max health by 20 and heal 20.",
        "apply": lambda player, core: (
            setattr(player, "max_health", player.max_health + 20),
            setattr(player, "health", min(player.max_health, player.health + 20)),
        ),
    },
    {
        "name": "Shield Recharge",
        "description": "Increase max shield by 15 and refill it.",
        "apply": lambda player, core: (
            setattr(player, "max_shield", player.max_shield + 15),
            setattr(player, "shield", player.max_shield),
        ),
    },
    {
        "name": "Mobility Boost",
        "description": "Move 10% faster.",
        "apply": lambda player, core: setattr(player, "speed", player.speed * 1.10),
    },
    {
        "name": "Split Shot",
        "description": "Add another projectile to each shot.",
        "apply": lambda player, core: setattr(player, "multishot", min(5, player.multishot + 1)),
    },
    {
        "name": "Piercing Rounds",
        "description": "Bullets can pass through one more enemy.",
        "apply": lambda player, core: setattr(player, "piercing", player.piercing + 1),
    },
    {
        "name": "Core Repair",
        "description": "Restore 60 core health.",
        "apply": lambda player, core: setattr(core, "health", min(core.max_health, core.health + 60)),
    },
]


def choose_upgrades(count=3):
    return random.sample(UPGRADES, count)
