# SpaceTime Visualizer

An interactive educational tool for visualizing special relativity concepts including time dilation, relativistic mass, and spacetime diagrams.

## Features

- Interactive visualization of relativistic effects
- Real-time calculations of:
  - Time dilation
  - Relativistic mass
  - Energy (rest, kinetic, total)
  - Spacetime components
- Dark theme interface optimized for physics visualization
- Animated clock visualization for time dilation
- Dynamic spacetime diagrams

## Installation

### Using pip (Option 1)

1. Clone this repository:
```bash
git clone https://github.com/yourusername/spacetime-visualizer.git
cd spacetime-visualizer
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Using Conda (Option 2)

1. Clone this repository:
```bash
git clone https://github.com/yourusername/spacetime-visualizer.git
cd spacetime-visualizer
```

2. Create and activate a Conda environment:
```bash
conda env create -f environment.yml
conda activate spacetime-visualizer
```

## Usage

Run the application using:
```bash
python run_spacetime_visualizer.py
```

The interface is divided into several sections:
- Left panel: Educational content and explanations
- Center: Interactive visualizations
- Right panel: Control parameters and calculations

## Technical Details

Built using:
- PyQt5 for the GUI
- pyqtgraph for high-performance scientific graphics
- NumPy for calculations
- Python 3.8+

## Project Structure

```
spacetime_visualizer/
├── run_spacetime_visualizer.py  # Main entry point
├── src/
│   ├── __init__.py
│   ├── physics.py              # Relativistic calculations
│   ├── ui.py                   # Main UI components
│   ├── visualizations.py       # Plot management
│   ├── clock_visualization.py  # Time dilation animation
│   └── config.py              # Theme and constants
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
