//
// Created by deren zhu on 2019/11/26.
//

#include <iostream>
#include <spdlog/spdlog.h>
#include "Session.h"

std::vector<std::string> Session::get_output(const std::string &c) {
    FILE *fp;
    char buff[1000];
    std::vector<std::string> result;
    fp = popen("ls", "r");
    spdlog::info("exec command in {}@{}:{} at {}",
                 host.get_username(),
                 host.get_hostname(),
                 host.get_port(),
                 current_path);
    while (fgets(buff, sizeof(buff), fp) != nullptr) {
        std::string item = buff;
        item.erase(item.find('\n'), 2);
        result.emplace_back(item);
    }
    return result;
}

Session::Session(const Host &h) : host(h) {
    spdlog::info("create session in {}@{}:{}",
        host.get_username(),
        host.get_hostname(),
        host.get_port());
}

void Session::set_current_path(const std::string& path) {
    this->current_path = path;
}

Session::~Session() = default;
