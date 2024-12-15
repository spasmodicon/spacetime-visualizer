from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QGraphicsView, QGraphicsScene)
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QFont
import math

class ClockWidget(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.setup_ui(title)
    
    def setup_ui(self, title):
        """Setup the clock widget UI."""
        layout = QVBoxLayout()
        layout.setSpacing(2)  # Reduced spacing
        
        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 9pt; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Clock face
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(80, 80)  # Reduced from default size
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.view)
        
        # Draw clock face
        self.scene.setSceneRect(-30, -30, 60, 60)  # Reduced scene size
        self.scene.addEllipse(-30, -30, 60, 60, QPen(Qt.black), QBrush(QColor(240, 240, 240)))
        
        # Add hour markers
        for i in range(12):
            angle = i * 30
            rad = math.radians(angle)
            
            # Calculate start and end points for hour markers
            start_x = 28 * math.sin(rad)
            start_y = -28 * math.cos(rad)
            end_x = 32 * math.sin(rad)
            end_y = -32 * math.cos(rad)
            
            # Draw hour marker
            self.scene.addLine(start_x, start_y, end_x, end_y,
                             QPen(Qt.black, 2))
            
            # Add hour numbers
            if i > 0:  # Skip 0/12 position
                number = str(i)
                text = self.scene.addText(number)
                text.setFont(QFont("Arial", 8))
                # Position numbers slightly inside the hour markers
                text.setPos(24 * math.sin(rad) - text.boundingRect().width()/2,
                          -24 * math.cos(rad) - text.boundingRect().height()/2)
        
        # Create clock hand
        self.hand = self.scene.addLine(0, 0, 0, -25, 
                                     QPen(QColor(255, 0, 0), 2))  # Reduced hand length
        
        # Digital time display
        self.time_label = QLabel("0.00 s")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 9pt;")
        layout.addWidget(self.time_label)
        
        self.setLayout(layout)
    
    def update_time(self, seconds, dilated=False):
        """Update the clock hand position and digital display."""
        # Update angle (360 degrees per 12 seconds)
        self.angle = (seconds % 12) * 30
        
        # Rotate hand
        self.hand.setRotation(self.angle)
        
        # Update digital display
        if dilated:
            self.time_label.setText(f"{seconds:.2f} s (dilated)")
        else:
            self.time_label.setText(f"{seconds:.2f} s")

class TimeDilationClocks(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.elapsed_time = 0
        
        # Setup update timer (50ms for smooth animation)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clocks)
        self.timer.start(50)  # 50ms = 20 fps
    
    def setup_ui(self):
        """Setup the clocks layout."""
        layout = QHBoxLayout()
        
        # Create stationary and moving clocks
        self.stationary_clock = ClockWidget("Stationary Observer")
        self.moving_clock = ClockWidget("Moving Observer")
        
        # Add explanation label
        self.explanation = QLabel(
            "These clocks show how time passes differently for moving objects.\n"
            "The moving clock ticks more slowly due to time dilation."
        )
        self.explanation.setWordWrap(True)
        self.explanation.setStyleSheet("font-size: 9pt;")
        
        # Create vertical layout for explanation and clocks
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.explanation)
        
        # Create horizontal layout for clocks
        clocks_layout = QHBoxLayout()
        clocks_layout.addWidget(self.stationary_clock)
        clocks_layout.addWidget(self.moving_clock)
        
        content_layout.addLayout(clocks_layout)
        layout.addLayout(content_layout)
        
        self.setLayout(layout)
    
    def update_clocks(self):
        """Update both clocks based on current velocity."""
        # Update elapsed time (50ms = 0.05s real time)
        self.elapsed_time += 0.05
        
        # Update stationary clock
        self.stationary_clock.update_time(self.elapsed_time)
        
        # Update moving clock with time dilation
        if hasattr(self, 'time_dilation_factor'):
            dilated_time = self.elapsed_time * self.time_dilation_factor
            self.moving_clock.update_time(dilated_time, dilated=True)
    
    def set_velocity(self, velocity_ratio):
        """Set the velocity and update time dilation factor."""
        # Calculate time dilation factor
        self.time_dilation_factor = math.sqrt(1 - velocity_ratio**2)
        
        # Update explanation text
        if velocity_ratio > 0:
            rate = self.time_dilation_factor * 100
            self.explanation.setText(
                f"These clocks show how time passes differently for moving objects.\n"
                f"At {velocity_ratio*100:.1f}% of light speed, time flows at {rate:.1f}% "
                f"of normal rate."
            )
        else:
            self.explanation.setText(
                "These clocks show how time passes differently for moving objects.\n"
                "The moving clock ticks more slowly due to time dilation."
            )
