import numpy as np
import pyqtgraph as pg
from .physics import RelativisticCalculator

class PlotManager:
    def __init__(self):
        self.velocities = np.linspace(0, 0.99, 1000)
        self.gamma = RelativisticCalculator.gamma(self.velocities)
        self.time_dilation = RelativisticCalculator.time_dilation(self.velocities)
        
    def setup_analogy_plot(self, plot_widget):
        """Setup the compass-like direction analogy plot."""
        # Create circle
        theta = np.linspace(0, 2*np.pi, 100)
        plot_widget.plot(np.cos(theta), np.sin(theta), pen=pg.mkPen('k', width=2))
        
        # Add compass lines
        plot_widget.plot([0, 0], [-1, 1], pen=pg.mkPen('k', width=1))
        plot_widget.plot([-1, 1], [0, 0], pen=pg.mkPen('k', width=1))
        
        # Add labels
        label_offset = 1.1
        time_label = pg.TextItem("Time\n(100%)", anchor=(0.5, 0))
        time_label.setPos(0, label_offset)
        plot_widget.addItem(time_label)
        
        space_label = pg.TextItem("Space\n(Light Speed)", anchor=(0, 0.5))
        space_label.setPos(label_offset, 0)
        plot_widget.addItem(space_label)
        
        # Initialize direction arrow
        initial_arrow_x, initial_arrow_y = RelativisticCalculator.create_arrow_coordinates(np.pi/2)
        direction_arrow = plot_widget.plot(initial_arrow_x, initial_arrow_y,
                                         pen=pg.mkPen('r', width=3))
        
        return direction_arrow
    
    def setup_time_dilation_plot(self, plot_widget):
        """Setup the time dilation curve plot."""
        # Plot time dilation curve
        plot_widget.plot(self.velocities * 100,
                        self.time_dilation * 100,
                        pen=pg.mkPen('b', width=2))
        
        # Add marker
        marker = plot_widget.plot([0], [100],
                                pen=None,
                                symbol='o',
                                symbolSize=10,
                                symbolBrush='r')
        
        return marker
    
    def setup_spacetime_plot(self, plot_widget):
        """Setup the space-time circle plot."""
        # Plot quarter circle
        theta = np.linspace(0, np.pi/2, 100)
        plot_widget.plot(np.cos(theta), np.sin(theta),
                        pen=pg.mkPen('r', width=2))
        
        # Add point marker
        point = plot_widget.plot([1], [0],
                               pen=None,
                               symbol='o',
                               symbolSize=10,
                               symbolBrush='b')
        
        return point
    
    def setup_lorentz_plot(self, plot_widget):
        """Setup the Lorentz factor plot."""
        # Plot Lorentz curve
        plot_widget.plot(self.velocities * 100, self.gamma,
                        pen=pg.mkPen('g', width=2))
        
        # Add marker
        marker = plot_widget.plot([0], [1],
                                pen=None,
                                symbol='o',
                                symbolSize=10,
                                symbolBrush='r')
        
        return marker
    
    def setup_energy_plot(self, plot_widget, rest_energy):
        """Setup the energy plot."""
        # Calculate and plot energy curve
        energies = [rest_energy * (1/np.sqrt(1-v**2)) for v in self.velocities]
        curve = plot_widget.plot(self.velocities * 100,
                               energies,
                               pen=pg.mkPen('b', width=2))
        
        # Add marker
        marker = plot_widget.plot([0], [rest_energy],
                                pen=None,
                                symbol='o',
                                symbolSize=10,
                                symbolBrush='r')
        
        return curve, marker
    
    def update_plots(self, velocity_ratio, mass_kg, plots):
        """Update all plot markers with new values."""
        # Calculate values
        gamma_val = RelativisticCalculator.gamma(velocity_ratio)
        time_component, space_component = RelativisticCalculator.spacetime_components(velocity_ratio)
        angle = RelativisticCalculator.direction_angle(velocity_ratio)
        energies = RelativisticCalculator.energy_calculations(mass_kg, velocity_ratio)
        
        # Update direction arrow
        arrow_x, arrow_y = RelativisticCalculator.create_arrow_coordinates(angle)
        plots['direction_arrow'].setData(arrow_x, arrow_y)
        
        # Update markers
        v_percent = velocity_ratio * 100
        time_percent = time_component * 100
        
        plots['time_marker'].setData([v_percent], [time_percent])
        plots['spacetime_point'].setData([time_component], [space_component])
        plots['lorentz_marker'].setData([v_percent], [gamma_val])
        
        return {
            'gamma_val': gamma_val,
            'time_component': time_component,
            'space_component': space_component,
            'angle_degrees': (np.pi/2 - angle) * 180/np.pi,
            'energies': energies
        }
