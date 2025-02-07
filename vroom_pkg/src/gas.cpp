#include <memory>
#include <sstream>
#include <cstdlib>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"

#include "vroomWPi.h"

class Gas : public rclcpp::Node
{
public:
  Gas()
  : Node("gas")
  {
	initWiringPi();
	
    auto topic_callback =
      [this](std_msgs::msg::Float64::UniquePtr msg) -> void {
        RCLCPP_INFO(this->get_logger(), "I heard: '%f'", msg->data);
        std::string pwmRange = "gpio pwmr 100";
        
        if (msg->data > 0) {
			forwards();
			std::ostringstream oss;
			oss << "gpio pwm 1 " << msg->data;
			std::string command = oss.str();
			system(pwmRange.c_str());
			system(command.c_str());
		} else {
			backwards();
			std::ostringstream oss;
			float val = msg->data * (-1);
			oss << "gpio pwm 1 " << val;
			std::string command = oss.str();
			system(pwmRange.c_str());
			system(command.c_str());
		}
      };
      
    subscription_ =
      this->create_subscription<std_msgs::msg::Float64>("velocity", 10, topic_callback);
  }

private: 
  rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Gas>());
  rclcpp::shutdown();
  return 0;
}
