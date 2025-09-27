# Contributing to Flappy Bird AI - Genetic Algorithm Evolution

First off, thank you for considering contributing to this project! 🎉

## 🤝 Ways to Contribute

### 🐛 Bug Reports
- Use GitHub Issues to report bugs
- Include detailed steps to reproduce
- Provide system information (OS, Python version, etc.)
- Include error messages and logs

### ✨ Feature Requests  
- Search existing issues first
- Describe the feature clearly
- Explain the use case and benefits
- Consider implementation complexity

### 🔧 Code Contributions
- Fork the repository
- Create a feature branch
- Follow coding standards
- Add tests for new features
- Update documentation

## 🛠️ Development Setup

```bash
# Clone your fork
git clone https://github.com/antilneeraj/geneticalgorithm.git
cd geneticalgorithm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 📝 Coding Standards

### Python Style Guide
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Code Formatting
```bash
# Format code
python -m black src/
python -m isort src/

# Check linting
python -m flake8 src/
```

### Testing
```bash
# Run tests
python -m pytest tests/

# Test coverage
python -m pytest --cov=src tests/
```

## 🚀 Pull Request Process

1. **Update Documentation**: Include relevant documentation updates
2. **Add Tests**: Ensure new features have corresponding tests
3. **Update CHANGELOG**: Add entry describing your changes
4. **Commit Messages**: Use clear, descriptive commit messages
5. **Small PRs**: Keep pull requests focused and manageable

### Commit Message Format
```
feat: add new neural network architecture
fix: resolve collision detection bug
docs: update README installation steps
test: add unit tests for genetic algorithm
```

## 🧪 Testing Guidelines

### Test Categories
- **Unit Tests**: Test individual functions/classes
- **Integration Tests**: Test component interactions
- **System Tests**: Test full AI training pipeline

### Test Structure
```python
def test_neural_network_forward_pass():
    """Test neural network produces valid output."""
    # Arrange
    nn = NeuralNetwork(4, [6, 4], 1)
    input_data = [0.5, 0.3, 0.8, 0.2]
    
    # Act
    output = nn.forward_pass(input_data)
    
    # Assert
    assert 0 <= output <= 1
    assert isinstance(output, float)
```

## 📊 Performance Considerations

- **Optimization**: Consider performance impact of changes
- **Memory Usage**: Monitor memory consumption in training loops
- **Scalability**: Ensure code works with larger populations
- **Profiling**: Use cProfile for performance analysis

## 📖 Documentation

### Code Documentation
- Add docstrings to all public functions
- Include parameter descriptions and return values
- Provide usage examples

### README Updates
- Keep installation instructions current
- Update feature lists
- Add examples for new functionality

## 🎯 Areas for Contribution

### High Priority
- [ ] Performance optimizations
- [ ] Additional neural network architectures
- [ ] Hyperparameter auto-tuning
- [ ] Better visualization tools

### Medium Priority  
- [ ] Alternative selection strategies
- [ ] Parallel processing support
- [ ] Model export/import features
- [ ] Advanced statistics tracking

### Low Priority
- [ ] GUI configuration interface
- [ ] Alternative game modes
- [ ] Sound effects and music
- [ ] Multiplayer capabilities

## ❓ Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas

### Resources
- [Python Style Guide](https://pep8.org/)
- [Genetic Algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm)
- [Neural Networks](https://www.3blue1brown.com/topics/neural-networks)
- [Pygame Documentation](https://www.pygame.org/docs/)


## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---