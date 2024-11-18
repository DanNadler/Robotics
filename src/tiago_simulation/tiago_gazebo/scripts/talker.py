#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tiago_gazebo.msg import Order  # Replace with your package name
import random
import time

class OrderPublisher(Node):
    def __init__(self):
        super().__init__('order_talker')
        self.publisher_ = self.create_publisher(Order, 'orders', 10)
        self.count = 0
        time.sleep(10)
        self.publish_order()
        # self.timer = self.create_timer(30, self.publish_order)  # 60 seconds
        self.get_logger().info('Order talker node has started.')


    def publish_order(self):
        self.count = self.count + 1
        if self.count<=10:
            order = Order()
            order.destination_table_number = random.randint(1, 4)
            #order.item = random.choice(["item1", "item2", "item3"])
            order.item = "coca cola"
            self.publisher_.publish(order)
            self.get_logger().info(f'Published new order to table: {order.destination_table_number} with items: {order.item}, count is {self.count}')
        else:
            # Stop the publisher after 10 messages
            self.get_logger().info('Max messages published. Shutting down publisher.')
            self.timer.cancel()  # Stop the timer to prevent further publishing


def main(args=None):
    rclpy.init(args=args)
    node = OrderPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
