//
// Created by deren zhu on 2019/11/17.
//

#ifndef REMOTEVIM_HOST_H
#define REMOTEVIM_HOST_H

class Host {
private:

    std::string username{};
    std::string hostname{};
    int port;

public:
    explicit Host(std::string u_name, std::string h_name, int p);
    ~Host();
    std::string get_username() const { return username; };
    std::string get_hostname() const { return hostname; };
    int get_port() const { return port; };
};


#endif //REMOTEVIM_HOST_H
