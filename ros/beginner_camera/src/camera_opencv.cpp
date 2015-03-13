#include "ros/ros.h"
#include <sensor_msgs/fill_image.h>

#include <image_transport/image_transport.h>
#include <sstream>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "image");
    ros::NodeHandle n;
    image_transport::Publisher image_pub;
    image_transport::Publisher image_pub_compress;
    image_transport::ImageTransport it(n);
    image_pub = it.advertise("image_raw", 1);
    image_pub_compress = it.advertise("image_raw_compress", 1);

    sensor_msgs::Image img_;
    sensor_msgs::Image img_compress_;
    ros::Rate loop_rate(25);
    cv::Mat frame;
    cv::VideoCapture cap(0);

    std::vector<int> params;
    std::vector<uchar> buf;
    params.push_back(CV_IMWRITE_JPEG_QUALITY);
    params.push_back(25); //image quality

    while (ros::ok()){
        cap>> frame;
        fillImage(img_,
                  "bgr8",
                  frame.rows,
                  frame.cols,
                  frame.channels() * frame.cols,
                  frame.data);

        cv::imencode(".jpg", frame, buf, params);
        cv::Mat frame_compress(buf);
        fillImage(img_compress_,
                  "mono8",
                  frame_compress.rows,
                  frame_compress.cols,
                  frame_compress.channels()* frame_compress.cols,
                  frame_compress.data);

        image_pub.publish(img_);
        image_pub_compress.publish(img_compress_);

        ros::spinOnce();
        loop_rate.sleep();
    }
    return 0;
}

