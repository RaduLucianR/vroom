#include <chrono>
#include <memory>
#include <string>
#include <thread>

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <libevdev-1.0/libevdev/libevdev.h>
#include <errno.h>
#include <string.h>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "vroom_interf/msg/xbox.hpp"

using namespace std::chrono_literals;

class XboxInputProcessor : public rclcpp::Node
{
public:
  XboxInputProcessor()
  : Node("xboxInputProcessor"), running_(true)
  {
    publisher_ = this->create_publisher<vroom_interf::msg::Xbox>("xboxInput", 10);
	
	const char *device_path = "/dev/input/event7";  // Replace with your device path
    while ((fd_ = open(device_path, O_RDONLY | O_NONBLOCK)) < 0) {
        RCLCPP_ERROR(this->get_logger(), "Failed to open device, retrying in 3 seconds...");
        sleep(3);
    }

    dev = NULL;
    int rc = libevdev_new_from_fd(fd_, &dev);
    if (rc < 0) {
        RCLCPP_ERROR(this->get_logger(), "Failed to initialize libevdev (%s)", strerror(-rc));
        close(fd_);
        return;
    }

    RCLCPP_INFO(this->get_logger(), "Input device name: \"%s\"", libevdev_get_name(dev));
    RCLCPP_INFO(this->get_logger(), "Input device ID: bus %#x vendor %#x product %#x",
           libevdev_get_id_bustype(dev),
           libevdev_get_id_vendor(dev),
           libevdev_get_id_product(dev));
    
    readEvent();
  }
  
  ~XboxInputProcessor() {
	  running_ = false;
	  
	  if(fd_ >= 0) {
		  close(fd_);
	  }
	  
	  libevdev_free(dev);
  }

private:
  rclcpp::Publisher<vroom_interf::msg::Xbox>::SharedPtr publisher_;
  int fd_;
  std::atomic<bool> running_;
  struct libevdev *dev;
  
  
  void readEvent() {
	  struct input_event ev;
	  int rc;
	  vroom_interf::msg::Xbox message = vroom_interf::msg::Xbox();
	  
	  while(rclcpp::ok() && running_) {
		rc = libevdev_next_event(dev, LIBEVDEV_READ_FLAG_NORMAL, &ev);
        if (rc == 0) {
            message.type = ev.type;
            message.code = ev.code;
            
            if (ev.type == 1) {
				
				if (ev.code == 304) {
					RCLCPP_INFO(this->get_logger(), "'A' button");
					message.value = ev.value;
					publisher_->publish(message);
				}
			}
            if (ev.type == 3) {
				message.type = 3;
				
				if (ev.code == 2) {
					RCLCPP_INFO(this->get_logger(), "Left big button");
					message.value = ev.value;
					publisher_->publish(message);
				}
				
				if (ev.code == 5) {
					RCLCPP_INFO(this->get_logger(), "Right big button");
					message.value = ev.value;
					publisher_->publish(message);
				}
				
				if (ev.code == 0) {
					if (ev.value > 0) {
						RCLCPP_INFO(this->get_logger(), "Right");
						message.value = ev.value;
						publisher_->publish(message);
					}
					
					if (ev.value < 0) {
						RCLCPP_INFO(this->get_logger(), "Left");
						message.value = ev.value;
						publisher_->publish(message);
					}
				}
			}
        } else if (rc == -EAGAIN) {
            // No events available right now; you can sleep or do other work here.
            usleep(10000);
        } else {
            fprintf(stderr, "Error reading event: %s\n", strerror(-rc));
            break;
        }
	  }
  }
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<XboxInputProcessor>());
  rclcpp::shutdown();
  return 0;
}
