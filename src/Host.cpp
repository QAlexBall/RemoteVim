//
// Created by deren zhu on 2019/11/17.
//

#include <string>
#include <utility>
#include "spdlog/spdlog.h"
#include "Host.h"


Host::Host(std::string u_name, std::string h_name, int p) :
    username(std::move(u_name)), hostname(std::move(h_name)), port(p) {

    spdlog::info("Host {}@{}:{} created!", username, hostname, port);
}

Host::~Host() = default;
