"""
Physics calculations for special relativity visualizations.

This module provides a collection of static methods for calculating various
relativistic effects including time dilation and energy calculations.
All calculations assume c = 1 (natural units) unless otherwise specified.

Note: In modern physics, we prefer to discuss energy rather than "relativistic mass".
The concept of mass changing with velocity (relativistic mass) is outdated.
Instead, we work with invariant rest mass and discuss how total energy changes with velocity.
"""

import numpy as np
from .config import SPEED_OF_LIGHT

class RelativisticCalculator:
    """
    A utility class for relativistic calculations.
    
    All methods are static and take velocity ratios (v/c) as input
    to maintain precision and avoid floating-point errors with large
    numbers when using actual velocities.
    """
    
    @staticmethod
    def gamma(velocity_ratio):
        """
        Calculate the Lorentz factor γ = 1/√(1-v²/c²).
        
        Args:
            velocity_ratio (float): Ratio of velocity to speed of light (v/c)
            
        Returns:
            float: Lorentz factor γ
        """
        return 1 / np.sqrt(1 - velocity_ratio**2)
    
    @staticmethod
    def time_dilation(velocity_ratio):
        """
        Calculate time dilation factor.
        
        Args:
            velocity_ratio (float): Ratio of velocity to speed of light (v/c)
            
        Returns:
            float: Time dilation factor
        """
        return 1 / RelativisticCalculator.gamma(velocity_ratio)
    
    @staticmethod
    def energy_calculations(rest_mass, velocity_ratio):
        """
        Calculate various energy values.
        
        In special relativity, the total energy increases with velocity while the rest mass
        remains constant. The additional energy manifests as kinetic energy.
        
        Args:
            rest_mass (float): Invariant mass of the object in kg (does not change with velocity)
            velocity_ratio (float): Ratio of velocity to speed of light (v/c)
            
        Returns:
            dict: Dictionary containing rest energy (E₀ = mc²), 
                 total energy (E = γmc²), and 
                 kinetic energy (K = mc²(γ-1))
        """
        gamma_val = RelativisticCalculator.gamma(velocity_ratio)
        rest_energy = rest_mass * SPEED_OF_LIGHT**2
        total_energy = rest_energy * gamma_val
        kinetic_energy = rest_energy * (gamma_val - 1)
        
        return {
            'rest_energy': rest_energy,
            'total_energy': total_energy,
            'kinetic_energy': kinetic_energy
        }
    
    @staticmethod
    def spacetime_components(velocity_ratio):
        """
        Calculate space and time components for visualization purposes.
        
        Note: This is a simplified visualization using a circle to build intuition.
        In actual spacetime geometry (Minkowski space), the relationship between
        space and time components forms a hyperbola, not a circle. This circular
        representation is a pedagogical tool to help visualize how motion through
        space affects the rate of time passage, but it should not be taken as a
        literal geometric representation of spacetime.
        
        Args:
            velocity_ratio (float): Ratio of velocity to speed of light (v/c)
            
        Returns:
            tuple: Time component and space component (for visualization purposes)
        """
        gamma_val = RelativisticCalculator.gamma(velocity_ratio)
        time_component = 1 / gamma_val
        space_component = velocity_ratio
        
        return time_component, space_component
    
    @staticmethod
    def direction_angle(velocity_ratio):
        """
        Calculate direction angle from vertical.
        
        Args:
            velocity_ratio (float): Ratio of velocity to speed of light (v/c)
            
        Returns:
            float: Direction angle in radians
        """
        time_component, space_component = RelativisticCalculator.spacetime_components(velocity_ratio)
        angle = np.pi/2 - np.arctan2(space_component, time_component)
        return angle
    
    @staticmethod
    def create_arrow_coordinates(angle, length=1.0, head_size=0.1):
        """
        Create coordinates for an arrow with a proper head.
        
        Args:
            angle (float): Angle of the arrow in radians
            length (float, optional): Length of the arrow. Defaults to 1.0.
            head_size (float, optional): Size of the arrow head. Defaults to 0.1.
            
        Returns:
            tuple: x and y coordinates of the arrow
        """
        # Main line
        cos_a = np.cos(angle) * length
        sin_a = np.sin(angle) * length
        
        # Arrow head
        head_angle = 20 * np.pi / 180  # 20 degree head
        left_angle = angle + np.pi - head_angle
        right_angle = angle + np.pi + head_angle
        
        head_cos_l = cos_a + np.cos(left_angle) * head_size
        head_sin_l = sin_a + np.sin(left_angle) * head_size
        head_cos_r = cos_a + np.cos(right_angle) * head_size
        head_sin_r = sin_a + np.sin(right_angle) * head_size
        
        # Create x and y coordinates for the full arrow
        x_coords = [0, cos_a, head_cos_l, cos_a, head_cos_r]
        y_coords = [0, sin_a, head_sin_l, sin_a, head_sin_r]
        
        return x_coords, y_coords

    @staticmethod
    def mass_lbs_to_kg(mass_lbs):
        """
        Convert mass from pounds to kilograms.
        
        Args:
            mass_lbs (float): Mass in pounds
            
        Returns:
            float: Mass in kilograms
        """
        return mass_lbs * 0.45359237
    
    @staticmethod
    def mass_kg_to_lbs(mass_kg):
        """
        Convert mass from kilograms to pounds.
        
        Args:
            mass_kg (float): Mass in kilograms
            
        Returns:
            float: Mass in pounds
        """
        return mass_kg * 2.20462
