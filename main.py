import sys
import argparse
import pygame
from src.game.game_engine import GameEngine
from src.utils.constants import POPULATION_SIZE


def print_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        🐦 FLAPPY BIRD - GENETIC ALGORITHM 🧬             ║
    ║                                                           ║
    ║        Watch AI birds learn to play Flappy Bird!          ║
    ║        Using neural networks and genetic algorithms       ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_controls():
    controls = """
    🎮 GAME CONTROLS:
    ┌─────────────────────────────────────────────┐
    │  SPACE    - Jump (Human mode) / Start game  │
    │  R        - Restart game                    │
    │  P        - Pause/Unpause                   │
    │  S        - Save high score                 │
    │  ESC      - Quit game                       │
    └─────────────────────────────────────────────┘
    
    🤖 GAME MODES:
    • human      - Play the game yourself
    • ai_training - Watch AI learn to play (50 birds)
    • ai_play    - Watch trained AI play
    """
    print(controls)


def validate_pygame():
    """Check if pygame is properly installed"""
    try:
        pygame.init()
        return True
    except Exception as e:
        print(f"❌ Error initializing pygame: {e}")
        print("💡 Try: pip install pygame")
        return False


def main():
    print_banner()

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Flappy Bird AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --mode human          # Play yourself
  python main.py --mode ai_training    # Watch AI learn
  python main.py --mode ai_play        # Watch trained AI
  
For help: python main.py --help
        """
    )

    parser.add_argument(
        '--mode',
        choices=['human', 'ai_training', 'ai_play'],
        default='human',
    )

    parser.add_argument(
        '--population',
        type=int,
        default=150,
        help='Population size'
    )

    parser.add_argument(
        '--no-sound',
        action='store_true',
        help='Disable sound effects'
    )

    parser.add_argument(
        '--fps',
        type=int,
        default=60,
        help='Target FPS (default: 60)'
    )

    args = parser.parse_args()

    pygame.init()
    game = GameEngine(mode=args.mode)

    # Validate pygame installation
    if not validate_pygame():
        return 1

    # Print controls and mode info
    print_controls()
    print(f"🎯 Starting in {args.mode.upper()} mode...")

    if args.mode == "ai_training":
        pop_size = args.population if args.population else POPULATION_SIZE
        game.population_size = pop_size
        print(f"⚙️ Configured Population Size: {pop_size}")

    # Additional setup based on arguments
    if args.no_sound:
        game.asset_loader.sounds = {}
        print("🔇 Sound disabled")

    print(f"⚡ Target FPS: {args.fps}")
    print("\n" + "="*60)

    try:
        # Apply additional settings
        if hasattr(game, 'population_size'):
            game.population_size = args.population

        # Set FPS
        if hasattr(game, 'clock'):
            # This will be used in the game loop
            pass

        # Disable sounds if requested
        if args.no_sound:
            if hasattr(game.asset_loader, 'sounds'):
                game.asset_loader.sounds = {}

        game.init_game_mode()

        game.run()

    except KeyboardInterrupt:
        print("\n\n🛑 Game interrupted by user")
        return 0

    except FileNotFoundError as e:
        print(f"\n❌ Asset file not found: {e}")
        print("💡 Make sure all asset files are in the 'assets' directory")
        print("💡 Download assets from: https://github.com/samuelcust/flappy-bird-assets")
        return 1

    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("💡 Make sure all required packages are installed:")
        print("   pip install -r requirements.txt")
        return 1

    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("💡 Please check your installation and try again")
        return 1

    finally:
        try:
            pygame.quit()
        except:
            pass

    return 0


if __name__ == "__main__":
    """Entry point when script is run directly"""
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        sys.exit(1)
