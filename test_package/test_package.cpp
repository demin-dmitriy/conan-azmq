#include <cstdlib>
#include <iostream>

#include <azmq/socket.hpp>
#include <boost/asio.hpp>

int main()
{
    boost::asio::io_service ios;
    azmq::pull_socket pull_sock(ios);
    azmq::push_socket push_sock(ios);

    push_sock.bind("inproc://example");
    pull_sock.connect("inproc://example");

    azmq::message m1("hello, azmq!");
    push_sock.send(m1);

    azmq::message m2;
    pull_sock.receive(m2);

    std::cout << m2.string() << std::endl;

    return EXIT_SUCCESS;
}
