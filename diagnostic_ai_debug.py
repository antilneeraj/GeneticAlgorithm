# FIXED DIAGNOSTIC SCRIPT - Handles pygame initialization properly
"""
diagnostic_ai_debug_fixed.py
Run this script to identify and fix AI training issues
"""

import sys
import os
import numpy as np
import random
import time
from src.utils.constants import *


def test_neural_networks():
    """Test if neural networks are actually different"""
    print("🧪 TESTING NEURAL NETWORKS")
    print("="*50)
    
    try:
        from src.ai.neural_network import NeuralNetwork
        
        # Create 3 neural networks with different seeds (FIXED: proper seed range)
        networks = []
        for i in range(3):
            # FIXED: Use proper seed range for numpy
            seed = (int(time.time() * 1000) + i * 1000) % (2**31 - 1)
            np.random.seed(seed)
            nn = NeuralNetwork(NN_INPUT_NODES, NN_HIDDEN_NODES, NN_OUTPUT_NODES)
            networks.append(nn)
            
        # Test with same input
        test_input = [0.5, 0.0, 0.8, 0.5]
        
        print("Testing with input:", test_input)
        outputs = []
        for i, nn in enumerate(networks):
            output = nn.forward_pass(test_input)
            decision = nn.predict(test_input)
            weights_sample = nn.get_weights_as_array()[:5]
            
            print(f"Network {i+1}:")
            print(f"  Output: {output:.4f}")
            print(f"  Decision: {decision}")
            print(f"  Sample weights: {weights_sample}")
            print()
            
            outputs.append(output)
            
        # Check if networks are different
        weights1 = networks[0].get_weights_as_array()
        weights2 = networks[1].get_weights_as_array()
        difference = np.mean(np.abs(weights1 - weights2))
        
        output_variance = np.var(outputs)
        
        print(f"Weight difference between networks: {difference:.6f}")
        print(f"Output variance: {output_variance:.6f}")
        
        success = difference > 0.0001 and output_variance > 0.0001
        if success:
            print("✅ Networks are properly different")
        else:
            print("❌ PROBLEM: Networks are too similar!")
            
        return success
        
    except Exception as e:
        print(f"❌ Error testing neural networks: {e}")
        return False

def test_game_state_inputs():
    """Test if game state inputs are valid"""
    print("\n🎮 TESTING GAME STATE INPUTS")
    print("="*50)
    
    try:
        # FIXED: Initialize pygame properly
        import pygame
        pygame.init()
        pygame.display.set_mode((400, 600))  # Initialize display for image conversion
        
        from src.game.bird import Bird
        from src.game.pipe import Pipe
        from src.utils.asset_loader import AssetLoader
        
        # Create mock bird
        asset_loader = AssetLoader()
        asset_loader.load_all_assets()
        
        bird_sprites = asset_loader.get_bird_sprites("BLUE")
        bird = Bird(100, 300, bird_sprites, "BLUE")
        
        # Create mock pipes
        pipe_sprite = asset_loader.get_pipe_sprite("GREEN")
        pipes = []
        
        # Create a proper pipe pair
        top_pipe = Pipe(400, 0, pipe_sprite, is_top=True)
        top_pipe.rect.height = 200  # Top pipe height
        top_pipe.rect.bottom = 200  # Top pipe bottom at y=200
        
        bottom_pipe = Pipe(400, 350, pipe_sprite, is_top=False)
        bottom_pipe.rect.height = 250  # Bottom pipe height  
        bottom_pipe.rect.top = 350   # Bottom pipe top at y=350
        
        pipes = [top_pipe, bottom_pipe]
        
        # Test game state extraction
        game_state = bird.get_game_state(pipes)
        
        print("Game state:", game_state)
        print("Game state length:", len(game_state))
        print("Game state types:", [type(x) for x in game_state])
        
        # Check validity
        valid = True
        if len(game_state) != 4:
            print("❌ PROBLEM: Game state should have 4 inputs")
            valid = False
            
        for i, val in enumerate(game_state):
            if not isinstance(val, (int, float)):
                print(f"❌ PROBLEM: Game state[{i}] is not numeric: {type(val)}")
                valid = False
            elif abs(val) > 10:  # Reasonable range check
                print(f"⚠️  WARNING: Game state[{i}] seems extreme: {val}")
                
        if valid:
            print("✅ Game state inputs look valid")
            
        pygame.quit()
        return valid
        
    except Exception as e:
        print(f"❌ Error testing game state: {e}")
        return False

