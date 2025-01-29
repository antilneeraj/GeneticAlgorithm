try:
    CONFIG = {
        'SCREEN_WIDTH': 400,
        'SCREEN_HEIGHT': 600,
        'POPULATION_SIZE': 50,
        'MUTATION_RATE': 0.1,
        'ELITISM': 0.2,
        'PIPE_GAP': 160,
        'GRAVITY': 0.5,
        'JUMP_FORCE': -12
    }
    
    # Validation
    if CONFIG['POPULATION_SIZE'] < 1:
        raise ValueError("Population size must be at least 1")
    if not (0 <= CONFIG['MUTATION_RATE'] <= 1):
        raise ValueError("Mutation rate must be between 0 and 1")
        
except Exception as e:
    print(f"Invalid configuration: {str(e)}")
    raise