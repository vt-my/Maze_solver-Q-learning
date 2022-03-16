from src.maze.maze import MazeBorder, MazeExhaustiveSearch, MazeRandomFuse


class MazeGenerator(object):
    # The maze factory
    # 'empty' is deprecated.
    @staticmethod
    def generate(cfg):
        generator_name = cfg.maze['generator']
        if generator_name == 'exhaustive_search':
            return MazeExhaustiveSearch(cfg)
        elif generator_name == 'random_fuse':
            return MazeRandomFuse(cfg)
        elif generator_name == 'empty':
            return MazeBorder(cfg)
        else:
            assert False, f"Generator type {generator_name} does not exists"
