#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/bool.hpp"

#include "vroomWPi.h"

class WheelEnabler : public rclcpp::Node
{
public:
  WheelEnabler()
  : Node("wheelEnabler")
  {
	initWiringPi();
	disableWheels();
	
    auto topic_callback =
      [this](std_msgs::msg::Bool::UniquePtr msg) -> void {
		  if (lastRequest == false && msg->data == true) {
			 RCLCPP_INFO(this->get_logger(), "I heard: '%d'", msg->data);
			 enableWheels();
			 lastRequest = true;
			 return;
		  }
		  
		  if (lastRequest == true && msg->data == false) {
			 RCLCPP_INFO(this->get_logger(), "I heard: '%d'", msg->data);
			 disableWheels();
			 lastRequest = false;
			 return;
		  }
      };
      
    subscription_ = this->create_subscription<std_msgs::msg::Bool>("enable_wheels", 10, topic_callback);
  }

private:
  bool lastRequest = false;
  rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<WheelEnabler>());
  rclcpp::shutdown();
  return 0;
}
