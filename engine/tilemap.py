"""Tile-based world data, loaded from external JSON + a tileset image.

Maps are never hard-coded into Python source. This keeps map content
editable independently of the engine and leaves room for a dedicated
tilemap editor later without changing this loader's data format.

Tile ids in the ground/decoration/foreground layers are 1-based indexes
into the tileset (0 means "no tile"). The collision layer is a separate
0/1 grid so visuals and solidity can be authored independently.
"""
import json

import pygame


class TileMap:
    def __init__(self, data, tileset_surface):
        self.tile_size = data["tile_size"]
        self.width = data["width"]
        self.height = data["height"]
        self.ground = data["layers"]["ground"]
        self.collision = data["layers"]["collision"]
        self.decoration = data["layers"].get("decoration")
        self.foreground = data["layers"].get("foreground")
        self.objects = data.get("objects", [])
        self.entities = data.get("entities", [])
        self.spawn_points = data.get("spawn_points", [])
        self.triggers = data.get("triggers", [])

        self._tiles = self._slice_tileset(tileset_surface)

    def _slice_tileset(self, tileset_surface):
        tiles = []
        sheet_width, sheet_height = tileset_surface.get_size()
        columns = sheet_width // self.tile_size
        rows = sheet_height // self.tile_size
        for row in range(rows):
            for col in range(columns):
                rect = pygame.Rect(col * self.tile_size, row * self.tile_size,
                                    self.tile_size, self.tile_size)
                tiles.append(tileset_surface.subsurface(rect).copy())
        return tiles

    @classmethod
    def load(cls, path):
        with open(path, "r") as f:
            data = json.load(f)
        tileset_surface = pygame.image.load(data["tileset"]).convert_alpha()
        return cls(data, tileset_surface)

    @property
    def pixel_width(self):
        return self.width * self.tile_size

    @property
    def pixel_height(self):
        return self.height * self.tile_size

    def is_solid(self, tile_x, tile_y):
        if tile_x < 0 or tile_y < 0 or tile_x >= self.width or tile_y >= self.height:
            return True  # treat out-of-bounds as solid so entities can't walk off the map
        return bool(self.collision[tile_y][tile_x])

    def rect_collides_solid(self, rect):
        tile_size = self.tile_size
        min_tx = rect.left // tile_size
        max_tx = (rect.right - 1) // tile_size
        min_ty = rect.top // tile_size
        max_ty = (rect.bottom - 1) // tile_size
        for ty in range(min_ty, max_ty + 1):
            for tx in range(min_tx, max_tx + 1):
                if self.is_solid(tx, ty):
                    return True
        return False

    def _visible_tile_range(self, camera):
        tile_size = self.tile_size
        min_tx = max(0, int(camera.x) // tile_size)
        min_ty = max(0, int(camera.y) // tile_size)
        max_tx = min(self.width - 1, int(camera.x + camera.viewport_width) // tile_size)
        max_ty = min(self.height - 1, int(camera.y + camera.viewport_height) // tile_size)
        return min_tx, min_ty, max_tx, max_ty

    def _render_layer(self, surface, camera, layer):
        if layer is None:
            return
        min_tx, min_ty, max_tx, max_ty = self._visible_tile_range(camera)
        tile_size = self.tile_size
        for ty in range(min_ty, max_ty + 1):
            row = layer[ty]
            for tx in range(min_tx, max_tx + 1):
                tile_id = row[tx]
                if tile_id <= 0:
                    continue
                sx, sy = camera.world_to_screen(tx * tile_size, ty * tile_size)
                surface.blit(self._tiles[tile_id - 1], (round(sx), round(sy)))

    def render_ground(self, surface, camera):
        self._render_layer(surface, camera, self.ground)

    def render_decoration(self, surface, camera):
        self._render_layer(surface, camera, self.decoration)

    def render_foreground(self, surface, camera):
        self._render_layer(surface, camera, self.foreground)
