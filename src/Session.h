//
// Created by deren zhu on 2019/11/26.
//

#ifndef REMOTEVIM_SESSION_H
#define REMOTEVIM_SESSION_H
#include "Host.h"
#include <vector>
#include <string>

class Session {
public:
    explicit Session(const Host& h);
    ~Session();
    std::shared_ptr<std::vector<std::string>> get_output(const std::string& cmd);
    void set_current_path(const std::string& path);
private:
    Host host;
    std::string current_path = "/";
};


#endif //REMOTEVIM_SESSION_H
