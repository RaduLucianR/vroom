#include <chrono>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"

#include "vroomWPi.h"

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  initWiringPi();
  enableWheels();
  
  rclcpp::shutdown();
  return 0;
}
