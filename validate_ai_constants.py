from src.utils.constants import *

def test_ai_constants():
    """Test all AI constants are accessible"""
    try:

        print("✅ TESTING AI CONSTANTS")
        print("="*50)

        # Test Genetic Algorithm constants
        constants_to_test = {
            "Population Settings": [
                ("POPULATION_SIZE", POPULATION_SIZE),
                ("GENERATIONS", GENERATIONS),
                ("ELITE_COUNT", ELITE_COUNT)
            ],
            "Evolution Rates": [
                ("MUTATION_RATE", MUTATION_RATE),
                ("CROSSOVER_RATE", CROSSOVER_RATE)
            ],
            "Neural Network": [
                ("NN_INPUT_NODES", NN_INPUT_NODES),
                ("NN_HIDDEN_NODES", NN_HIDDEN_NODES),
                ("NN_OUTPUT_NODES", NN_OUTPUT_NODES)
            ],
            "Fitness Parameters": [
                ("FITNESS_BONUS_PIPE", FITNESS_BONUS_PIPE),
                ("FITNESS_BONUS_DISTANCE", FITNESS_BONUS_DISTANCE),
                ("FITNESS_PENALTY_DEATH", FITNESS_PENALTY_DEATH)
            ]
        }

        all_good = True

        for category, constants in constants_to_test.items():
            print(f"\n📊 {category}:")
            for name, value in constants:
                try:
                    print(f"  ✅ {name} = {value}")
                except NameError:
                    print(f"  ❌ {name} = UNDEFINED")
                    all_good = False

        if all_good:
            print("\n🎉 ALL AI CONSTANTS PROPERLY DEFINED!")
            print("Your genetic algorithm is ready to run!")

            # Test neural network creation
            print("\n🧠 Testing Neural Network Creation:")
            from src.ai.neural_network import NeuralNetwork

            nn = NeuralNetwork(
                NN_INPUT_NODES, NN_HIDDEN_NODES, NN_OUTPUT_NODES)
            print(f"  ✅ Neural Network: {nn}")
            print(f"  ✅ Total Parameters: {nn.get_total_params()}")

            # Test a forward pass
            test_input = [0.5, 0.2, 0.8, 0.6]  # Normalized bird state
            output = nn.forward_pass(test_input)
            decision = nn.predict(test_input)
            print(f"  ✅ Forward Pass Output: {output:.3f}")
            print(f"  ✅ Jump Decision: {decision}")

        else:
            print("\n❌ Some constants are missing!")
            return False

        return True

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure all AI files are in src/ai/ directory")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    test_ai_constants()
