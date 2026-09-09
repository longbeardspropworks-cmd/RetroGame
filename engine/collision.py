"""Simple AABB collision helpers for a tile-based world.

Movement is resolved one axis at a time (X then Y) so an entity sliding
into a wall diagonally keeps moving along the axis that isn't blocked.
"""
import pygame


def make_rect(x, y, width, height):
    return pygame.Rect(int(round(x)), int(round(y)), width, height)


def rects_overlap(rect_a, rect_b):
    return rect_a.colliderect(rect_b)


def move_with_tile_collision(x, y, width, height, dx, dy, tilemap):
    """Move an AABB by (dx, dy), resolving collisions against tilemap's
    solid tiles independently on each axis. Returns the corrected (x, y)."""
    new_x = x + dx
    rect = make_rect(new_x, y, width, height)
    if dx != 0 and tilemap.rect_collides_solid(rect):
        new_x = _resolve_axis(rect.left, rect.right, dx, tilemap.tile_size, width)

    new_y = y + dy
    rect = make_rect(new_x, new_y, width, height)
    if dy != 0 and tilemap.rect_collides_solid(rect):
        new_y = _resolve_axis(rect.top, rect.bottom, dy, tilemap.tile_size, height)

    return new_x, new_y


def _resolve_axis(min_edge, max_edge, delta, tile_size, size):
    """Snap an AABB's leading edge to the near edge of the tile it just
    penetrated while moving along one axis."""
    if delta > 0:
        # max_edge is the exclusive right/bottom edge, so subtract 1 to land
        # on the last pixel actually occupied before dividing into tiles.
        tile_index = (max_edge - 1) // tile_size
        return tile_index * tile_size - size
    tile_index = min_edge // tile_size
    return (tile_index + 1) * tile_size
