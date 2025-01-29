try:
    from game.core import Game
    from utils.config import CONFIG
    
    if __name__ == "__main__":
        game = Game(CONFIG)
        game.run()
except ImportError as e:
    print(f"Import error: {str(e)}")
    print("Make sure all dependencies are installed and paths are correct")
except Exception as e:
    print(f"Fatal error: {str(e)}")