import numpy as np

class PowerCalculator:

    def __init__(self, watts, time):
        """
        Initialize the PowerCalculator with power (watts) and time data.
        
        Args:
            watts (list): List of power data points in watts.
            time (list): List of corresponding time data points in seconds.
        """
        self.watts = [w if w is not None else 150 for w in watts]  # Replace None with 150
        self.time = time
    
    def get_max_power(self, duration):
        """
        Calculate the maximum average power over a specified duration.
        
        Args:
            duration (int): The duration in seconds for which to calculate max average power.
            
        Returns:
            float: The maximum average power over the specified duration.
        """
        if not self.watts or not self.time:
            raise ValueError("Watts and time data must be provided.")

        target_duration = duration
        
        if self.time[-1] - self.time[0] < target_duration:
            print(f"Not enough data for a {duration // 60}-minute/second window.")
            raise ValueError(f"Not enough data for a {duration // 60}-minute/second window.")
        
        max_avg_power = 0
        start_index = 0
        
        for i in range(1, len(self.time)):
            while self.time[i] - self.time[start_index] >= target_duration:
                current_window_sum = sum(self.watts[start_index:i])
                current_duration = self.time[i] - self.time[start_index]
                current_avg_power = current_window_sum / current_duration
                if current_avg_power > max_avg_power:
                    max_avg_power = current_avg_power
                start_index += 1
        
        return max_avg_power
    
    def calculate_normalized_power(self):
        """
        Calculate the normalized power over the provided watts data.

        Raises:

        
        Returns:
            float: The normalized power.
        """
        window_size = 30
        
        if len(self.watts) < window_size:
            print("Not enough data for the calculation.")
            raise Exception("Not enough data for the calculation.")
        
        rolling_powers = np.convolve(self.watts, np.ones(window_size)/window_size, mode='valid')
        rolling_powers_fourth = np.power(rolling_powers, 4)
        average_of_fourth_powers = np.mean(rolling_powers_fourth)
        normalized_power = np.power(average_of_fourth_powers, 0.25)
        
        return normalized_power
    
    def get_average_power(self):
        """
        Calculate the average power over the provided watts data.
        
        Returns:
            float: The average power.
        """
        return np.mean(self.watts)
    
    def get_intensity_factor(self, ftp):
        """
        Calculate the intensity factor.
        
        Returns:
            float: The intensity factor.
        """
        return self.calculate_normalized_power() / ftp

    def get_training_stress_score(self, ftp):
        """
        Calculate the training stress score.
        
        Returns:
            float: The training stress score.
        """
        intensity_factor = self.get_intensity_factor(ftp)
        return (self.calculate_normalized_power() * intensity_factor * len(self.time)) / (ftp * 3600) * 100