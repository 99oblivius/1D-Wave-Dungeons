from . import event_handler


def update(state, entities):
    player = entities.player
    enemies = entities.enemies
    effects = entities.effects
    # Effect update
    kill = []
    for effect in effects:
        effect.lifetime -= state.delta_time
        if effect.lifetime <= 0:
            kill.append(effect)
    for effect in kill:
        effects.remove(effect)

    # Enemy update
    kill = []
    for n, enemy in enumerate(enemies):
        old_positions = enemies[n + 1:]
        if enemy.pos > player.pos:
            enemy.facing_left = True
            blocked = any((True for e in old_positions if 0 < enemy.pos - e.pos < 2))
            if not blocked and enemy.pos - player.pos > 1:
                enemy.left()

        elif enemy.pos < player.pos:
            enemy.facing_left = False
            blocked = any((True for e in old_positions if 0 < e.pos - enemy.pos < 2))
            if not blocked and player.pos - enemy.pos > 1:
                enemy.right()
        if abs(enemy.pos - player.pos) <= enemy.attack_range:
            event_handler.attacking(enemy, [player], effects)

        if enemy.health <= 0:
            player.score += enemy.points
            kill.append(enemy)
    for enemy in kill:
        enemies.remove(enemy)

    # Player update
    state.died = player.health <= 0.0
    state.slaughtered = all(enemy.health <= 0 for enemy in enemies)
    state.escaped = player.pos > state.playspace - 1
    if any((state.died, state.slaughtered, state.escaped)):
        state.playing = False