import random

class NotificationSystem:
    def __init__(self, threshold):
        self.threshold = threshold
        self.notifications_sent = 0
        self.probability = 1.0  # initial probability of sending a notification

    def send_notification(self):
        # Simulate sending a notification based on the current probability
        if random.random() < self.probability:
            self.notifications_sent += 1
            return True
        return False

    def adjust_probability(self, threshold = 4):
        if self.notifications_sent > threshold:
            # Decrease the probability if we've sent more than the threshold
            self.probability *= 0.9
        else:
            # Increase the probability if we've sent less than the threshold
            self.probability *= 1.1

        # Reset the count for the next week
        self.notifications_sent = 0
    
    def accept(self, threshold = 4):
        if self.notifications_sent > threshold:
            # Decrease the probability if we've sent more than the threshold
            self.probability *= 0.9
        else:
            # Increase the probability if we've sent less than the threshold
            self.probability *= 1.1

        # Reset the count for the next week
        self.notifications_sent = 0