import pygame
from pytmx import TiledObjectGroup, TiledTileLayer
from pytmx.util_pygame import load_pygame


class TiledMap:
    def __init__(self, tmx_path):
        self.tmx_data = load_pygame(tmx_path)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

    def draw(self, surface):
        for layer in self.tmx_data.visible_layers:
            if not isinstance(layer, TiledTileLayer):
                continue
            for x, y, gid in layer:
                tile = self.tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

    def get_collision_rects(self, layer_name="collisions"):
        rects = self._get_collision_rects_from_object_layer(layer_name)
        if rects:
            return rects

        # Fallback: build collisions from tile property `bloquant=true`.
        return self._get_collision_rects_from_tile_property("bloquant")

    def _get_collision_rects_from_object_layer(self, layer_name):
        rects = []
        for layer in self.tmx_data.visible_layers:
            if not isinstance(layer, TiledObjectGroup):
                continue
            if layer.name != layer_name:
                continue
            for obj in layer:
                if hasattr(obj, "width") and hasattr(obj, "height") and obj.width and obj.height:
                    rects.append(
                        pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height))
                    )
        return rects

    def _get_collision_rects_from_tile_property(self, property_name):
        rects = []
        tile_w = self.tmx_data.tilewidth
        tile_h = self.tmx_data.tileheight

        for layer in self.tmx_data.visible_layers:
            if not isinstance(layer, TiledTileLayer):
                continue

            for x, y, gid in layer:
                if gid == 0:
                    continue

                props = self.tmx_data.get_tile_properties_by_gid(gid) or {}
                if not props.get(property_name, False):
                    continue

                tile_x = x * tile_w
                tile_y = y * tile_h

                # If a tile has a collision shape in the tileset, use it.
                objects = props.get("objectgroup")
                if objects:
                    for obj in objects:
                        if not getattr(obj, "width", 0) or not getattr(obj, "height", 0):
                            continue
                        rects.append(
                            pygame.Rect(
                                int(tile_x + obj.x),
                                int(tile_y + obj.y),
                                int(obj.width),
                                int(obj.height),
                            )
                        )
                    continue

                rects.append(pygame.Rect(tile_x, tile_y, tile_w, tile_h))

        return rects

    def get_spawns(self, layer_name="spawns"):
        spawns = {}
        for layer in self.tmx_data.visible_layers:
            if not isinstance(layer, TiledObjectGroup):
                continue
            if layer.name != layer_name:
                continue
            for obj in layer:
                if obj.name:
                    spawns[obj.name] = (int(obj.x), int(obj.y))
        return spawns
