#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/float64.hpp"
#include "std_msgs/msg/bool.hpp"

#include "vroom_interf/msg/xbox.hpp"

class Controller : public rclcpp::Node
{
public:
  Controller()
  : Node("controller")
  {
	pub_Vel_ = this->create_publisher<std_msgs::msg::Float64>("velocity", 10);
	pub_EnableWheels_ = this->create_publisher<std_msgs::msg::Bool>("enable_wheels", 10);
	  
    auto xbox_callback =
      [this](vroom_interf::msg::Xbox::UniquePtr msg) -> void {
        RCLCPP_INFO(this->get_logger(), "I heard: '%d'", msg->type);
        
        if (msg->type == 1) {
				if (msg->code == 304) {
					if (msg->value == 1) {
						std_msgs::msg::Bool enable_msg = std_msgs::msg::Bool();
						
						if (relayValue_ == true) {
							enable_msg.data = false;
							pub_EnableWheels_->publish(enable_msg);
							relayValue_ = false;
						} else {
							enable_msg.data = true;
							pub_EnableWheels_->publish(enable_msg);
							relayValue_ = true;
						}
					}
				}
			}
            if (msg->type == 3) {
				if (msg->code == 2) {
					RCLCPP_INFO(this->get_logger(), "Left big button");
					
					float val_speed = 65.0f / 1023.0f * msg->value + 35.0f;
					std_msgs::msg::Float64 vel = std_msgs::msg::Float64();
					vel.data = val_speed;
					pub_Vel_->publish(vel);
				}
				
				if (msg->code == 5) {
					RCLCPP_INFO(this->get_logger(), "Right big button");
					float val_speed = 65.0f / 1023.0f * msg->value + 35.0f;
					val_speed *= -1;
					std_msgs::msg::Float64 vel = std_msgs::msg::Float64();
					vel.data = val_speed;
					pub_Vel_->publish(vel);
				}
				
				//~ if (msg->code == 0) {
					//~ if (msg->value > 0) {
						//~ RCLCPP_INFO(this->get_logger(), "Right");
						//~ message.value = ev.value;
						//~ publisher_->publish(message);
					//~ }
					
					//~ if (msg->value < 0) {
						//~ RCLCPP_INFO(this->get_logger(), "Left");
						//~ message.value = ev.value;
						//~ publisher_->publish(message);
					//~ }
				//~ }
			}
      };
      
      
    sub_Xbox_ =
      this->create_subscription<vroom_interf::msg::Xbox>("xboxInput", 10, xbox_callback);
  }

private:
  bool relayValue_ = false;
  rclcpp::Subscription<vroom_interf::msg::Xbox>::SharedPtr sub_Xbox_;
  rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr pub_Vel_;
  rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr pub_EnableWheels_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Controller>());
  rclcpp::shutdown();
  return 0;
}
