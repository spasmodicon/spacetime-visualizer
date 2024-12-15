from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QSlider, QGroupBox, QLineEdit, QFormLayout,
                           QPushButton, QStackedWidget, QCheckBox, QToolTip,
                           QTabWidget, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt, QTimer, QSize, QUrl
from PyQt5.QtGui import QDoubleValidator, QFont, QDesktopServices
import pyqtgraph as pg
from .config import LIGHT_THEME, DARK_THEME
from .physics import RelativisticCalculator
from .visualizations import PlotManager
from .clock_visualization import TimeDilationClocks

class SpaceTimeVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Space-Time Motion Visualizer')
        self.setMinimumSize(1400, 900)  # Set minimum size instead of fixed size
        
        # Initialize components
        self.current_theme = DARK_THEME  # Always use dark theme
        self.plot_manager = PlotManager()
        self.plots = {}
        
        # Set tooltip style
        QToolTip.setFont(QFont('Arial', 10))
        
        self.setup_ui()
        
        # Initialize plots
        self.update_plots()

    def setup_ui(self):
        """Setup the main UI layout."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create horizontal split layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(15)  # Increased spacing between columns
        main_layout.setContentsMargins(15, 15, 15, 15)  # Increased margins
        
        # Left panel for narrative content
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(10, 10, 10, 10)  # Increased margins
        
        # Create scrollable explanation area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setMinimumWidth(500)  # Set minimum width for text area
        
        explanation_widget = QWidget()
        explanation_layout = QVBoxLayout(explanation_widget)
        explanation_layout.setSpacing(15)  # Increased spacing between elements
        
        # Add narrative content to left panel
        self.create_explanation(explanation_layout)
        self.create_mass_input(explanation_layout)
        self.create_info_display(explanation_layout)
        
        scroll.setWidget(explanation_widget)
        left_layout.addWidget(scroll)
        
        # Right panel for visualizations
        right_panel = QWidget()
        self.vis_layout = QVBoxLayout(right_panel)
        self.vis_layout.setSpacing(10)
        self.vis_layout.setContentsMargins(5, 5, 5, 5)
        
        # Add visualizations to right panel
        self.create_clocks()
        self.vis_layout.addWidget(self.clocks_group)
        
        # Create velocity slider
        self.create_velocity_slider()
        
        # Create plots
        self.create_plots()
        
        # Add panels to main layout with equal width
        main_layout.addWidget(left_panel, 1)  # stretch factor 1
        main_layout.addWidget(right_panel, 1)  # stretch factor 1

    def create_explanation(self, layout):
        """Create the explanation text at the top."""
        # Main explanation text
        self.explanation = QLabel(
            "This visualization demonstrates how measurements of space and time depend on relative motion between "
            "observers. According to Einstein's special relativity, the speed of light in vacuum is constant for all "
            "observers, regardless of their relative motion. This leads to profound consequences.\n\n"
            "When you're stationary relative to an observer, you both agree on measurements of time. However, as your "
            "relative velocity increases, time dilation occurs - the observer measures time passing more slowly for you "
            "than for themselves.\n\n"
            "The space-time visualization uses a simplified circular representation to help build intuition about how "
            "motion affects time. While this is a helpful teaching tool, it's important to note that the actual geometry "
            "of spacetime (Minkowski space) involves hyperbolic relationships, not circular ones. The visualization helps "
            "demonstrate that as an object's motion through space increases, its rate of time passage must decrease to "
            "maintain the constant speed of light.\n\n"
            "Note: Modern physics emphasizes that an object's mass (often called rest mass or invariant mass) remains "
            "constant regardless of its velocity. What changes with velocity is the object's total energy, which includes "
            "both its rest energy (E₀ = mc²) and kinetic energy."
        )
        self.explanation.setWordWrap(True)
        self.explanation.setMinimumWidth(450)  # Ensure minimum width for text wrapping
        self.explanation.setStyleSheet("font-size: 10pt; padding: 5px;")
        layout.addWidget(self.explanation)
        
        # Video link
        video_link = QPushButton("Watch Video Explanation")
        video_link.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.youtube.com/watch?v=dT0rsEtfqyU")))
        video_link.setToolTip("Watch a video explaining these concepts in detail")
        layout.addWidget(video_link)

    def create_velocity_slider(self):
        """Create the velocity slider."""
        velocity_group = QGroupBox("Velocity (% of light speed)")
        velocity_group.setToolTip(
            "Adjust the object's speed as a percentage of the speed of light. Slide to see\n"
            "how increasing velocity affects time dilation, length contraction, and other\n"
            "relativistic effects."
        )
        velocity_inner_layout = QVBoxLayout()
        
        self.slider_label = QLabel('0% c')
        self.slider_label.setStyleSheet("QLabel { font-size: 10pt; }")
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(999)  # Allow for 99.9%
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.update_plots)
        
        velocity_inner_layout.addWidget(self.slider_label)
        velocity_inner_layout.addWidget(self.slider)
        
        velocity_group.setLayout(velocity_inner_layout)
        self.vis_layout.addWidget(velocity_group)

    def create_mass_input(self, layout):
        """Create the mass input section with enhanced validation."""
        mass_layout = QHBoxLayout()
        mass_form = QFormLayout()
        
        self.mass_input = QLineEdit()
        validator = QDoubleValidator(0.0, 1e12, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.mass_input.setValidator(validator)
        self.mass_input.setText("1.0")
        self.mass_input.textChanged.connect(self.validate_mass_input)
        self.mass_input.setToolTip(
            "Input the object's **rest mass** in pounds (lbs), which is its mass when not moving\n"
            "relative to you. This affects calculations of energy and relativistic mass.\n"
            "Valid range: 0 to 1 trillion lbs."
        )
        
        mass_label = QLabel("Rest Mass (lbs):")
        self.mass_kg_label = QLabel("0.454 kg")
        self.mass_error_label = QLabel()
        self.mass_error_label.setStyleSheet("color: red;")
        
        mass_form.addRow(mass_label, self.mass_input)
        mass_form.addRow("SI Equivalent:", self.mass_kg_label)
        mass_form.addRow(self.mass_error_label)
        
        self.mass_group = QGroupBox("Object Rest Mass")
        self.mass_group.setLayout(mass_form)
        layout.addWidget(self.mass_group)

    def create_info_display(self, layout):
        """Create the information display label."""
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.info_label.setMinimumWidth(450)  # Ensure minimum width for text wrapping
        self.info_label.setToolTip(
            "This panel provides detailed explanations of the relativistic effects at the current\n"
            "speed, including time dilation, length contraction, the Lorentz factor (γ), and\n"
            "energy equivalents. It updates automatically as you change the velocity."
        )
        self.update_info_style()
        layout.addWidget(self.info_label)

    def create_clocks(self):
        """Create the time dilation clocks visualization."""
        self.clocks_group = QGroupBox("Time Dilation Visualization")
        self.clocks_group.setToolTip(
            "These clocks visually demonstrate **time dilation**. The stationary clock ticks\n"
            "at a normal rate, while the moving clock ticks slower as its speed increases.\n"
            "This shows how time passes more slowly for objects moving at high speeds relative\n"
            "to an observer."
        )
        clocks_layout = QVBoxLayout()
        self.clocks = TimeDilationClocks()
        clocks_layout.addWidget(self.clocks)
        self.clocks_group.setLayout(clocks_layout)

    def create_plots(self):
        """Create all plot widgets."""
        # Create grid layout for plots
        plots_widget = QWidget()
        plots_layout = QGridLayout()
        plots_layout.setSpacing(15)  # Increased spacing between plots
        
        # Set minimum sizes for plot widgets
        plot_min_size = QSize(300, 220)  # Increased minimum size for plots
        
        # Directional Analogy Plot (Top Left)
        self.analogy_group = QGroupBox("Relative Motion")
        self.analogy_group.setMinimumSize(plot_min_size)
        self.analogy_group.setToolTip(
            "This diagram illustrates how moving through space affects your passage through time\n"
            "in special relativity. The red arrow represents the object's velocity relative to\n"
            "an observer. As speed increases, the object moves more through space and less through\n"
            "time, similar to changing direction while walking splits your movement between north and east."
        )
        analogy_layout = QVBoxLayout()
        self.analogy_plot = pg.PlotWidget(title="Motion Effects")
        self.analogy_plot.setMinimumSize(300, 200)
        self.analogy_plot.setAspectLocked(True)
        self.analogy_plot.setXRange(-1.2, 1.2)
        self.analogy_plot.setYRange(-1.2, 1.2)
        self.analogy_plot.setLabel('left', "Time")
        self.analogy_plot.setLabel('bottom', "Velocity")
        analogy_layout.addWidget(self.analogy_plot)
        self.analogy_group.setLayout(analogy_layout)
        plots_layout.addWidget(self.analogy_group, 0, 0)
        
        # Space-Time Circle Plot (Top Right)
        self.spacetime_group = QGroupBox("Space-Time")
        self.spacetime_group.setMinimumSize(plot_min_size)
        self.spacetime_group.setToolTip(
            "This plot visualizes the relationship between space and time in special relativity\n"
            "using a circle. Each point on the circle represents a combination of space and time\n"
            "measurements that together reach the speed of light (the circle's constant radius).\n"
            "As an object moves faster through space (rightward), it moves slower through time\n"
            "(upward), illustrating time dilation and length contraction."
        )
        spacetime_layout = QVBoxLayout()
        self.spacetime_plot = pg.PlotWidget(title="Measurements")
        self.spacetime_plot.setMinimumSize(300, 200)
        self.spacetime_plot.setAspectLocked(True)
        self.spacetime_plot.setXRange(0, 1.1)
        self.spacetime_plot.setYRange(0, 1.1)
        self.spacetime_plot.setLabel('left', "Space")
        self.spacetime_plot.setLabel('bottom', "Time")
        spacetime_layout.addWidget(self.spacetime_plot)
        self.spacetime_group.setLayout(spacetime_layout)
        plots_layout.addWidget(self.spacetime_group, 0, 1)
        
        # Time Dilation Plot (Bottom Left)
        self.time_dilation_group = QGroupBox("Time Dilation")
        self.time_dilation_group.setMinimumSize(plot_min_size)
        self.time_dilation_group.setToolTip(
            "This graph shows **time dilation**—how time slows down for a moving object compared\n"
            "to a stationary observer. As the object's speed approaches the speed of light,\n"
            "its clock ticks more slowly, meaning less time passes for it than for the observer."
        )
        time_dilation_layout = QVBoxLayout()
        self.time_dilation_plot = pg.PlotWidget(title="Time Slowing")
        self.time_dilation_plot.setMinimumSize(300, 200)
        self.time_dilation_plot.setLabel('left', "Time (%)")
        self.time_dilation_plot.setLabel('bottom', "Velocity (%c)")
        self.time_dilation_plot.showGrid(x=True, y=True)
        self.time_dilation_plot.setYRange(0, 100)
        time_dilation_layout.addWidget(self.time_dilation_plot)
        self.time_dilation_group.setLayout(time_dilation_layout)
        plots_layout.addWidget(self.time_dilation_group, 1, 0)
        
        # Lorentz Factor Plot (Bottom Right)
        self.lorentz_group = QGroupBox("Lorentz Factor")
        self.lorentz_group.setMinimumSize(plot_min_size)
        self.lorentz_group.setToolTip(
            "This plot displays the **Lorentz factor (γ)**, which tells you how much time dilation\n"
            "and length contraction occur at different speeds. A higher γ means stronger\n"
            "relativistic effects, noticeable when moving close to the speed of light."
        )
        lorentz_layout = QVBoxLayout()
        self.lorentz_plot = pg.PlotWidget(title="Relativistic Effects")
        self.lorentz_plot.setMinimumSize(300, 200)
        self.lorentz_plot.setLabel('left', "γ")
        self.lorentz_plot.setLabel('bottom', "Velocity (%c)")
        self.lorentz_plot.showGrid(x=True, y=True)
        self.lorentz_plot.setLogMode(y=True)
        lorentz_layout.addWidget(self.lorentz_plot)
        self.lorentz_group.setLayout(lorentz_layout)
        plots_layout.addWidget(self.lorentz_group, 1, 1)
        
        plots_widget.setLayout(plots_layout)
        self.vis_layout.addWidget(plots_widget)
        
        # Initialize plot elements
        self.plots['direction_arrow'] = self.plot_manager.setup_analogy_plot(self.analogy_plot)
        self.plots['time_marker'] = self.plot_manager.setup_time_dilation_plot(self.time_dilation_plot)
        self.plots['spacetime_point'] = self.plot_manager.setup_spacetime_plot(self.spacetime_plot)
        self.plots['lorentz_marker'] = self.plot_manager.setup_lorentz_plot(self.lorentz_plot)

    def update_explanation_style(self):
        """Update explanation label style."""
        self.explanation.setStyleSheet(
            f"QLabel {{ background-color: {self.current_theme['background']}; "
            f"color: {self.current_theme['text']}; padding: 10px; font-size: 10pt; }}"
        )

    def update_info_style(self):
        """Update info label style."""
        self.info_label.setStyleSheet(
            f"QLabel {{ background-color: {self.current_theme['background']}; "
            f"color: {self.current_theme['text']}; padding: 10px; font-size: 10pt; }}"
        )

    def get_mass_kg(self):
        """Get mass in kilograms from input."""
        try:
            mass_lbs = float(self.mass_input.text())
            mass_kg = RelativisticCalculator.mass_lbs_to_kg(mass_lbs)
            self.mass_kg_label.setText(f"{mass_kg:.3f} kg")
            return mass_kg
        except ValueError:
            return 1.0

    def update_plots(self):
        """Update all plots and displays."""
        velocity_ratio = self.slider.value() / 1000  # Divide by 1000 for 99.9%
        mass_kg = self.get_mass_kg()
        
        # Update clocks
        self.clocks.set_velocity(velocity_ratio)
        
        # Update slider label with real-world comparison
        speed_ms = velocity_ratio * 299792458  # Speed in m/s
        comparison = self.get_speed_comparison(speed_ms)
        self.slider_label.setText(
            f'{velocity_ratio*100:.1f}% c\n'  # Show one decimal place
            f'({speed_ms:.1f} m/s - {comparison})'
        )
        
        # Update plots and get results
        results = self.plot_manager.update_plots(velocity_ratio, mass_kg, self.plots)
        
        # Update info display with enhanced explanations
        gamma = RelativisticCalculator.gamma(velocity_ratio)
        info_text = (
            f'Time Dilation:\n'
            f'• A clock moving at this speed appears to tick slower when observed from Earth\n'
            f'• If the clock emits regular light signals (like a pulsar\'s radio pulses),\n'
            f'  Earth observers measure {1/results["time_component"]:.2f} seconds between signals\n'
            f'  even though the moving clock is emitting them every 1 second\n\n'
            f'Relativistic Effects:\n'
            f'• Lorentz factor (γ): {results["gamma_val"]:.2f}\n'
            f'• Length contraction: The moving object appears {results["time_component"]*100:.1f}% as long\n\n'
            f'Energy (E = γmc²):\n'
            f'• Rest mass: {mass_kg:.3f} kg ({mass_kg*2.20462:.1f} lbs)\n'
            f'• Rest energy (E₀ = mc²): {results["energies"]["rest_energy"]/1e9:.1f} GJ\n'
            f'• Total energy: {results["energies"]["total_energy"]/1e9:.1f} GJ\n'
            f'• Kinetic energy: {results["energies"]["kinetic_energy"]/1e9:.1f} GJ\n'
            f'  ({self.get_energy_comparison(results["energies"]["total_energy"])})'
        )
        self.info_label.setText(info_text)

    def get_speed_comparison(self, speed_ms):
        """Get a real-world comparison for the current speed."""
        if speed_ms < 1:
            return "slower than a snail"
        elif speed_ms < 5:
            return "about walking speed"
        elif speed_ms < 15:
            return "about running speed"
        elif speed_ms < 50:
            return "faster than Usain Bolt"
        elif speed_ms < 300:
            return "faster than a cheetah"
        elif speed_ms < 1000:
            return "faster than a bullet"
        elif speed_ms < 8000:
            return "faster than the Space Station"
        elif speed_ms < 30000:
            return "faster than any spacecraft"
        else:
            return "approaching light speed"

    def get_energy_comparison(self, energy_joules):
        """Get a real-world comparison for the current energy."""
        if energy_joules < 1e6:
            return f"equivalent to {energy_joules/4184:.1f} food Calories"
        elif energy_joules < 1e9:
            return f"equivalent to {energy_joules/1e6:.1f} kg of TNT"
        elif energy_joules < 1e12:
            return f"equivalent to {energy_joules/1e9:.1f} tons of TNT"
        elif energy_joules < 1e15:
            return f"equivalent to {energy_joules/1e12:.1f} kilotons of TNT"
        else:
            return f"equivalent to {energy_joules/1e15:.1f} megatons of TNT"

    def validate_mass_input(self):
        """Validate mass input and show error message if invalid."""
        try:
            mass = float(self.mass_input.text())
            if mass <= 0:
                self.mass_error_label.setText("Mass must be greater than 0")
                return False
            elif mass > 1e12:
                self.mass_error_label.setText("Mass must be less than 1e12 lbs")
                return False
            else:
                self.mass_error_label.setText("")
                self.update_plots()
                return True
        except ValueError:
            if self.mass_input.text():  # Only show error if there's input
                self.mass_error_label.setText("Please enter a valid number")
            return False
