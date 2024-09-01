import matplotlib.pyplot as plt
import numpy as np
import datetime
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Wedge
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class DailySchedule:
    def __init__(self):
        self.activities = {
            "Ngủ": list(range(22, 24)) + list(range(0, 5)),
            "Dậy": range(5, 6),
            "Ăn sáng": range(6, 7),
            "Code": range(9, 11),
            "Ăn trưa": range(11, 13),
            "Nghỉ": range(13, 15),
            "Học": range(15, 17),
            "Xem phim": range(17, 19),
            "Ăn tối": range(19, 21),
            "Play": range(21, 22)
        }

    def get_current_activity(self):
        current_hour = datetime.datetime.now().hour
        for activity, hours in self.activities.items():
            if current_hour in hours:
                return activity
        return "Ngủ"  # Default to sleeping if hour is 0

class ClockPlot:
    def __init__(self):
        self.schedule = DailySchedule()
        self.fig, self.ax = plt.subplots(figsize=(10, 10), facecolor='#F0F0F0')
        self.ax.set_aspect('equal')
        self.fig.suptitle("Today's Time Table", fontsize=20, color='pink', y=1) 

    def draw_clock_face(self):
        # Draw outer circle
        outer_circle = plt.Circle((0, 0), 1, fill=False, color='#333333', linewidth=1)
        self.ax.add_artist(outer_circle)

        # Draw inner circle
        inner_circle = plt.Circle((0, 0), 0.97, fill=False, color='#333333', linewidth=1)
        self.ax.add_artist(inner_circle)

        # Draw activity sectors
        colors = plt.cm.Set3(np.linspace(0, 1, len(self.schedule.activities)))
        for i, (activity, hours) in enumerate(self.schedule.activities.items()):
            start_hour = hours[0]
            end_hour = hours[-1] + 1
            start_angle = 90 - start_hour * 15
            end_angle = 90 - end_hour * 15
            wedge = Wedge((0, 0), 0.968, end_angle, start_angle, width=0.028, 
                          facecolor=colors[i], edgecolor='white', alpha=0.7)
            self.ax.add_patch(wedge)

            # Draw dividing lines at the start and end of each activity
            for hour in [start_hour, end_hour]:
                angle = np.radians(90 - hour * 15)
                x, y = 0.925 * np.cos(angle), 0.925 * np.sin(angle)
                self.ax.plot([0, x], [0, y], color='#c0c0c0', lw=1)
           # Add activity names
            mid_hour = (start_hour + end_hour) / 2
            mid_angle = 90 - mid_hour * 15
            x, y = 0.72 * np.cos(np.radians(mid_angle)), 0.72 * np.sin(np.radians(mid_angle))
            if activity == "Ngủ":
                rotation_angle = 0
                # Add sleep image within the sector
                img = plt.imread(r'sleepimage.png')  # Replace with your image path
                imagebox = OffsetImage(img, zoom=0.1)
                ab = AnnotationBbox(imagebox, (0.2 * np.cos(np.radians(90 - 3 * 15)), 
                                               0.95 * np.sin(np.radians(90 - 3 * 15))), 
                                    frameon=False, box_alignment=(0.5, 0.5))
                self.ax.add_artist(ab)
                # Add "Ngủ" text
                self.ax.text(0.45 * np.cos(np.radians(90 - 3 * 15)), 
                             0.75 * np.sin(np.radians(90 - 3 * 15)), activity, 
                             ha='center', va='center', fontsize=17, color='#333333')
            else:
                rotation_angle = mid_angle if mid_angle > -90 and mid_angle < 90 else mid_angle + 180
                self.ax.text(x, y, activity, ha='center', va='center', fontsize=17, 
                             color='#333333', rotation=rotation_angle, rotation_mode='anchor')
        # Draw hour marks
        for hour in range(24):
            angle = np.radians(90 - hour * 15)
            x1, y1 = 0.97 * np.cos(angle), 0.97 * np.sin(angle)
            x2, y2 = np.cos(angle), np.sin(angle)
            lw = 3 if hour in [12, 24] else 1  # Make the lines at 12 and 24 hours thicker
            self.ax.plot([x1, x2], [y1, y2], 'k-', lw=lw)
            self.ax.text(1.05*x2, 1.05*y2, str(hour if hour != 24 else 0), ha='center', va='center', fontsize=12, 
                         fontweight='bold', color='#333333')

        self.ax.set_xlim(-1.1, 1.1)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.axis('off')

    def update(self, frame):
        self.ax.clear()
        self.draw_clock_face()

        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second

        # Hour hand
        hour_angle = np.radians(90 - (hour % 24 + minute/60) * 15)
        self.ax.plot([0, 0.5*np.cos(hour_angle)], [0, 0.5*np.sin(hour_angle)], '-', color='#0066cc', lw=4)

        # Minute hand
        minute_angle = np.radians(90 - (minute + second/60) * 6)
        self.ax.plot([0, 0.7*np.cos(minute_angle)], [0, 0.7*np.sin(minute_angle)], '-', color='#009933', lw=3)

        # Second hand
        second_angle = np.radians(90 - second * 6)
        self.ax.plot([0, 0.8*np.cos(second_angle)], [0, 0.8*np.sin(second_angle)], '-', color='#cc0000', lw=1)

        # Draw center circle
        center_circle = plt.Circle((0, 0), 0.02, facecolor='#333333', edgecolor='white', zorder=10)
        self.ax.add_artist(center_circle)

        # Current activity
        current_activity = self.schedule.get_current_activity()
        self.ax.set_title(f"Current Activity: {current_activity}", fontsize=12, fontweight='normal', color='#FFCCE5', pad=1)
        return self.ax

    def animate(self):
        anim = FuncAnimation(self.fig, self.update, frames=range(60), interval=1000, blit=False)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    clock = ClockPlot()
    clock.animate()