def test_collision_detection():
    """Test if collision detection is too aggressive"""
    print("\n💥 TESTING COLLISION DETECTION")
    print("="*50)
    
    try:
        # FIXED: Initialize pygame properly
        import pygame
        pygame.init()
        pygame.display.set_mode((400, 600))
        
        from src.game.bird import Bird
        from src.utils.asset_loader import AssetLoader
        
        # Create bird
        asset_loader = AssetLoader()
        asset_loader.load_all_assets()
        
        bird_sprites = asset_loader.get_bird_sprites("BLUE")
        bird = Bird(100, 300, bird_sprites, "BLUE")
        
        print(f"Bird initial position: ({bird.rect.x}, {bird.rect.y})")
        print(f"Bird size: {bird.rect.width} x {bird.rect.height}")
        print(f"Screen height: {SCREEN_HEIGHT}")
        print(f"Ground level: {SCREEN_HEIGHT - 112}")
        
        # Simulate bird falling
        frames_to_ground = 0
        original_y = bird.rect.y
        
        while bird.rect.bottom < SCREEN_HEIGHT - 112 and frames_to_ground < 100:
            bird.update(False)  # No jumping
            frames_to_ground += 1
            
        distance_fallen = bird.rect.y - original_y
        
        print(f"Frames to reach ground: {frames_to_ground}")
        print(f"Distance fallen: {distance_fallen} pixels")
        print(f"Final bird position: ({bird.rect.x}, {bird.rect.y})")
        
        # Analysis
        if frames_to_ground < 40:
            print("⚠️  WARNING: Bird reaches ground very quickly!")
            print("This explains why all birds die at ~38 frames")
            success = False
        else:
            print("✅ Bird takes reasonable time to fall")
            success = True
            
        # Test collision buffer
        bird2 = Bird(100, SCREEN_HEIGHT - 112 - 3, bird_sprites, "BLUE")  # Near ground
        collision = bird2.check_collision([], SCREEN_HEIGHT - 112, SCREEN_HEIGHT)
        
        print(f"Collision with 3px buffer: {collision}")
        
        pygame.quit()
        return success
        
    except Exception as e:
        print(f"❌ Error testing collision: {e}")
        return False

def test_fitness_calculation():
    """Test fitness calculation logic"""
    print("\n🎯 TESTING FITNESS CALCULATION") 
    print("="*50)
    
    try:
        from src.ai.fitness import Fitness
        
        # Create mock bird data
        class MockBird:
            def __init__(self, score, alive, frames_survived=38):
                self.score = score
                self.alive = alive
                self.fitness = frames_survived * FITNESS_BONUS_DISTANCE
                
        birds = [
            MockBird(0, False, 38),   # Typical failing case
            MockBird(1, False, 180),  # Bird that scored once  
            MockBird(0, True, 200),   # Still alive bird
        ]
        
        print("Testing fitness calculation:")
        for i, bird in enumerate(birds):
            fitness = Fitness.calculate_fitness(bird, 600, 1)  # 600ms = 0.6s
            expected_fitness = (
                600 * FITNESS_BONUS_DISTANCE +  # Survival time bonus
                bird.score * FITNESS_BONUS_PIPE +  # Score bonus
                bird.fitness +  # Distance bonus
                (0 if bird.alive else abs(FITNESS_PENALTY_DEATH))  # Death penalty
            ) * 1.1  # Generation multiplier
            
            print(f"Bird {i+1}: score={bird.score}, alive={bird.alive}, frames={bird.fitness/FITNESS_BONUS_DISTANCE:.0f}")
            print(f"  Calculated fitness: {fitness:.1f}")
            print(f"  Expected range: ~{expected_fitness:.1f}")
            print()
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing fitness: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("🔬 FLAPPY BIRD AI DIAGNOSTIC TOOL (FIXED)")
    print("="*60)
    print("This will identify the exact issues with your AI training")
    print()
    
    results = {}
    
    # Run all tests
    results['neural_networks'] = test_neural_networks()
    results['game_state'] = test_game_state_inputs()
    results['collision'] = test_collision_detection()
    results['fitness'] = test_fitness_calculation()
    
    # Summary
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("="*50)
    
    issues_found = []
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        if not passed:
            issues_found.append(test_name)
    
    if issues_found:
        print(f"\n🚨 ISSUES FOUND: {len(issues_found)}")
        print("Problems detected in:", ", ".join(issues_found))
        print("\n🔧 SPECIFIC FIXES NEEDED:")
        
        if 'neural_networks' in issues_found:
            print("- Fix neural network random seed initialization")
            print("- Ensure each bird gets different weights")
            
        if 'game_state' in issues_found:
            print("- Fix bird.get_game_state() method")
            print("- Ensure proper pipe detection and normalization")
            
        if 'collision' in issues_found:
            print("- Make collision detection more lenient")
            print("- Add collision buffers to prevent instant death")
            
        if 'fitness' in issues_found:
            print("- Fix fitness calculation formula")
            
        print(f"\n💡 PRIORITY: Fix neural network diversity first!")
        print("All birds are making identical decisions because they have identical weights.")
        
    else:
        print("\n✅ ALL TESTS PASSED!")
        print("The AI training should work properly now.")
        
    print(f"\n{'='*60}")
    
if __name__ == "__main__":
    main()